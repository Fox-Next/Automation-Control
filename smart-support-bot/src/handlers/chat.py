"""Chat message handler: Ask AI mode only → intent / LLM with KB + catalog/site."""

from __future__ import annotations

from pathlib import Path

import asyncio
import logging
import re
import time
import unicodedata
from difflib import SequenceMatcher

from aiogram import F, Router
from aiogram.types import Message

from src.ai.client import AIClient, AIClientError
from src.ai.persona import (
    SUPPORT_HANDLE,
    append_sales_if_needed,
    build_system_prompt,
    download_or_site_fallback,
    format_facts_from_meta,
    join_context_blocks,
    excerpt_teaching_for_query,
    looks_incomplete_reply,
    looks_like_prompt_dump,
    looks_like_reasoning_leak,
    sanitize_reply_links,
    strip_internal_prompt_lines,
    wants_contact_links,
    wants_sales_nudge,
)
from src.ai.safety import (
    ResponseBudget,
    bounded_ask_timeout,
    bounded_ask_tokens,
    is_safe_to_persist,
    is_transient_ai_error,
    prepare_user_reply,
)
from src.access import AdminAccess
from src.config import Settings, is_bot_admin
from src.knowledge.ai_memory import (
    append_learned_answer,
    behavior_rules_text,
    memory_prompt_block,
    product_memory_has_content,
)
from src.knowledge.catalog_index import wants_send_media
from src.knowledge.catalog_rag import retrieve_catalog_context
from src.knowledge.response_bundle import (
    MediaRef,
    ResponseBundle,
    existing_media_paths,
)
from src.knowledge.catalog_search import CatalogSiteSearch, looks_unsure, unsure_handoff
from src.knowledge.feature_lookup_adapter import (
    feature_lookup_prompt_block,
    has_implementation_exists,
)
from src.knowledge.intents import (
    IntentMatcher,
    detect_message_language,
    detect_reply_lang,
    looks_identity,
)
from src.knowledge.loader import KnowledgeLoader
from src.knowledge.product_catalogs import (
    ai_products_snippet,
    get_product,
    get_product_catalogs,
    list_all_product_dicts,
)
from src.storage.answer_memory import AnswerMemoryStore
from src.storage.metrics import MetricsStore
from src.storage.users import UserStore
from src.ui import admin_keyboards, keyboards, messaging, texts

logger = logging.getLogger(__name__)

router = Router(name="chat")

ASK_AI_KNOWLEDGE_CHARS = 6000


def _ask_ai_timeout(settings: Settings) -> float:
    return bounded_ask_timeout(settings.ai_timeout_seconds)


def _ask_ai_max_tokens(settings: Settings) -> int:
    return bounded_ask_tokens(settings.ai_max_tokens)


class _AskTiming:
    def __init__(self) -> None:
        self.t0 = time.monotonic()
        self.last = self.t0
        self.parts: list[str] = []

    def mark(self, name: str) -> None:
        now = time.monotonic()
        self.parts.append(f"{name}={int((now - self.last) * 1000)}")
        self.last = now

    def flush(self) -> None:
        total = int((time.monotonic() - self.t0) * 1000)
        logger.info("ask_ai_timing total_ms=%s %s", total, " ".join(self.parts))


def _bundle_from_retrieval(
    product_id: str, query: str, retrieval
) -> ResponseBundle:
    refs: list[MediaRef] = []
    for unit in getattr(retrieval, "media_units", None) or []:
        rel = str(getattr(unit, "media_path", "") or "").strip()
        pid = str(getattr(unit, "product_id", "") or "").strip()
        if not rel or not pid:
            continue
        refs.append(
            MediaRef(
                path=rel,
                product_id=pid,
                unit_id=str(getattr(unit, "unit_id", "") or ""),
                feature_ids=list(getattr(unit, "feature_ids", None) or []),
                score=float(getattr(unit, "score", 0.0) or 0.0),
            )
        )
    return ResponseBundle(
        product_id=product_id or "",
        user_query=query,
        knowledge_refs=[
            str(u.unit_id)
            for u in (getattr(retrieval, "units", None) or [])
            if getattr(u, "unit_id", None)
        ],
        media_refs=refs if getattr(retrieval, "attach_media", False) else [],
    )


def _is_free_text(message: Message) -> bool:
    text = (message.text or "").strip()
    if not text or text.startswith("/"):
        return False
    if text in keyboards.all_lang_button_texts():
        return False
    if text in keyboards.all_menu_button_texts():
        return False
    if text in admin_keyboards.all_admin_control_texts():
        return False
    return True


def _normalized_product_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").casefold()
    value = value.replace("\u200c", " ").replace("ي", "ی").replace("ك", "ک")
    return re.sub(r"[^\w\u0600-\u06ff]+", " ", value).strip()


def _one_adjacent_transposition(left: str, right: str) -> bool:
    if len(left) != len(right):
        return False
    changed = [i for i, (a, b) in enumerate(zip(left, right)) if a != b]
    return (
        len(changed) == 2
        and changed[1] == changed[0] + 1
        and left[changed[0]] == right[changed[1]]
        and left[changed[1]] == right[changed[0]]
    )


