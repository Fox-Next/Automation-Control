[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control — by Fox Next</h1>

<p align="center">
  <strong>8-Agent AI Orchestration Platform, Unified Local-First Desktop App &amp; Open-Source Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/">Official Website</a> •
  <a href="https://foxnext.net/en/download.html">Download Windows App</a> •
  <a href="https://foxnext.online/en/">Cloud Control Panel</a> •
  <a href="ARCHITECTURE.md">Architecture</a> •
  <a href="SECURITY.md">Security</a>
</p>

---

## 1. Overview

**Automation Control** (built by **Fox Next**) coordinates **8 specialized AI agents** across customer sales, multilingual technical support, Linux DevOps monitoring, financial verification, omnichannel social publishing, and creative audio/video production.

This public repository distributes:
- The sanitized, open-source **Smart Support Bot** runtime (`smart-support-bot/src/`) extracted from live production services.
- One-line installation automation for **Linux VPS** (`install.sh`) and **Windows Local ComfyUI** (`scripts/setup-comfyui.ps1`).
- Architectural, security, and ethical governance guides (`ARCHITECTURE.md`, `SECURITY.md`, `CODE_OF_ETHICS.md`).

> Official Desktop installers (`.exe`) are published exclusively on the verified download page: [foxnext.net/en/download.html](https://foxnext.net/en/download.html).

---

## 2. Core Capabilities

- **8-Agent Coordinated Team:** Orchestrator dispatcher, knowledge catalog sync, sales advisor, multi-platform technical support, Linux platform engineer, treasury verification, omnichannel publisher, and creative media director.
- **Two-Way Global Voice:** Continuous multi-language speech dictation, clean filler-free post-processing, ordered agent audio queue, hands-free silence detection, and instant barge-in interrupt.
- **Web Search & Anti-SSRF Fetch:** Controlled web search (up to 10 results) and network-safe webpage extraction blocking private/loopback/metadata IPs.
- **Secure Desktop Bridge & `Chat-to-Config`:** Encrypted inline credential forms inside chat that write straight to your encrypted Vault (`[REDACTED_SECRET]` pre-LLM masking) plus SSH-guarded bridge execution for platform operations.
- **Unified Desktop App (`Local-First` + `ComfyUI`):** Run private Bring-Your-Own-Key (BYOK) models and local GPU image/video generation offline with seamless `.fnbackup` workspace portability.

---

## 3. Transparent Plans & Editions

| Plan | Price | Active Agents | Key Highlights |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 Agents** | Daily & monthly token allowance, +48h welcome bonus (verified email), 1 social channel (Telegram/Instagram), 1 catalog, 20 MB storage (7-day temp TTL), 7 scheduled posts/week, 20 local ComfyUI outputs/month |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 Agents** | Expanded monthly tokens, 10 social channels & catalogs, 200 MB storage, Cloud Media API enabled, annual monthly-tranche release + up to 3-month rollover |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 Agents** | High-capacity monthly token allowance, full omnichannel + Cloud Media automation, up to 3-month unused rollover |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 Agents** | Maximum Cloud throughput for teams & high-frequency campaigns, Cloud Media APIs, up to 3-month rollover |
| **Lifetime** | **`$49`** (one-time) | **8 Agents** | **1 transferable active installation** (Windows Desktop **or** Linux VPS + Smart Support Bot), 48h trial, full BYOK endpoints, one-click encrypted `.fnbackup` migration |

Manage your subscription or launch instantly at [foxnext.online/en/](https://foxnext.online/en/).

---

## 4. Quick Installation

### Option A — Unified Windows Desktop App (`Local-First` + `ComfyUI`)

1. Download the official Windows package from [foxnext.net/en/download.html](https://foxnext.net/en/download.html).
2. *(Optional)* Install & connect local **ComfyUI** media rendering with one PowerShell command:

```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
```

### Option B — Linux VPS One-Line Install (`Smart Support Bot`)

```bash
curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | bash
```

Then configure `/opt/smart-support/.env` (see `.env.example`, including `TELEGRAM_BOT_TOKEN` and `CONTROL_PANEL_URL`) and start the `foxnext-smart-support` systemd service.

---

## 5. Control Panel Integration (`panel_conversation_hook.py`)

`smart-support-bot/src/panel_conversation_hook.py` connects Telegram support/sales sessions cleanly to any Control Panel instance solely via environment configuration:

- `CONTROL_PANEL_URL`: Target Control Panel HTTP base URL (no hardcoded server IPs or private domains).
- `CONTROL_PANEL_TOKEN`: Optional bearer token for authenticated webhook relays.
- `CONTROL_PANEL_ROOT`: Optional local filesystem path for co-located deployments.

---

## 6. Repository Structure

```text
Automation-Control/
├── assets/
│   └── foxnext-logo.png
├── scripts/
│   └── setup-comfyui.ps1
├── smart-support-bot/
│   ├── requirements.txt
│   └── src/
│       └── panel_conversation_hook.py
├── .env.example
├── .gitignore
├── ARCHITECTURE.md
├── CODE_OF_ETHICS.md
├── LICENSE
├── SECURITY.md
├── install.sh
└── README*.md
```

---

## 7. Security, Ethics & License

- Vulnerability disclosure & Vault isolation: [SECURITY.md](SECURITY.md)
- Responsible AI & anti-abuse principles: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- Licensed under the [MIT License](LICENSE) — Copyright © 2026 **Fox Next**.
