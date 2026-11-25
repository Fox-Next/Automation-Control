[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control v3.0.0 — by Fox Next</h1>

<p align="center">
  <strong>8-Agent AI Orchestration Platform, Unified Local-First Desktop Suite &amp; Open-Source Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/en/">Official Website</a> •
  <a href="https://foxnext.net/en/download.html">Download Page (foxnext.net)</a> •
  <a href="https://github.com/Fox-Next/Automation-Control/releases/latest">GitHub Releases (v3.0.0)</a> •
  <a href="https://foxnext.online/en/">Cloud Control Panel</a> •
  <a href="ARCHITECTURE.md">Architecture</a> •
  <a href="SECURITY.md">Security</a>
</p>

---

## 1. Overview & Official Releases

**Automation Control** (by **Fox Next**) orchestrates **8 specialized AI agents** for sales qualification, multi-platform technical support, Linux infrastructure operations, license & fulfillment verification, omnichannel marketing, and creative studio automation.

Official verified installers (`v3.0.0`) are published on **[GitHub Releases](https://github.com/Fox-Next/Automation-Control/releases/latest)** and **[foxnext.net/en/download.html](https://foxnext.net/en/download.html)** with full `SHA256SUMS.txt` verification:

| Package | Target | Description |
| :--- | :--- | :--- |
| **`AutomationControl.exe`** | Windows | Unified single desktop app (~29 MB) with Light `foxnext.online` UI, post-install email license routing (`Cloud`, `Self-Hosted VPS`, `Local Engine`), strict `connect_vps_strict` gate, Multi-GPU worker (`>= 6 GB VRAM`), and on-demand `ComfyUI` / `FFmpeg` setup |
| **`automation-control-linux.tar.gz`** | Linux VPS | Clean Self-Hosted runtime package auto-downloaded and verified by `install.sh` |
| **`SHA256SUMS.txt`** | All | Cryptographic `SHA-256` checksums for all official release packages |

---

## 2. Core Capabilities

- **8-Agent Team with Simple (`Grok Bot`) & Advanced Modes:** Streamlined 3-column chat-centric Simple Mode or full 6-tab Advanced Mode coordinating all 8 specialists.
- **Google OAuth & One Tap Sign-In:** Seamless browser authentication alongside email verification and unified multi-device workspace access across 10 languages.
- **Bidirectional Global Voice:** Continuous multi-language speech dictation, clean post-processing, ordered TTS playback queue, hands-free mode, and instant barge-in interrupt.
- **Two-Layer `Chat-First` DM & Comment Engine:** Ultra-efficient deterministic rule & AI pipeline for instant Instagram and Telegram responses.
- **3-Layer Token-Optimized Memory:** Automatic episodic compression, brand-brain grounding, and short-term context pruning for consistent, low-overhead agent replies.
- **Browserless `cPanel / SSH / SFTP` & Commerce Hub:** Direct server/website integration without headless browser overhead (with immediate cleanup of temporary credentials) plus unified Store, Inventory, and Finance workflows (with or without an external website).
- **Unified Single Windows App & Email License Auto-Routing:** Single frictionless `AutomationControl.exe` (~29 MB) with Light `foxnext.online` theme, post-install Email/Google license routing (Cloud / Local Engine / 3-Mode Picker), strict online Lifetime VPS License Gate, and on-demand `ComfyUI`/`FFmpeg` runtime download.
- **Dual-Slot Single-Active-Per-Platform Sessions (Web + Desktop):** Uniformly allows **1 active Web session + 1 active Desktop session** concurrently across all plans (`Free` through `Lifetime`); logging into a second Web browser or second Desktop device automatically replaces only that platform's previous session without interrupting the other platform.
- **Multi-GPU `CUDA`, `ROCm` & `DirectML` Acceleration:** Automatic Windows Multi-GPU enumeration (`NVIDIA` → `CUDA`/`NVENC`, `AMD Radeon` → `ROCm`/`DirectML` + `AMF`, `Intel Arc` → `DirectML`/`QSV`, `>= 6 GB VRAM`) plus manual GPU selector.
- **Settings → Tools & MCP Management (`find_tools` & `register_tool_or_mcp`):** All 8 core agents autonomously discover, register, and invoke tools; Desktop & Self-Hosted modes unlock custom MCP servers while Shared Cloud restricts registrations to tenant-isolated SSRF-safe `https://` API/webhook tools (32 KB output cap).
- **2-Layer AI Inheritance, `Unlimited` Max Tokens & Localized 8-Agent Prompts (`AI & Models` vs `Superadmin Hub`):** Regular Cloud subscribers save isolated per-agent BYOK overrides cleanly without overwriting global defaults or viewing Superadmin keys/budgets; all 8 core agents use brand-neutral placeholders localized to the active panel language, while `Max Tokens` defaults to `0` (`Unlimited` — omitting hard caps from LLM payloads).
- **Superadmin Governance Hierarchy, Live `Annual USD` & `Storage MB` Quotas, `$1–$10` Top-Up & Audit Log:** Primary vs. Secondary Superadmin RBAC (`Email OTP + Reason` gating on sensitive actions, `#1` pinned undeletable Primary row), live `Online Now` KPI, 10-row pagination/sorting, dynamic `$1–$10` Dollar Top-Up, live `Plans & Pricing` (`Monthly USD`, `Annual USD`, `Tokens / mo`, `Storage MB`) directly synchronizing `HTTP 413` upload caps and `/api/public/pricing` without restarts, Tabular Audit Log (including `update_pricing_policy`, zero raw keys), 2-row Campaign Mode (`Publish Immediately` + Gregorian `datetime-local` pickers), full-width editable 5 Cloud Pools, and 10-language Connection Test & Live Diagnostics modals.
- **Profile Permissions, 2FA Password Rotation & Self-Service Danger Zone:** Every user inspects exact active `plan_permissions`; Email/Password accounts rotate passwords via Current Password + Email OTP + Turnstile/Captcha, and Cloud subscribers can self-delete their accounts from the Profile Danger Zone via Email OTP (immediately revoking Web & Desktop sessions).
- **Desktop `Local-First` & Local `MCP` / `Skills`:** Isolated local `Plugins / Skills / MCP` ecosystem unlocked on Desktop & Linux (`Local-First` workspace Vault, `.fnbackup` migration, `BYOK` model routing, and `6 GB VRAM` local `ComfyUI` rendering).

---

## 3. Plans & Editions

| Plan | Price | Active Agents | Key Highlights |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 Agents** | Starter daily/monthly token allowance + 48h welcome bonus (verified email), 1 social channel (Telegram/Instagram), 1 catalog, 20 MB temp storage, local `ComfyUI` |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 Agents** | Expanded monthly quota, 10 social channels & catalogs, 200 MB storage, Cloud Media API enabled, annual monthly-tranche release + up to 3-month rollover |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 Agents** | High-capacity monthly token allowance, full omnichannel + Cloud Media automation, up to 3-month rollover |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 Agents** | Maximum cloud throughput for teams & high-volume campaigns, full Cloud Media APIs + up to 3-month rollover |
| **Lifetime** | **`$49`** (one-time) | **8 Agents** | **1 transferable active installation** (unified `AutomationControl.exe` in `Local Engine` mode on Windows **or** Linux VPS + Smart Support Bot), 48h trial, full `BYOK`, `.fnbackup` portability |

---

## 4. One-Line Installation Commands

### 1) Windows Desktop — Automation Control (`PowerShell`)
```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.ps1 | iex
```

### 2) Windows — Local ComfyUI GPU Worker (`PowerShell` / `scripts/Setup-ComfyUI.bat`)
```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
```

### 3) Windows — Smart Support Bot (`PowerShell`)
```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/install-smart-support-bot.ps1 | iex
```

### 4) Linux VPS — Automation Control + Smart Support Bot (`bash`)
```bash
curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | sudo bash
```

---

## 5. Control Panel Integration (`panel_conversation_hook.py`)

`smart-support-bot/src/panel_conversation_hook.py` connects Telegram sessions cleanly via environment variables only (`CONTROL_PANEL_URL`, `CONTROL_PANEL_TOKEN`, `CONTROL_PANEL_ROOT`).

---

## 6. Repository Structure

```text
Automation-Control/
├── assets/
│   └── foxnext-logo.png
├── scripts/
│   ├── Setup-ComfyUI.bat
│   ├── install-smart-support-bot.ps1
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
├── install.ps1
├── install.sh
└── README*.md
```

---

## 7. Security, Ethics & License

- Security & Vault policy: [SECURITY.md](SECURITY.md)
- Ethical AI principles: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- Architecture guide: [ARCHITECTURE.md](ARCHITECTURE.md)
- Licensed under [MIT License](LICENSE) — Copyright © 2026 **Fox Next**.