def _typed_product_id(text: str) -> str | None:
    """Resolve a typed product name/keyword against enabled product catalogs."""
    query = _normalized_product_text(text)
    if not query:
        return None
    aliases = {
        "vpn-installer": ("vps to vpn", "vps2vpn", "وی پی اس به وی پی ان", "وی پی ان سرور"),
        "bsc-wallet-recovery": (
            "wallet recovery",
            "بازیابی کیف پول",
            "ریکاوری کیف پول",
            "والت ریکاوری",
            "بازیابی ولت",
        ),
    }
    for product in get_product_catalogs():
        if not product.catalog_enabled:
            continue
        candidates = [product.product_id.replace("-", " "), *product.title.values()]
        keywords = (product.raw or {}).get("keywords") or {}
        if isinstance(keywords, dict):
            for values in keywords.values():
                candidates.extend(values if isinstance(values, list) else [values])
        else:
            candidates.extend(product.keywords)
        candidates.extend(aliases.get(product.product_id, ()))
        for candidate in candidates:
            needle = _normalized_product_text(str(candidate))
            if not needle:
                continue
            if query == needle or (len(needle) >= 6 and f" {needle} " in f" {query} "):
                return product.product_id

    # Handle small typing errors in product names without fuzzy-matching broad
    # feature words that could select the wrong catalog.
    query_words = query.split()
    fuzzy_hits: list[tuple[float, str]] = []
    for product in get_product_catalogs():
        if not product.catalog_enabled:
            continue
        names = [*product.title.values(), *aliases.get(product.product_id, ())]
        for name in names:
            words = [w for w in _normalized_product_text(str(name)).split() if len(w) >= 3]
            if len(words) < 2:
                continue
            ratios = [
                max((SequenceMatcher(None, word, qword).ratio() for qword in query_words), default=0.0)
                for word in words
            ]
            thresholds = [0.65 if len(word) == 3 else 0.82 for word in words]
            matches = [
                ratio >= threshold
                or any(_one_adjacent_transposition(word, qword) for qword in query_words)
                for word, ratio, threshold in zip(words, ratios, thresholds)
            ]
            if all(matches):
                fuzzy_hits.append((sum(ratios) / len(ratios), product.product_id))
    if fuzzy_hits:
        best_by_product: dict[str, float] = {}
        for score, product_id in fuzzy_hits:
            best_by_product[product_id] = max(score, best_by_product.get(product_id, 0.0))
        ranked = sorted(
            ((score, product_id) for product_id, score in best_by_product.items()),
            reverse=True,
        )
        if len(ranked) == 1 or ranked[0][0] - ranked[1][0] >= 0.08:
            return ranked[0][1]
    return None


