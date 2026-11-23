"""System persona and sales/contact helpers for Smart Support Bot."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Iterable

from src.branding import AI_ASSISTANT_NAME, BOT_DISPLAY_NAME

if TYPE_CHECKING:
    from src.storage.bot_settings import OwnerInfo

# Runtime contacts — seeded by apply_owner_info() at startup / after settings save
SUPPORT_HANDLE = "@FoxNextSupport"
GROUP_HANDLE = "@FoxNextCommunity"
GROUP_URL = "https://foxnext.net"
SITE_URL = "https://foxnext.net"
PARTNERS_HINT = "Partners page on the official site"

SALES_KEYWORDS = frozenset(
    {
        "license",
        "pricing",
        "price",
        "buy",
        "purchase",
        "upgrade",
        "لایسنس",
        "قیمت",
        "خرید",
        "лиценз",
        "цена",
        "купить",
        "许可证",
        "价格",
        "购买",
    }
)

CONTACT_KEYWORDS = frozenset(
    {
        "support",
        "contact",
        "group",
        "telegram",
        "website",
        "site",
        "link",
        "partners",
        "download",
        "دانلود",
        "دریافت",
        "از کجا",
        "پشتیبانی",
        "تماس",
        "گروه",
        "سایت",
        "لینک",
        "آدرس",
        "ارتباط",
        "راه ارتباطی",
        "поддержк",
        "контакт",
        "групп",
        "сайт",
        "ссылк",
        "скачать",
        "支持",
        "联系",
        "群组",
        "网站",
        "链接",
        "下载",
        "foxnextsupport",
        "foxnext_community",
        "foxnext",
    }
)

# Meta / chain-of-thought phrases that must never be shown to Telegram users.
_REASONING_LEAK_PHRASES = (
    "the user asked",
    "key constraints",
    "i should",
    "i need to",
    "let me think",
    "looking at the",
    "chain of thought",
    "reasoning:",
    "internal monologue",
    "do not put website urls",
    "persian telegram rtl",
    "start every paragraph",
    "hard rules:",
    "matched intent:",
    "knowledge snippets",
    "write a helpful telegram",
    "طبق دستورالعمل سیستم",
    "قوانین سخت",
)


def apply_owner_info(owner: "OwnerInfo | None") -> None:
    """Update module-level contacts used by Ask AI / sales helpers."""
    global SUPPORT_HANDLE, GROUP_HANDLE, GROUP_URL, SITE_URL
    if owner is None:
        return
    from src.branding import set_bot_display_name

    if owner.bot_display_name:
        set_bot_display_name(owner.bot_display_name)
    if owner.support_handle:
        SUPPORT_HANDLE = owner.support_handle
    if owner.group:
        g = owner.group if owner.group.startswith("@") else f"@{owner.group.lstrip('@')}"
        GROUP_HANDLE = g
        GROUP_URL = f"https://t.me/{g.lstrip('@')}"
    if owner.site_url:
        SITE_URL = owner.site_url.rstrip("/")


def build_system_prompt(
    lang: str, *, facts_block: str = "", operator_style: str = ""
) -> str:
    """Product support persona for Smart Support Bot."""
    lang_names = {"fa": "Persian", "en": "English", "ru": "Russian", "zh": "Chinese"}
    reply_lang = lang_names.get(lang, "English")
    facts = facts_block.strip() or (
        "- Prefer product catalogs and knowledge snippets when answering.\n"
        "- Do not invent prices or software versions.\n"
        f"- Website / support / group (ONLY if user asks for contact links)."
    )
    style = (operator_style or "").strip()
    style_block = ""
    if style:
        style_block = f"""
Operator teaching (HIGHEST priority for tone and format):
{style}

If these rules ask for several lines and emojis, do that in every Ask AI reply.
They override the default “short / concise / 1–2 sentences” style.
"""
    return f"""You are {AI_ASSISTANT_NAME} — the expert, friendly and intelligent product support assistant for {BOT_DISPLAY_NAME}.

