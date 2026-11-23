# -*- coding: utf-8 -*-
"""Control panel conversation hook for Smart Support Bot.

Routes buy/support/sales conversation turns to the external Control Panel URL
configured strictly via ``CONTROL_PANEL_URL`` (or an optional local panel checkout
set via ``CONTROL_PANEL_ROOT``). Contains zero hardcoded hosts, IPs, or secrets.
"""
from __future__ import annotations

import json
import logging
import os
import sys
import urllib.request
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def _panel_url() -> str:
    return (os.environ.get("CONTROL_PANEL_URL") or "").strip().rstrip("/")


def _ensure_local_root() -> Path | None:
    raw = (os.environ.get("CONTROL_PANEL_ROOT") or "").strip()
    if not raw:
        return None
    root = Path(raw)
    if not (root / "services" / "conversation").is_dir():
        return None
    root_s = str(root)
    if root_s not in sys.path:
        sys.path.insert(0, root_s)
    return root


def _relay_post(endpoint: str, payload: dict[str, Any], timeout: float = 8.0) -> dict[str, Any] | None:
    base = _panel_url()
    if not base:
        return None
    url = f"{base}/{endpoint.lstrip('/')}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    token = (os.environ.get("CONTROL_PANEL_TOKEN") or "").strip()
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
        parsed = json.loads(raw)
        return parsed if isinstance(parsed, dict) else None
    except Exception as exc:  # noqa: BLE001
        logger.debug("control panel relay call skipped: %s", exc)
        return None


def handle_user_text(
    text: str,
    *,
    account_id: str,
    profile_lang: str = "fa",
    last_message_lang: str = "",
    source: str | None = None,
    channel: str = "telegram",
    chat_history: list | None = None,
    user_record: dict[str, Any] | None = None,
    prior_message_count: int | None = None,
) -> dict[str, Any]:
    root = _ensure_local_root()
    if root is not None:
        try:
            from adapters.support_bot.conversation import handle_support_message

            turn = handle_support_message(
                text,
                channel=channel,
                account_id=str(account_id),
                profile_lang=profile_lang,
                last_message_lang=last_message_lang,
                source=source,
                chat_history=chat_history,
                user_record=user_record,
                prior_message_count=prior_message_count,
            )
            return turn.as_dict()
        except Exception as exc:  # noqa: BLE001
            logger.warning("local conversation hook failed: %s", exc)
            return {"ok": False, "text": "", "reason": type(exc).__name__}

    if _panel_url():
        relayed = _relay_post(
            "/api/agent-relay/inbound",
            {
                "text": text,
                "account_id": str(account_id),
                "profile_lang": profile_lang,
                "last_message_lang": last_message_lang,
                "source": source,
                "channel": channel,
                "chat_history": chat_history or [],
            },
        )
        if relayed is not None:
            return relayed

    return {"ok": False, "text": "", "reason": "CONTROL_PANEL_URL not configured"}


def should_bypass_ask_ai(
    account_id: str,
    text: str = "",
    *,
    channel: str = "telegram",
    source: str | None = None,
) -> bool:
    """True -> Smart Support Bot chat must not emit Ask-AI-inactive errors."""
    root = _ensure_local_root()
    if root is not None:
        try:
            from adapters.support_bot.conversation import should_bypass_ask_ai as _impl

            return bool(
                _impl(
                    str(account_id),
                    text=text,
                    channel=channel,
                    source=source,
                )
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("ask-ai bypass check failed: %s", exc)
            return False
    return bool(_panel_url())


def end_conversation(account_id: str, *, channel: str = "telegram") -> None:
    root = _ensure_local_root()
    if root is not None:
        try:
            from adapters.support_bot.conversation import end_conversation as _impl

            _impl(str(account_id), channel=channel)
        except Exception as exc:  # noqa: BLE001
            logger.warning("end conversation failed: %s", exc)
        return
    if _panel_url():
        _relay_post(
            "/api/agent-relay/end",
            {"account_id": str(account_id), "channel": channel},
            timeout=3.0,
        )


def has_locked_session(account_id: str, *, channel: str = "telegram") -> bool:
    root = _ensure_local_root()
    if root is None:
        return False
    try:
        from adapters.support_bot.conversation import has_locked_session as _impl

        return bool(_impl(str(account_id), channel=channel))
    except Exception as exc:  # noqa: BLE001
        logger.warning("locked-session check failed: %s", exc)
        return False