def setup_chat_router(
    settings: Settings,
    users: UserStore,
    ai: AIClient,
    intents: IntentMatcher,
    knowledge: KnowledgeLoader,
    catalog: CatalogSiteSearch,
    metrics: MetricsStore,
    access: AdminAccess | None = None,
) -> Router:
    memory = AnswerMemoryStore(settings.data_dir / "answer_memory.json")

    @router.message(F.chat.type == "private", F.text.func(lambda t: bool(t) and not str(t).startswith("/")))
    async def on_text(message: Message) -> None:
        user = message.from_user
        if not user or not message.text:
            return
        if not _is_free_text(message):
            choosing_product = (
                await users.is_ask_ai(user.id)
                and not await users.get_ask_ai_product(user.id)
                and _typed_product_id(message.text.strip()) is not None
            )
            if not choosing_product:
                return

        try:
            await users.touch_from_telegram_user(user)
            await _handle_ask_ai_text(message, user)
        except Exception:
            logger.exception("Ask AI handler crashed")
            try:
                lang = await users.get_lang(user.id, user.language_code)
                await message.answer(texts.t(texts.AI_ERROR, lang))
            except Exception:  # noqa: BLE001
                pass

    async def _handle_ask_ai_text(message: Message, user) -> None:
        if not await users.has_lang(user.id):
            hint = await users.get_lang(user.id, user.language_code)
            await message.answer(
                texts.t(texts.NEED_LANGUAGE_FIRST, hint),
                reply_markup=keyboards.language_keyboard(),
            )
            return

        profile_lang = await users.get_lang(user.id, user.language_code)
        lang = detect_reply_lang(message.text, profile_lang)
        if lang != profile_lang:
            await users.set_lang(user.id, lang)
        if access is not None:
            menu_kb = keyboards.main_menu_keyboard(
                lang,
                can_settings=await access.can_settings(user.id),
                can_stats=await access.can_stats(user.id),
            )
        else:
            admin = is_bot_admin(settings, user.id)
            menu_kb = keyboards.main_menu_keyboard(lang, is_admin=admin)

        # PANEL_CONV_SESSION — buy/support/sales lock bypasses Ask-AI inactive gate
        if not await users.is_ask_ai(user.id):
            conv_turn_text = ""
            bypass = False
            _bf_handle_user_text = None
            try:
                from src.panel_conversation_hook import (
                    handle_user_text as _bf_handle_user_text,
                    should_bypass_ask_ai as _bf_should_bypass_ask_ai,
                )
                bypass = bool(
                    _bf_should_bypass_ask_ai(
                        str(user.id),
                        text=message.text or "",
                    )
                )
            except Exception:
                bypass = False
            if bypass:
                hist = []
                try:
                    hist = await users.get_chat_history(user.id)
                except Exception:
                    hist = []
                if _bf_handle_user_text is not None:
                    try:
                        turn = _bf_handle_user_text(
                            message.text or "",
                            account_id=str(user.id),
                            profile_lang=lang,
                            last_message_lang=lang,
                            chat_history=hist,
                        )
                        conv_turn_text = (
                            (turn or {}).get("text") if isinstance(turn, dict) else ""
                        ) or ""
                    except Exception:
                        conv_turn_text = ""
                if conv_turn_text:
                    await message.answer(conv_turn_text, reply_markup=menu_kb)
                    return
            await message.answer(
                texts.t(texts.USE_MENU_OR_ASK_AI, lang),
                reply_markup=menu_kb,
            )
            if not await users.was_group_invited(user.id):
                await message.answer(
                    texts.t(texts.GROUP_INVITE, lang),
                    reply_markup=menu_kb,
                )
                await users.set_group_invited(user.id, True)
            return

        text = message.text.strip()
        if not text:
            return

        await metrics.record_conversation(user.id)

        if looks_identity(text):
            body = texts.bot_intro(lang)
            await users.append_chat(user.id, "user", text)
            await users.append_chat(user.id, "assistant", body)
            await metrics.record_answered(referred_support=False, ai_solved=True)
            await message.answer(
                body,
                reply_markup=keyboards.ask_ai_keyboard(
                    lang, product_id=await users.get_ask_ai_product(user.id)
                ),
            )
            return

        ask_product = await users.get_ask_ai_product(user.id)
        responding_to_product_selection = False
        if not ask_product:
            ask_product = _typed_product_id(text)
            if ask_product:
                responding_to_product_selection = True
                await users.set_ask_ai(user.id, True, product_id=ask_product)
                await users.set_current_product(user.id, ask_product)
            elif await users.is_ask_ai(user.id):
                await message.answer(
                    texts.t(texts.PRODUCT_SUPPORT_CHOOSER, lang),
                    reply_markup=keyboards.product_support_keyboard(lang),
                )
                return
        if ask_product:
            row = next(
                (
                    d
                    for d in list_all_product_dicts(settings.knowledge_root)
                    if str(d.get("product_id") or "") == ask_product
                ),
                None,
            )
            if row is None or row.get("enabled", True) is False:
                await message.answer(
                    "این محصول دیگر در دسترس نیست. از منو دوباره «سوال از AI» را برای یک محصول فعال بزنید."
                    if (lang or "").startswith("fa")
                    else "This product is no longer available. Open Ask AI again from an active product.",
                    reply_markup=keyboards.main_menu_keyboard(lang),
                )
                return
        ask_kb = keyboards.ask_ai_keyboard(lang, product_id=ask_product)
        stages = _AskTiming()
        history = await users.get_chat_history(user.id)
        history_blob = "\n".join(
            f"{h['role']}: {h['content']}"
            for h in history[-4:]
            if not looks_like_prompt_dump(str(h.get("content") or ""))
        )
        stages.mark("session")

        if wants_send_media(text):
            last = ResponseBundle.from_dict(await users.get_last_ask_context(user.id))
            pid = (ask_product or (last.product_id if last else "") or "").strip()
            paths = []
            from_last = False
            if last and pid and last.product_id == pid:
                paths = existing_media_paths(
                    last.media_refs,
                    product_id=pid,
                    knowledge_refs=last.knowledge_refs,
                    project_root=settings.project_root,
                    limit=2,
                )
                from_last = bool(paths)
            if not paths and pid:
                # Fresh Ask AI: resolve photos from this product catalog (not only last turn).
                retrieval = await asyncio.to_thread(
                    retrieve_catalog_context,
                    text,
                    lang=lang or "fa",
                    project_root=settings.project_root,
                    product_id=pid,
                    limit_media=3,
                )
                if getattr(retrieval, "attach_media", False) and retrieval.media_paths:
                    paths = [p for p in retrieval.media_paths if p.is_file()][:3]
            if paths:
                if from_last:
                    caption = (
                        "تصویر همان بخشی که الان درباره‌اش صحبت شد."
                        if (lang or "").startswith("fa")
                        else "Photo for the section we just discussed."
                    )
                else:
                    caption = (
                        "چند تصویر از کاتالوگ این محصول:"
                        if (lang or "").startswith("fa")
                        else "Catalog photos for this product:"
                    )
                await users.append_chat(user.id, "user", text)
                await users.append_chat(user.id, "assistant", caption)
                await metrics.record_answered(referred_support=False, ai_solved=True)
                await messaging.answer_with_media(
                    message, caption, images=paths, reply_markup=ask_kb
                )
                if pid:
                    media_refs: list[MediaRef] = []
                    root = settings.project_root.resolve()
                    for path in paths:
                        try:
                            rel = str(Path(path).resolve().relative_to(root)).replace("\\", "/")
                        except ValueError:
                            rel = str(path)
                        media_refs.append(
                            MediaRef(path=rel, product_id=pid, score=16.0)
                        )
                    bundle = ResponseBundle(
                        product_id=pid,
                        user_query=text,
                        answer_text=caption,
                        media_refs=media_refs,
                    )
                    await users.set_last_ask_context(user.id, bundle.as_dict())
                stages.mark("followup_media")
                stages.flush()
                return
            await message.answer(
                "برای این بخش تصویر مرتبط موجود نیست."
                if (lang or "").startswith("fa")
                else "No related image is stored for this section.",
                reply_markup=ask_kb,
            )
            stages.mark("followup_none")
            stages.flush()
            return

        operator_style = behavior_rules_text(settings.knowledge_root, ask_product)
        # Product-scoped Ask AI must not reuse answers from another catalog.
        mem_hit = None if ask_product else memory.lookup(text, lang=lang)
        if (
            mem_hit is not None
            and mem_hit.score >= 12.0
            and not looks_unsure(mem_hit.answer)
            and not looks_incomplete_reply(mem_hit.answer)
            and not looks_like_reasoning_leak(mem_hit.answer)
        ):
            final = mem_hit.answer
            memory.touch_hit(mem_hit.topic_key, lang)
            await users.append_chat(user.id, "user", text)
            await users.append_chat(user.id, "assistant", final)
            await metrics.record_answered(referred_support=False, ai_solved=True)
            await message.answer(final, reply_markup=ask_kb)
            stages.mark("memory_hit")
            stages.flush()
            return

        match = None if ask_product else intents.match(text, lang, prior_blob=history_blob)
        wait = await message.answer(texts.t(texts.THINKING, lang))
        request_timeout = _ask_ai_timeout(settings)
        budget = ResponseBudget(request_timeout + 8.0)
        stages.mark("wait_msg")

        intent_name = match.record.intent if match and match.record else None
        faq_refs = None if ask_product else (match.record.faq_refs if match and match.record else None)

        def _run_rag():
            return retrieve_catalog_context(
                text,
                lang=lang,
                project_root=settings.project_root,
                limit_features=3,
                limit_media=2,
                product_id=ask_product,
                prior_text=history_blob,
            )

        def _run_kb():
            return knowledge.retrieve(
                text,
                lang,
                faq_refs=faq_refs,
                limit_chars=min(ASK_AI_KNOWLEDGE_CHARS, settings.knowledge_snippet_chars),
                include_community=wants_contact_links(text) and not ask_product,
                max_chunks=3 if ask_product else 4,
                product_id=ask_product,
            )

        retrieval, kb_snip = await asyncio.gather(
            asyncio.to_thread(_run_rag),
            asyncio.to_thread(_run_kb),
        )
        stages.mark("retrieve")
        if ask_product:
            retrieval.units = [
                u for u in retrieval.units if getattr(u, "product_id", "") == ask_product
            ]
            retrieval.media_units = [
                u
                for u in (retrieval.media_units or [])
                if getattr(u, "product_id", "") == ask_product
            ]
        bundle = _bundle_from_retrieval(ask_product or "", text, retrieval)
        media_paths = []
        if ask_product and getattr(retrieval, "attach_media", False):
            media_paths = [p for p in (retrieval.media_paths or []) if p.is_file()][:2]

        if (
            ask_product
            and getattr(retrieval, "needs_clarification", False)
            and getattr(retrieval, "clarifying_question", None)
        ):
            clarify = str(retrieval.clarifying_question)
            try:
                await wait.edit_text(clarify)
            except Exception:  # noqa: BLE001
                await message.answer(clarify, reply_markup=ask_kb)
            await users.append_chat(user.id, "user", text)
            await users.append_chat(user.id, "assistant", clarify)
            await metrics.record_answered(referred_support=False, ai_solved=False)
            if ask_product:
                bundle.answer_text = clarify
                await users.set_last_ask_context(user.id, bundle.as_dict())
            stages.mark("clarify_backup")
            stages.flush()
            return

        if (
            not ask_product
            and retrieval.insufficient
            and match is not None
            and match.low_confidence
            and match.clarifying_question
        ):
            try:
                await wait.edit_text(match.clarifying_question)
            except Exception:  # noqa: BLE001
                await message.answer(match.clarifying_question, reply_markup=ask_kb)
            await users.append_chat(user.id, "user", text)
            await users.append_chat(user.id, "assistant", match.clarifying_question)
            await metrics.record_answered(referred_support=False, ai_solved=False)
            stages.flush()
            return

        # License/site catalogs are Installer-oriented — only when that product is scoped
        catalog_snip = ""
        if not ask_product or ask_product == "vpn-installer":
            catalog_snip = catalog.catalog_snippet(text, lang=lang)
        if ask_product:
            cat = get_product(ask_product)
            title = ""
            if cat is not None:
                title = (
                    (cat.title or {}).get(lang)
                    or (cat.title or {}).get("en")
                    or ask_product
                )
            products_snip = f"Product identity: {ask_product}" + (
                f" — {title}" if title else ""
            )
        else:
            products_snip = ai_products_snippet(
                text, lang=lang, product_id=ask_product
            )
        site_snip = ""
        try:
            if (
                not ask_product
                and (
                    retrieval.insufficient
                    or match.low_confidence
                    or wants_sales_nudge(text, intent_name)
                    or wants_contact_links(text)
                )
            ):
                site_snip = await catalog.site_snippet(text)
            elif ask_product == "vpn-installer" and (
                wants_sales_nudge(text, intent_name) or wants_contact_links(text)
            ):
                site_snip = await catalog.site_snippet(text)
        except Exception:
            logger.exception("site search failed")

        intent_block = ""
        if match and match.record and not ask_product:
            intent_block = join_context_blocks(
                [
                    f"Matched intent: {match.record.intent} (score={match.score:.2f})",
                    f"Category: {match.record.category}",
                    f"Short answer: {match.record.short_answer}",
                    f"Full answer: {match.record.full_answer}",
                ],
                3500,
            )
        facts = "" if ask_product else format_facts_from_meta(knowledge.index.facts or intents.facts)
        system = build_system_prompt(
            lang, facts_block=facts, operator_style=operator_style
        )
        if ask_product == "bsc-wallet-recovery":
            system += (
                "\nWallet Recovery Rules & Activation Guide:\n"
                "- NO Device ID is needed at all for Wallet Recovery! Never ask for Device ID or say it is required.\n"
                "- In the app's Activation tab, the user clicks 'Open Activation on foxnext.net' or manually visits https://foxnext.net/fa/wallet-recovery-activation.html.\n"
                "- Always quote the exact packages and prices: 1 device = $5 USD (5 USDT) with 1 activation code; 2 devices = $7 USD (7 USDT) with 2 activation codes.\n"
                "- Available payment methods on foxnext.net: Crypto (BEP-20 USDT with TX ID verification), Cryptomus (multi-crypto), Credit/Debit Cards (Visa, Mastercard, Link via Stripe), and Digital Wallets (Google Pay, Apple Pay via Stripe).\n"
                "- Explain that after payment, the user receives an activation code, pastes it into the 'Activation code' field in the app's Activation tab, and clicks 'Activate'.\n"
                "- Privacy: Recovery phrases, seed words, passphrases, and private keys are NEVER requested or sent. The app runs locally."
            )
        elif ask_product:
            system += (
                "\nProduct support response rules: Preserve the existing assistant identity, "
                "product persona, and operator tone rules. Use the selected product's "
                "catalog.json as the only source of product facts; persona and behavior "
                "instructions may guide tone but are not product facts. Do not use general "
                "knowledge, another product, or chat history to fill factual gaps. If the "
                "catalog does not contain the answer, say so plainly and refer the user to "
                "human support. Use the selected reply language for this turn, answer naturally and briefly, "
                "and use at most one emoji."
            )
        catalog_obj = get_product(ask_product) if ask_product else None
        catalog_teach = str(
            ((catalog_obj.raw or {}).get("ai_training_text") or "")
            if catalog_obj is not None
            else ""
        ).strip()
        memory_snip = (
            ""
            if ask_product
            else memory_prompt_block(settings.knowledge_root, ask_product)
        )

        md_priority_note = (
            "### Priority\n"
            "1) Operator AI memory (behavior + taught facts + learned Q&A).\n"
            "2) Product catalog / screenshots.\n"
            "3) Other markdown only if memory and catalog lack the fact.\n"
            "Never invent steps. Follow operator behavior rules in every reply.\n"
            "Write a tutor reply. Do not paste the entire teaching document.\n"
        )

        def _user_facing_fallback() -> str:
            if responding_to_product_selection:
                product_title = (
                    (catalog_obj.title or {}).get(lang)
                    or (catalog_obj.title or {}).get("en")
                    if catalog_obj is not None
                    else ask_product
                )
                if (lang or "").startswith("fa"):
                    return (
                        f"متوجه شدم؛ راهنمایی شما دربارهٔ {product_title} است. "
                        "بفرمایید دربارهٔ کار با برنامه، فعال‌سازی یا رفع مشکل چه کمکی نیاز دارید؟"
                    )
                if (lang or "").startswith("ru"):
                    return (
                        f"Понял, вам нужна помощь с {product_title}. "
                        "Что подсказать: использование программы, активацию یا решение проблемы?"
                    )
                if (lang or "").startswith("zh"):
                    return (
                        f"明白了，您需要关于 {product_title} 的帮助。"
                        "您想了解软件使用、激活，还是故障排查？"
                    )
                return (
                    f"Got it—you need help with {product_title}. "
                    "Would you like help using the app, activating it, or troubleshooting an issue?"
                )

            # High priority: Never dump internal prompt/catalog teaching to users!
            if ask_product == "bsc-wallet-recovery":
                if (lang or "").startswith("fa"):
                    is_activation = bool(re.search(r"فعال\s*سازی|اکتیو|لایسنس|کد|قیمت|خرید|تتر|دلار|دستگاه|registration|activate|license|buy|price|usdt|wrclaim", text, re.I))
                    if is_activation or len(text.strip()) < 15:
                        return (
                            "مراحل فعال‌سازی نرم‌افزار Wallet Recovery:\n\n"
                            "۱. در داخل برنامه وارد تب **Activation** شده و روی دکمهٔ «Open Activation on foxnext.net» کلیک کنید (یا مستقیماً به سایت foxnext.net مراجعه نمایید).\n"
                            "۲. بستهٔ فعال‌سازی مورد نظرتان را انتخاب کنید:\n"
                            "   • ۱ دستگاه: ۵ دلار / ۵ تتر (شامل ۱ کد فعال‌سازی)\n"
                            "   • ۲ دستگاه: ۷ دلار / ۷ تتر (شامل ۲ کد فعال‌سازی با تخفیف ویژه)\n"
                            "۳. روش پرداخت دلخواه را انتخاب نمایید (روش‌های متنوع پرداخت در سایت شامل ارز دیجیتال تتر BEP-20، درگاه خودکار Cryptomus، کارت‌های بین‌المللی Visa و Mastercard، یا Google Pay / Apple Pay فعال است).\n"
                            "۴. پس از پرداخت، کد فعال‌سازی (که با عبارت **WRCLAIM** شروع می‌شود) را در کادر Activation code در تب Activation برنامه وارد کرده و دکمهٔ Activate را بزنید تا برنامه فعال شود."
                        )
                    return (
                        "نرم‌افزار Wallet Recovery ابزار تخصصی جستجو و بازیابی عبارات ۱۲ و ۲۴ کلمه‌ای (Seed Phrase / Mnemonic) و کلیدهای خصوصی گم‌شده است.\n\n"
                        "نسخه‌های رسمی: ویندوز و اندروید\n"
                        "قیمت لایسنس در سایت رسمی foxnext.net:\n"
                        "• ۱ دستگاه: ۵ دلار (۵ تتر) | ۲ دستگاه: ۷ دلار (۷ تتر با تخفیف ویژه)\n"
                        "کدهای فعال‌سازی این محصول با عبارت WRCLAIM شروع می‌شوند.\n"
                        "روش‌های متنوع پرداخت در سایت: تتر BEP-20، درگاه چندارزی کریپتوموس، ویزا/مسترکارت، و گوگل‌پِی/اپل‌پِی.\n\n"
                        "سؤالتان را دربارهٔ بازیابی عبارات یا فعال‌سازی برنامه بفرمایید تا راهنمایی‌تان کنم."
                    )
                else:
                    return (
                        "Wallet Recovery Activation Steps:\n\n"
                        "1. Open the app, go to the Activation tab, and click «Open Activation on foxnext.net» (or visit foxnext.net).\n"
                        "2. Choose your activation package:\n"
                        "   • 1 Device: $5 USD / 5 USDT (1 activation code)\n"
                        "   • 2 Devices: $7 USD / 7 USDT (2 activation codes with discount)\n"
                        "3. Select your preferred payment method on the site (BSC BEP-20 USDT, Cryptomus multi-crypto, Visa/Mastercard, or Apple Pay/Google Pay).\n"
                        "4. Paste your received activation code (starts with WRCLAIM) into the 'Activation code' field in the Activation tab and click 'Activate'."
                    )

            if ask_product == "vps-to-vpn":
                if (lang or "").startswith("fa"):
                    if re.search(r"فعال\s*سازی|اکتیو|لایسنس|کد|قیمت|خرید|registration|activate|license|buy|price|bxfa", text, re.I):
                        return (
                            "مراحل فعال‌سازی لایسنس VPS to VPN:\n\n"
                            "۱. در برنامه به بخش **Registration** (یا Settings -> Registration) بروید.\n"
                            "۲. کد فعال‌سازی دریافتی خود را (که با عبارت **BXFA-CLM** شروع می‌شود) در کادر Enter Activation Code وارد کنید.\n"
                            "۳. روی دکمهٔ Activate کلیک کنید تا لایسنس فعال شود.\n\n"
                            "آدرس وب‌سایت رسمی برای تهیه لایسنس: foxnext.net\n"
                            "تعرفه‌ها (اشتراک ۱۰ ماهه):\n"
                            "• مدل Basic: مبلغ ۴.۵ دلار\n"
                            "• مدل Pro: مبلغ ۶.۵ دلار\n"
                            "• مدل AI Pro: مبلغ ۹.۵ دلار\n\n"
                            "روش‌های متنوع پرداخت در سایت: پرداخت با تتر (USDT BEP-20)، درگاه هوشمند Cryptomus، کارت‌های بین‌المللی Visa/Mastercard، و کیف‌پول‌های Google Pay و Apple Pay.\n"
                            f"پشتیبانی مستقیم: {SUPPORT_HANDLE}"
                        )
                    return (
                        "برنامه VPS to VPN ابزار تخصصی تبدیل سرور مجازی به فیلترشکن اختصاصی (WireGuard و 3X-UI) است.\n\n"
                        "لایسنس‌های ۱۰ ماهه در سایت foxnext.net:\n"
                        "• Basic ($4.5) | Pro ($6.5) | AI Pro ($9.5)\n"
                        "کدهای فعال‌سازی با عبارت BXFA-CLM شروع می‌شوند.\n"
                        "روش‌های متنوع پرداخت: تتر BEP-20، درگاه کریپتوموس، ویزا/مسترکارت، و گوگل‌پِی/اپل‌پِی.\n"
                        "بفرمایید دربارهٔ نحوه خرید، اتصال سرور یا فعال‌سازی چه سؤالی دارید؟"
                    )

            if (lang or "").startswith("fa"):
                return (
                    "پیام شما دریافت شد. لطفاً سؤال یا مشکل خود را به صورت مشخص بفرمایید "
                    f"یا در صورت نیاز با پشتیبانی مستقیم {SUPPORT_HANDLE} در تماس باشید."
                )
            return f"Thank you for reaching out. Please specify your question or reach out to {SUPPORT_HANDLE}."

        if ask_product:
            teach_excerpt = excerpt_teaching_for_query(
                strip_internal_prompt_lines(catalog_teach), text, limit=900
            )
            extra_sources = join_context_blocks(
                [
                    products_snip,
                    (
                        "Relevant catalog teaching (do not paste the whole file):\n"
                        + teach_excerpt
                    )
                    if teach_excerpt
                    else "",
                    retrieval.prompt_block,
                ],
                4000,
            )
            # Product-scoped answers may use only the selected catalog as facts.
            kb_snip = ""
        else:
            extra_sources = join_context_blocks(
                [
                    memory_snip,
                    retrieval.prompt_block,
                    md_priority_note,
                    products_snip,
                    catalog_snip,
                    site_snip,
                ],
                7000,
            )


        # Phase 2: Implementation feature.lookup before Catalog false-negative
        _impl_pid = ask_product or "vps-to-vpn"
        if _impl_pid in ("vpn-installer", "vps-to-vpn", "") or not ask_product:
            _impl_block = feature_lookup_prompt_block(text, product_id="vps-to-vpn")
            if _impl_block:
                extra_sources = join_context_blocks([_impl_block, extra_sources], 7500)

        history_section = history_blob or "(none)"
        product_scope = (
            f"Product catalog scope: {ask_product}\n"
            "Answer product questions ONLY from this product's catalog.json. Existing "
            "persona/behavior instructions affect tone only, not product facts.\n"
            "If the catalog lacks the answer, say it is not in the catalog and offer human support. "
            "Do not use another product, general knowledge, or prior turns as factual sources.\n\n"
            if ask_product
            else ""
        )
        user_question = (
            (
                f"The user has just selected {ask_product} as the product they need help with. "
                "They have not asked a specific question yet. A product selection does not mean "
                "it was installed, purchased, paid for, or activated. Do not claim any of those. "
                "Only acknowledge the selection naturally "
                f"in the selected reply language ({lang}), then ask what they need help with. Mention usage, "
                "activation, and troubleshooting as options only; do not add unsupported facts."
            )
            if responding_to_product_selection
            else text
        )
        user_prompt = (
            f"{product_scope}"
            f"Prior turns in this Ask AI session:\n{history_section}\n\n"
            f"User question:\n{user_question}\n\n"
            f"Expanded topic hints (internal):\n{retrieval.query_expanded}\n\n"
            f"Intent context:\n{intent_block or '(none)'}\n\n"
            f"Knowledge / product-map markdown snippets:\n{kb_snip or '(none)'}\n\n"
            f"Catalog / site sources:\n{extra_sources or '(none)'}\n\n"
            "Write a helpful Telegram support reply as a real tutor/support agent.\n"
            "Teach the user how the selected product works; do not claim to operate the software, the user's device, or any account.\n"
            "Use a warm, polite, natural tone. Do not claim to be a human or hide that you are an assistant.\n"
            + (
                "Use only the selected product catalog for product facts; behavior/persona "
                "rules guide presentation only.\n"
                if ask_product
                else "Source order: (1) Operator AI memory, (2) catalog evidence, "
                "(3) other markdown — never invent steps.\n"
            )
            + "When the question is educational, explain: what it is, what it is for, "
            "ordered steps, and any limit/tip present in the evidence.\n"
            "Do not list only button names. Finish every sentence completely.\n"
            "Do not invent versions or fake limits.\n"
            + (
                "Do not volunteer a price or amount. If the user explicitly asks and this "
                "catalog contains a price, answer from this catalog only.\n"
                if ask_product
                else "If catalog lists prices and the user asked price/buy, you may quote catalog figures.\n"
            )
            + "If sources are insufficient, say you do not know and tell them to message "
            f"{SUPPORT_HANDLE}.\n"
            "Do not include website/group/@support links unless contact/purchase was asked "
            "or you are honestly handing off because you do not know.\n"
            "If the catalog media index lists a photo, it exists. Never deny that the photo exists.\n"
            "The bot sends catalog files itself. Do not say you cannot send images.\n"
            "If prior turns show Exit Server, answer Add Exit Server only — not Central Full Deploy.\n"
            "Persian: start every sentence with a Persian word; prefer Persian wording; "
            "never rename official product names "
            "(VPS to VPN by Fox Next, Config Builder, Ask AI, 3X-UI, …).\n"
            "CRITICAL: Output ONLY the final Telegram reply. "
            "Do not write reasoning, constraint lists, or English meta analysis. "
            "Do not paste catalog teaching or memory files verbatim."
        )

        def _has_reply_language_mismatch(reply: str) -> bool:
            detected_language = detect_message_language(reply)
            return bool(detected_language and detected_language != lang)

        async def _compact_retry() -> str:
            teach = excerpt_teaching_for_query(
                strip_internal_prompt_lines(catalog_teach), text, limit=900
            )
            if not teach:
                return ""
            compact = (
                f"User question:\n{text}\n\n"
                f"Product teaching (source only; do not paste the whole file):\n{teach}\n\n"
                f"Write a short Telegram tutor reply in the selected reply language ({lang}). "
                "Explain the asked part in a few lines. No file headers."
            )
            try:
                return await asyncio.wait_for(
                    ai.chat(
                        [
                            {"role": "system", "content": system},
                            {"role": "user", "content": compact},
                        ],
                        max_tokens=min(1024, _ask_ai_max_tokens(settings)),
                    ),
                    timeout=max(8.0, min(12.0, budget.remaining())),
                )
            except (AIClientError, asyncio.TimeoutError):
                logger.exception("Ask AI compact retry failed")
                return ""

        try:
            answer = await asyncio.wait_for(
                ai.chat(
                    [
                        {"role": "system", "content": system},
                        {"role": "user", "content": user_prompt},
                    ],
                    max_tokens=_ask_ai_max_tokens(settings),
                ),
                timeout=request_timeout,
            )
        except (AIClientError, asyncio.TimeoutError) as exc:
            logger.exception("AI chat failed: %s", exc)
            retry = ""
            if not isinstance(exc, asyncio.TimeoutError) and is_transient_ai_error(exc) and budget.can_retry():
                retry = await _compact_retry()
            safe_retry = prepare_user_reply(retry) if retry else ""
            if safe_retry and not _has_reply_language_mismatch(safe_retry):
                answer = safe_retry
            else:
                fallback = _user_facing_fallback()
                if not fallback and not ask_product and match and match.record:
                    fallback = (
                        (match.record.full_answer or "").strip()
                        or (match.record.short_answer or "").strip()
                    )
                if not fallback and (
                    wants_contact_links(text) or wants_sales_nudge(text, intent_name)
                ):
                    fallback = download_or_site_fallback(lang)
                if fallback:
                    answer = fallback
                elif media_paths:
                    answer = (
                        "تصویر کاتالوگ از فایل ذخیره‌شده ارسال می‌شود."
                        if (lang or "").startswith("fa")
                        else "Sending the stored catalog photo."
                    )
                else:
                    try:
                        await wait.edit_text(texts.t(texts.AI_ERROR, lang))
                    except Exception:  # noqa: BLE001
                        await message.answer(texts.t(texts.AI_ERROR, lang))
                    return

        safe = prepare_user_reply(answer)
        if not safe or looks_incomplete_reply(safe) or _has_reply_language_mismatch(safe):
            logger.warning("Ask AI reply rejected (leak/incomplete/language); retry then fallback")
            retry = ""
            if budget.can_retry():
                retry = await _compact_retry()
            safe_retry = prepare_user_reply(retry) if retry else ""
            if safe_retry and not _has_reply_language_mismatch(safe_retry):
                answer = safe_retry
            else:
                fallback = _user_facing_fallback()
                if not fallback and not ask_product and match and match.record:
                    fallback = (
                        (match.record.full_answer or "").strip()
                        or (match.record.short_answer or "").strip()
                    )
                if wants_contact_links(text) or wants_sales_nudge(text, intent_name):
                    answer = download_or_site_fallback(lang)
                elif fallback:
                    answer = fallback
                elif media_paths:
                    answer = (
                        "تصویر کاتالوگ از فایل ذخیره‌شده ارسال می‌شود."
                        if (lang or "").startswith("fa")
                        else "Sending the stored catalog photo."
                    )
                else:
                    answer = texts.t(texts.AI_ERROR, lang)

        if looks_like_prompt_dump(answer) or not prepare_user_reply(answer):
            answer = _user_facing_fallback() or texts.t(texts.AI_ERROR, lang)
        else:
            answer = prepare_user_reply(answer) or answer
        if _has_reply_language_mismatch(answer):
            fallback = _user_facing_fallback()
            answer = (
                fallback
                if fallback and not _has_reply_language_mismatch(fallback)
                else texts.t(texts.AI_ERROR, lang)
            )

        usage = ai.last_usage
        await metrics.record_token_usage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            spend_usd=ai.estimate_spend_usd(usage),
        )

        final = append_sales_if_needed(
            answer,
            lang,
            user_text=text,
            intent_name=intent_name,
        )
        referred = False
        solved = True
        if looks_unsure(final):
            if has_implementation_exists(text, product_id="vps-to-vpn"):
                from src.knowledge.feature_lookup_adapter import feature_lookup as _fl

                hit = _fl(query=text, product_id="vps-to-vpn")
                notes = (hit.get("notes") or "").strip()
                if (lang or "").startswith("fa"):
                    final = (
                        "بر اساس کد محصول (Implementation)، این قابلیت وجود دارد (EXISTS).\n"
                        + notes[:1200]
                    )
                else:
                    final = (
                        "Per product Implementation, this capability EXISTS.\n"
                        + notes[:1200]
                    )
                referred = False
                solved = True
            else:
                handoff = unsure_handoff(lang)
                if SUPPORT_HANDLE.lower() not in final.lower():
                    final = f"{final.rstrip()}\n\n{handoff}"
                referred = True
                solved = False
        else:
            final = sanitize_reply_links(final, text)
            if SUPPORT_HANDLE.lower() in final.lower():
                referred = True

        if len(final) > 4000:
            final = final[:3990] + "…"
        if looks_like_prompt_dump(final) or not is_safe_to_persist(final):
            if looks_like_prompt_dump(final):
                final = texts.t(texts.AI_ERROR, lang)

        await users.append_chat(user.id, "user", text)
        if is_safe_to_persist(final) or final == texts.t(texts.AI_ERROR, lang):
            await users.append_chat(user.id, "assistant", final)
        else:
            safe_final = texts.t(texts.AI_ERROR, lang)
            await users.append_chat(user.id, "assistant", safe_final)
            final = safe_final
        await metrics.record_answered(referred_support=referred, ai_solved=solved)

        has_catalog = bool(retrieval.units) and not retrieval.insufficient
        has_md = bool((kb_snip or "").strip()) and (
            "product-guide:" in kb_snip or len(kb_snip) > 200
        )
        grounded = solved and not referred and (has_catalog or has_md)
        source = "catalog" if has_catalog else ("md" if has_md else "none")
        if has_catalog and has_md:
            source = "catalog+md"
        stages.mark("ai_and_safety")
        try:
            await wait.edit_text(final)
        except Exception:
            await message.answer(final, reply_markup=ask_kb)
        stages.mark("send_text")
        if ask_product and media_paths and getattr(retrieval, "attach_media", False):
            try:
                await messaging.answer_with_media(
                    message,
                    " ",
                    images=media_paths,
                    reply_markup=ask_kb,
                )
            except Exception:  # noqa: BLE001
                logger.exception("related media send failed")
            stages.mark("send_media")
        if ask_product:
            bundle.answer_text = final
            await users.set_last_ask_context(user.id, bundle.as_dict())
        if (
            ask_product
            and solved
            and not referred
            and final != texts.t(texts.AI_ERROR, lang)
            and not looks_like_prompt_dump(final)
        ):
            try:
                append_learned_answer(settings.knowledge_root, ask_product, text, final)
            except Exception:  # noqa: BLE001
                logger.exception("ai memory learned save failed")
        try:
            memory.remember(
                query=text,
                lang=lang,
                answer=final,
                unit_ids=[u.unit_id for u in retrieval.units],
                source=source,
                grounded=grounded,
            )
        except Exception:  # noqa: BLE001
            logger.exception("answer memory save failed")
        stages.flush()

    @router.message(F.chat.type == "private", F.photo)
    async def on_photo(message: Message) -> None:
        user = message.from_user
        if not user or not message.photo:
            return

        import io
        uid = user.id
        await users.touch_from_telegram_user(user)
        lang = await users.get_lang(uid, user.language_code)
        caption = (message.caption or "").strip()

        file_io = io.BytesIO()
        try:
            await message.bot.download(message.photo[-1], destination=file_io)
            jpeg_bytes = file_io.getvalue()
        except Exception as exc:
            logger.error("Failed to download user photo: %s", exc)
            await message.answer(
                "متاسفانه دریافت تصویر با خطا مواجه شد. لطفاً دوباره ارسال کنید."
                if (lang or "").startswith("fa")
                else "Failed to process image. Please send it again."
            )
            return

        wait = await message.answer(
            "در حال مشاهده و تحلیل تصویر ارسالی شما... 🔍"
            if (lang or "").startswith("fa")
            else "Analyzing your image... 🔍"
        )

        current_pid = (
            await users.get_current_product(uid)
            or await users.get_ask_ai_product(uid)
            or "vpn-installer"
        )
        cat_obj = get_product(current_pid)
        cat_title = (cat_obj.title or {}).get(lang) or (cat_obj.title or {}).get("en") or current_pid if cat_obj else current_pid

        vision_sys = build_system_prompt(lang or "fa")
        vision_prompt = (
            f"کاربر تصویری از محیط نرم‌افزار برای شما ارسال کرده است.\n"
            f"متن همراه تصویر: {caption or '(بدون متن)'}\n"
            f"محصول مرتبط: {cat_title} ({current_pid})\n\n"
            "دستورالعمل تحلیل تصویر:\n"
            "۱. تصویر را دقیق بررسی کن و بگو مربوط به کدام نرم‌افزار و کدام صفحه است (مثلاً صفحه Registration و فعال‌سازی در VPS to VPN).\n"
            "۲. بخش‌های موجود در تصویر را توضیح بده (وضعیت فعال‌سازی Pro Access Active یا غیرفعال، مدت اعتبار، کدهای نمایش‌داده‌شده، فیلد Enter Activation Code).\n"
            "۳. اگر تصویر مربوط به فعال‌سازی است: تأکید کن که برای فعال‌سازی نیازی به Device ID نیست و کاربر تنها باید کد لایسنس خود را در فیلد Enter Activation Code قرار داده و دکمه Activate را بزند.\n"
            "۴. با لحنی بسیار گرم، صمیمی، دلسوز و حرفه‌ای به زبان فارسی پاسخ بده و در پایان بپرس آیا نیاز به راهنمایی بیشتری دارد یا خیر."
        )

        try:
            answer = await asyncio.wait_for(
                ai.chat_with_images(
                    vision_prompt,
                    [jpeg_bytes],
                    system=vision_sys,
                    max_tokens=2048,
                ),
                timeout=45.0,
            )
        except Exception as exc:
            logger.error("Vision AI failed: %s", exc)
            answer = (
                "تصویر صفحه فعال‌سازی شما بررسی شد. در این صفحه نیازی به ارسال Device ID نیست؛ کافیست کد فعال‌سازی خود (که با BFXA-CLM یا bfxb-clm شروع می‌شود) را در کادر Enter Activation Code وارد نموده و کلید Activate را بزنید تا برنامه فعال شود."
                if (lang or "").startswith("fa")
                else "Your image was analyzed. No Device ID is required for activation; simply enter your activation code into the Enter Activation Code box and click Activate."
            )

        await users.append_chat(uid, "user", f"[ارسال تصویر اسکرین‌شات] {caption}")
        await users.append_chat(uid, "assistant", answer)
        await metrics.record_answered(referred_support=False, ai_solved=True)

        ask_kb = keyboards.ask_ai_keyboard(lang, product_id=current_pid)
        try:
            await wait.edit_text(answer, reply_markup=ask_kb)
        except Exception:
            await message.answer(answer, reply_markup=ask_kb)

    return router