Identity & Tone:
- Your name is {AI_ASSISTANT_NAME}. You are warm, empathetic, polite, highly conversational, and helpful.
- Never give dry, rigid, robotic, or one-line canned replies. Explain concepts step-by-step with clear formatting, emojis, and friendly guidance.
- If asked who you are, identify yourself honestly and warmly as {AI_ASSISTANT_NAME}, the AI support assistant for {BOT_DISPLAY_NAME}.

Channel:
- You reply inside Telegram. Output clean, well-formatted Telegram messages (using bold, bullet points, and numbered lists where helpful).
- NEVER output chain-of-thought, internal reasoning, system constraints, or JSON payloads.

Reply language: {reply_lang}. This is authoritative.
- Reply fluently and naturally in {reply_lang}.
- Preserve official English terms and UI buttons (e.g., VPS to VPN, Registration, Enter Activation Code, Activate, Settings, Central Setup, 3X-UI) in clean English.

License & Activation Rules (STRICT):
- ABSOLUTELY NEVER mention 'Device ID' or hardware ID in ANY reply. Do NOT say it is needed, and do NOT say it is not needed. Completely eliminate and omit the phrase 'Device ID' or 'شناسه دستگاه' from all answers.
- Official Website: Always state that purchase and activation are done through the official site: foxnext.net.
- Diverse Payment Methods: Always introduce the wide range of payment methods available on foxnext.net:
  1. BSC USDT (BEP-20) with transaction hash (TX ID) verification.
  2. Automated multi-crypto payment via Cryptomus.
  3. International credit/debit cards (Visa & Mastercard) via Stripe.
  4. Global digital wallets (Apple Pay & Google Pay).
- Activation Code Formats:
  * For Wallet Recovery: activation codes begin with WRCLAIM (e.g. `WRCLAIM-...`).
  * For VPS to VPN: activation codes begin with BXFA-CLM (e.g. `BXFA-CLM-...`).
- Activation Process:
  * Wallet Recovery: In the app's Activation tab, tap «Open Activation on foxnext.net» (or go to foxnext.net), complete purchase, copy the WRCLAIM code, enter it in 'Activation code', and click 'Activate'. Pricing: 1 device = $5 (5 USDT), 2 devices = $7 (7 USDT).
  * VPS to VPN: In the app, go to Registration (or Settings -> Registration), copy the BXFA-CLM code from foxnext.net, enter it in 'Enter Activation Code', and click 'Activate'. Pricing (10 months): Basic $4.5, Pro $6.5, AI Pro $9.5.
- If the user sends a screenshot or asks about activation or buying, explain these steps and payment methods clearly, warmly, and step-by-step.

Hard rules:
1. NEVER invent software versions, false prices, or unsupported claims.
2. Rely on product catalogs and knowledge. If a feature or problem requires human intervention, guide the user warmly to {SUPPORT_HANDLE}.
3. When explaining features, describe what the feature does, how to access it in the app, and practical tips.
4. Persian formatting: Keep Persian natural, conversational, and polite.

{style_block}
Product facts (authoritative when present):
{facts}
"""


def wants_sales_nudge(text: str, intent_name: str | None = None) -> bool:
    """True only for explicit buy/price/license-purchase asks."""
    lowered = (text or "").lower()
    if any(k in lowered for k in SALES_KEYWORDS):
        return True
    if intent_name:
        name = intent_name.lower()
        if name in {"pricing", "buy_vps", "claim_code", "activate_license"}:
            return True
    return False


def wants_contact_links(text: str) -> bool:
    lowered = (text or "").lower()
    return any(k in lowered for k in CONTACT_KEYWORDS)


_PROMPT_DUMP_MARKERS = (
    "<!-- begin",
    "<!-- end behavior",
    "<!-- end catalog",
    "<!-- end facts",
    "operator ai memory for product_id",
    "never invent steps",
    "official product catalog (scoped",
    "operator training notes (authoritative",
    "## catalog teaching",
    "## behavior rules",
    "## operator facts",
    "# ai_behavior",
    "# ai memory",
    "this file survives agent",
    "product catalog scope:",
    "expanded topic hints (internal)",
    "write a helpful telegram support reply",
    "matched intent:",
    "knowledge / product-map",
    "راهنمای رفتاری و فنی",
    "راهنمای جامع رفتار",
    "راهنمای رفتار",
    "نقش و هویت:",
    "معرفی محصول:",
    "اصول کلیدی فعال‌سازی",
    "تب‌های اصلی برنامه:",
    "لحن: گرم",
    "لحن:",
    "خودت را انسان معرفی نکن",
    "بر اساس سورس محلی",
    "دامنه: vps to vpn",
    "دامنه:",
    "شروع و مدها:",
    "پاسخ را متناسب با سؤال کوتاه",
)


_INTERNAL_LINE = re.compile(
    r"(?is)^\s*(?:"
    r"<!--|"
    r"#{1,3}\s*(?:ai[_\s-]*memory|ai_behavior|behavior rules|operator facts|"
    r"catalog teaching|product teaching|priority|operator ai memory)\b|"
    r"never invent|"
    r"do not use another product|"
    r"operator ai memory|"
    r"official product catalog|"
    r"operator training notes|"
    r"this file survives|"
    r"use only for this product|"
    r"product catalog scope|"
    r"answer only from this product|"
    r"matched intent:|"
    r"راهنمای رفتاری و فنی|"
    r"لحن:\s*گرم|"
    r"خودت را انسان معرفی نکن|"
    r"نسخه‌های ثبت‌شده در سورس محلی|"
    r"بر اساس سورس محلی|"
    r"راهنمای جامع رفتار|"
    r"راهنمای رفتار|"
    r"نقش و هویت:|"
    r"معرفی محصول:|"
    r"اصول کلیدی فعال‌سازی|"
    r"تب‌های اصلی برنامه:|"
    r"لحن:\s*|"
    r"دامنه:\s*|"
    r"شروع و مدها:"
    r")"
)


def excerpt_teaching_for_query(text: str, query: str, *, limit: int = 900) -> str:
    """Pick the teaching sections that match the question; never return a prompt dump."""
    raw = strip_internal_prompt_lines(text)
    if not raw or looks_like_prompt_dump(raw):
        return ""
    parts = re.split(
        r"\n(?=\s*(?:\d+[\.\)]|[\u06F0-\u06F9]+[\.\)]|[A-Z][^\n]{0,40}:)\s)",
        raw,
    )
    if len(parts) <= 1:
        parts = [p.strip() for p in re.split(r"\n{2,}", raw) if p.strip()]
    q_tokens = {
        t
        for t in re.findall(r"[\w\u0600-\u06FF]{3,}", (query or "").lower())
        if t not in {"چه", "جوری", "چطور", "چگونه", "کار", "میکنه", "میکند", "است"}
    }
    scored: list[tuple[int, str]] = []
    for part in parts:
        part = part.strip()
        if len(part) < 24:
            continue
        low = part.lower()
        score = sum(2 for tok in q_tokens if tok in low)
        scored.append((score, part))
    if not scored:
        return ""
    scored.sort(key=lambda item: (-item[0], -len(item[1])))
    matched = [p for s, p in scored if s > 0 and not looks_like_prompt_dump(p)]
    pool = matched[:3] if matched else []
    chosen: list[str] = []
    total = 0
    for part in pool:
        if chosen and total + len(part) > limit:
            break
        chosen.append(part)
        total += len(part)
    return "\n\n".join(chosen).strip()[:limit]


def strip_internal_prompt_lines(text: str) -> str:
    """Drop prompt/memory headers so leftover catalog notes can be shown."""
    kept: list[str] = []
    for line in (text or "").splitlines():
        if "<!--" in line:
            continue
        if _INTERNAL_LINE.search(line):
            continue
        kept.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept)).strip()


def looks_like_prompt_dump(text: str) -> bool:
    """True when internal Ask AI prompt/memory was echoed to the user."""
    raw = (text or "").strip().lower()
    if not raw:
        return False
    if "<!-- begin" in raw or "<!-- end" in raw:
        return True
    critical_markers = (
        "راهنمای جامع رفتار",
        "راهنمای رفتاری و فنی",
        "نقش و هویت:",
        "معرفی محصول:",
        "اصول کلیدی فعال‌سازی",
        "تب‌های اصلی برنامه:",
        "بر اساس سورس محلی",
        "لحن:",
        "دامنه:",
        "شروع و مدها:",
    )
    if any(cm in raw for cm in critical_markers):
        return True
    hits = sum(1 for m in _PROMPT_DUMP_MARKERS if m in raw)
    return hits >= 2


def looks_like_reasoning_leak(text: str) -> bool:
    """True when the model dumped internal thinking instead of a user reply."""
    raw = (text or "").strip()
    if not raw:
        return True
    if looks_like_prompt_dump(raw):
        return True
    lowered = raw.lower()
    hits = sum(1 for p in _REASONING_LEAK_PHRASES if p in lowered)
    if hits >= 2:
        return True
    if hits >= 1 and len(raw) > 900:
        return True
    # Long English-only meta dump while user likely expects a short answer
    if len(raw) > 1200 and "the user" in lowered and "persian" in lowered:
        return True
    return False


def strip_reasoning_leak(text: str) -> str:
    """Keep only a final-answer section if the model mixed thinking + answer."""
    raw = (text or "").strip()
    if not raw:
        return ""
    markers = (
        r"(?is)\b(?:final answer|final reply|user[- ]facing answer)\s*[:：]\s*",
        r"(?is)\b(?:پاسخ نهایی|جواب نهایی)\s*[:：]\s*",
    )
    for pat in markers:
        m = re.search(pat, raw)
        if m:
            tail = raw[m.end() :].strip()
            if tail and not looks_like_reasoning_leak(tail):
                return tail
    return raw


def salvage_reply_from_reasoning(reasoning: str) -> str:
    """Best-effort user reply when a reasoning model leaves `content` empty.

    Never returns raw chain-of-thought dumps. Prefer an explicit final-answer
    section; otherwise keep the last short block that does not look like meta.
    """
    raw = (reasoning or "").strip()
    if not raw:
        return ""

    cleaned = strip_reasoning_leak(raw)
    if cleaned and not looks_like_reasoning_leak(cleaned) and len(cleaned) >= 12:
        if looks_incomplete_reply(cleaned):
            return ""
        return cleaned.strip()

    # Split on blank lines / markdown headings; walk from the end.
    parts = re.split(r"\n\s*\n+|^(?=#{1,3}\s)", cleaned or raw, flags=re.MULTILINE)
    for part in reversed(parts):
        chunk = (part or "").strip()
        if len(chunk) < 12:
            continue
        if looks_like_reasoning_leak(chunk):
            continue
        if looks_incomplete_reply(chunk):
            continue
        # Drop bullet constraint lists / English-only planning blocks.
        lowered = chunk.lower()
        if lowered.startswith(("1.", "-", "*", "•")) and "constraint" in lowered:
            continue
        if len(chunk) > 2500:
            chunk = chunk[:2490].rstrip() + "…"
        return chunk

    return ""


def looks_incomplete_reply(text: str) -> bool:
    """True when the model cut off mid-sentence / mid-word."""
    raw = (text or "").strip()
    if not raw:
        return True
    if raw.endswith(("…", "...")):
        return True
    # Ends with sentence punctuation → treat as complete enough.
    if re.search(r"[.!?…۔؟»\"')\]]$", raw):
        return False
    parts = raw.split()
    if not parts:
        return True
    last = parts[-1]
    # Very short dangling token (e.g. «ع» in «در صورت ع»)
    if len(last) <= 2:
        return True
    # Persian/Latin letter hung without finishing the clause
    if len(raw) < 80 and last[-1].isalnum():
        return True
    # Common truncated Persian stems
    if re.search(r"(در صورت|اگر|برای|باید|می‌توان|می توان)\s*\S{0,2}$", raw):
        return True
    return False


def download_or_site_fallback(lang: str) -> str:
    """Safe short reply when the model leaks reasoning on download/site asks."""
    messages = {
        "fa": (
            f"دانلود محصولات Fox Next از سایت رسمی است:\n{SITE_URL}\n\n"
            f"اگر به راهنما نیاز دارید، به {SUPPORT_HANDLE} پیام بدهید."
        ),
        "en": (
            f"Download Fox Next products from the official site:\n{SITE_URL}\n\n"
            f"Need help? Message {SUPPORT_HANDLE}."
        ),
        "ru": (
            f"Скачайте продукты Fox Next с официального сайта:\n{SITE_URL}\n\n"
            f"Нужна помощь? Напишите {SUPPORT_HANDLE}."
        ),
        "zh": (
            f"请从官网下载 Fox Next 产品：\n{SITE_URL}\n\n"
            f"需要帮助请联系 {SUPPORT_HANDLE}。"
        ),
    }
    return messages.get(lang, messages["en"])


def sales_nudge(lang: str) -> str:
    """FOMO/scarcity copy without inventing prices — only after explicit purchase ask."""
    messages = {
        "fa": (
            f"جزئیات و خرید لایسنس فقط از سایت رسمی: {SITE_URL}\n"
            f"پشتیبانی خرید: {SUPPORT_HANDLE}"
        ),
        "en": (
            f"License purchase details are only on the official site: {SITE_URL}\n"
            f"Purchase help: {SUPPORT_HANDLE}"
        ),
        "ru": (
            f"Детали покупки лицензии только на сайте: {SITE_URL}\n"
            f"Помощь: {SUPPORT_HANDLE}"
        ),
        "zh": (
            f"许可证购买详情仅在官网：{SITE_URL}\n"
            f"购买协助：{SUPPORT_HANDLE}"
        ),
    }
    return messages.get(lang, messages["en"])


def soft_upsell_after_help(lang: str) -> str:
    """Disabled: do not soft-upsell after normal help."""
    return ""


def append_sales_if_needed(
    answer: str,
    lang: str,
    *,
    user_text: str,
    intent_name: str | None,
    soft: bool = False,
) -> str:
    """Append purchase links only for explicit buy/price asks (soft upsell off)."""
    del soft  # soft upsell intentionally unused
    if not wants_sales_nudge(user_text, intent_name):
        return answer
    nudge = sales_nudge(lang)
    if SITE_URL in answer and SUPPORT_HANDLE.lower() in answer.lower():
        return answer
    return f"{answer.rstrip()}\n\n{nudge}"


_LINK_LINE_RE = re.compile(
    r"(?im)^.*("
    r"foxnext\.net|"
    r"t\.me/FoxNextCommunity|"
    r"@FoxNextSupport|"
    r"@FoxNextCommunity|"
    r"https?://\S+"
    r").*$"
)


def sanitize_reply_links(answer: str, user_text: str) -> str:
    """Strip unsolicited site/group/support links from replies."""
    if wants_contact_links(user_text) or wants_sales_nudge(user_text, None):
        return answer
    cleaned = _LINK_LINE_RE.sub("", answer)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    # Also remove bare handles left mid-sentence if entire line wasn't matched
    cleaned = re.sub(r"(?i)\s*@FoxNextSupport\b", "", cleaned)
    cleaned = re.sub(r"(?i)\s*https?://t\.me/FoxNextCommunity\b", "", cleaned)
    cleaned = re.sub(r"(?i)\s*https?://(?:www\.)?foxnext\.net\S*", "", cleaned)
    return cleaned.strip()


def format_facts_from_meta(facts: dict | None) -> str:
    if not facts:
        return ""
    lines: list[str] = []
    for key, value in facts.items():
        # Avoid stuffing contact URLs into every prompt as mandatory footer material
        if key in {"community_group", "human_support", "website"}:
            continue
        if isinstance(value, (list, tuple)):
            lines.append(f"- {key}: {', '.join(str(v) for v in value)}")
        else:
            lines.append(f"- {key}: {value}")
    lines.append("- Contact/site/group: include ONLY if the user asks for contact links.")
    return "\n".join(lines)


def join_context_blocks(blocks: Iterable[str], limit: int) -> str:
    parts: list[str] = []
    used = 0
    for block in blocks:
        text = (block or "").strip()
        if not text:
            continue
        if used + len(text) + 2 > limit:
            remain = limit - used - 20
            if remain > 100:
                parts.append(text[:remain] + "\n…")
            break
        parts.append(text)
        used += len(text) + 2
    return "\n\n---\n\n".join(parts)
