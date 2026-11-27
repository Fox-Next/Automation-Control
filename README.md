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
- **Decluttered Chat Bar, Meeting Room Live Voice & Collapsible Swarm Table:** Clean header organizing actions into 3 localized RTL/LTR dropdowns (`Tools & Chat`, `Quick Setup`, `Ready Playbooks`), minimal icon-only composers with an animated 4-bar dictation equalizer (populating input without auto-sending), and an immersive green-mic Live Voice Mode in both Command Center and `Agents' meeting room` centering the animated robot mascot over a blurred backdrop with glowing blue `#38bdf8` eye-equalizer modulation (`AnalyserNode` + Web Audio fallback) and `Escape`/Exit dismissal preserving the full transcript, paired with a collapsed-by-default 10/page paginated Unified Swarm Accordion (newest-first, multi-select delete, and `Send to Chat`).
- **Two-Layer `Chat-First` DM & Comment Engine:** Ultra-efficient deterministic rule & AI pipeline for instant Instagram and Telegram responses.
- **3-Layer Token-Optimized Memory:** Automatic episodic compression, brand-brain grounding, and short-term context pruning for consistent, low-overhead agent replies.
- **Browserless `cPanel / SSH / SFTP` & Commerce Hub:** Direct server/website integration without headless browser overhead (with immediate cleanup of temporary credentials) plus unified Store, Inventory, and Finance workflows (with or without an external website).
- **Unified Single Windows App & Email License Auto-Routing:** Single frictionless `AutomationControl.exe` (~29 MB) with Light `foxnext.online` theme, post-install Email/Google license routing (Cloud / Local Engine / 3-Mode Picker), strict online Lifetime VPS License Gate, and on-demand `ComfyUI`/`FFmpeg` runtime download.
- **Dual-Slot Single-Active-Per-Platform Sessions (Web + Desktop):** Uniformly allows **1 active Web session + 1 active Desktop session** concurrently across all plans (`Free` through `Lifetime`); logging into a second Web browser or second Desktop device automatically replaces only that platform's previous session without interrupting the other platform.
- **Multi-GPU `CUDA`, `ROCm` & `DirectML` Acceleration:** Automatic Windows Multi-GPU enumeration (`NVIDIA` → `CUDA`/`NVENC`, `AMD Radeon` → `ROCm`/`DirectML` + `AMF`, `Intel Arc` → `DirectML`/`QSV`, `>= 6 GB VRAM`) plus manual GPU selector.
- **Settings → Tools & MCP Management (`find_tools` & `register_tool_or_mcp`):** All 8 core agents autonomously discover, register, and invoke tools; Desktop & Self-Hosted modes unlock custom MCP servers while Shared Cloud restricts registrations to tenant-isolated SSRF-safe `https://` API/webhook tools (32 KB output cap).
- **2-Layer AI Inheritance, Custom Agent BYOK Quota Exemption & Free Google Key `?` Guide:** Create custom agents in clean empty forms without losing workspace access, store personal keys encrypted (`enc:v1:`) with optional aistudio.google.com setup guidance, and run BYOK agents directly with **0 Cloud token quota deduction** across Chat, Meeting Room, and Creative Studio; all 8 core agents ship brand-neutral, 10-language localized directives editable inside a multi-line modal, `Max Tokens` defaults to `0` (`Unlimited`), and default visual palette uses the `Studio` (`dark-photo`) theme.
- **Zero-Flash 10-Language UI, Google Profile Avatar & 16 Contextual `?` Help Tooltips:** Clean English `<html dir="ltr" lang="en">` base markup with synchronous `<head>` pre-paint locale resolution, debounced DOM observer locking (`window.__bfI18nTranslating`), circular Google OAuth avatar rendering in the header & dropdown, localized right-click Command Center actions, and interactive `?` help buttons across all 6 workspace tabs, modals, and 7 settings panes.
- **ChatGPT-Style Daily, Weekly & Monthly Quota Allowances + Read-Only Finance Hub:** Superadmin-configurable daily & weekly plan caps (`daily_token_cap`, `weekly_token_cap`) alongside monthly credit & live `storage_mb`, with automated UTC daily & Monday weekly resets, countdown usage bars (`%` & `Resets in ...`, zero raw token exposure) inside the Dashboard card, polite `HTTP 429` upgrade notices, and strictly read-only incoming wallet/payment monitoring.
- **Superadmin Governance Hierarchy, Live `Annual USD` & `Storage MB` Quotas, `$1–$10` Top-Up & Audit Log:** Primary vs. Secondary Superadmin RBAC (`Email OTP + Reason` gating on sensitive actions, `#1` pinned undeletable Primary row), live `Online Now` KPI, 10-row pagination/sorting, dynamic `$1–$10` Dollar Top-Up, live `Plans & Pricing` (`Monthly USD`, `Annual USD`, `Daily Cap`, `Weekly Cap`, `Tokens / mo`, `Storage MB`) directly synchronizing `HTTP 413` upload caps and `/api/public/pricing` without restarts, Tabular Audit Log (including `update_pricing_policy`, zero raw keys), 2-row Campaign Mode (`Publish Immediately` + Gregorian `datetime-local` pickers), full-width editable 5 Cloud Pools, and 10-language Connection Test & Live Diagnostics modals.
- **Profile Permissions, Permanent Chat Clear & Immediate GDPR Danger Zone Purge:** Every user inspects exact active `plan_permissions` and rotates passwords via Current Password + Email OTP + Turnstile/Captcha; clearing an agent chat permanently deletes thread & legacy history files on disk and local cache; and confirmed self-deletion in `#profileDangerZoneCard` (via Email OTP) immediately revokes Web & Desktop sessions and purges the user's tenant workspace directory (`shutil.rmtree`) while preserving anti-abuse billing integrity.
- **Interactive Spotlight Workflow Graph, Unconfigured Gateway Lock, Mobile Fallback & Meta Cross-Posting (`∞ Meta`):** Subtle resting edges (`0.10` opacity) expand on hover/click into animated flow highlights with unrelated nodes dimmed (`0.28`) and collision-avoiding edge labels positioned cleanly above cards across 8 dedicated social output gateways (`Telegram`, `Instagram`, `Facebook`, `WhatsApp`, `YouTube`, `LinkedIn`, `X`, `Reddit`) and dynamic Brand Brain websites; unconfigured gateways reject toggles with a direct `Settings → Social Media` shortcut and `HTTP 400 gateway_not_configured`, mobile viewports (`<= 768px`) display clean bottom status cards only, and enabling `Meta Accounts Center Cross-Posting` displays `∞ Meta` SVG badges while dispatching publish calls only through the chosen Primary Meta Publisher (keeping comments/DMs 100% independent).
- **Mobile 70% Drawer, UUID Reply Quotes, Central `FileRegistry` & Range Media Preview:** Responsive mobile (`<= 768px`) 70%-width navigation & agent drawer, server-generated message `UUID` reply jumping, strict tenant-isolated `FileRegistry` with SVG script sanitization, and byte-range (`HTTP 206`) audio/video/image preview modal (`media_preview.js`).
- **Unified `StorageManager` (`Google Drive drive.file`, Cloudflare R2 & Local) + Safe Lifecycle:** Direct pluggable storage transfers, least-privilege `drive.file` OAuth vaulting (`enc:v1:`), format optimization policies, and automated publish-guarded storage cleanup & retention reconciliation.
- **4-Layer Hybrid `MemoryManager` & Editable `Timeline Manifest` Pipeline:** Tenant/project-isolated `SQLite FTS5` + 64-dim vector memory with prompt-injection sanitization, secret-blocking (`HTTP 422`), contradiction version history, and editable multi-scene video timelines (`style_bible` continuity, single-scene regeneration, Cloud CPU Shield `queued_for_worker`, and `ffprobe`/`blackdetect` QA).
- **Google One Tap, Mandatory Terms Gate, Aikido Security Headers & Self-Hosted Fonts:** Active `GOOGLE_CLIENT_ID` integration for `/login` Google One Tap + cross-origin CORS (`foxnext.online` & `app.foxnext.online`), one-time SQLite `terms_accepted_at` enforcement (`HTTP 403 terms_not_accepted` until `#modalMandatoryTermsGate`), `HSTS` + `X-Frame-Options: DENY` + strict CSP headers, and 35 locally hosted `.woff2` font files with zero external CDN requests.
- **Rolling 5-Hour Quota Cap, 12-Field `Cloud Media Pool` & Live FX Rate:** Superadmin `Cloud Media Pool` (`span 2`, 3×4 Image/Audio/Video provider/model/URL/key fields with Fernet encryption wired to `HybridComputeRouter`), aligned single-row pool card headers, chat-window **5-Hour Allowance** enforcement with reset countdowns (zero raw tokens exposed), and live FX conversion (`275,000` Toman/USD default).
- **High-Concurrency Omnichannel Commerce (`70+` Concurrent Customers), Universal Receipt OCR & End-to-End Closure:** Per-tenant isolated SQLite `WAL` conversation engine (`workspaces/{tenant_id}/conversations/sessions.db`, composite `tenant_id:channel:account_id:customer_id` key, `168h` 7-day continuity across Telegram, Instagram, WhatsApp, and Facebook) verified under `70+` concurrent customer threads with zero lock contention; multimodal Vision OCR & strict read-only verification across Crypto (`BEP-20`, `TRC-20`, `TON`) and International gateways (`Dodo Payments`, `Stripe`, `PayPal`, `Visa`/`Mastercard` HTTP `GET` only, strictly filtered to connected gateways with zero outgoing transfers); human-like `Brand Brain` `Comment-to-DM`; and automated physical (shipping + 10-digit postal code) & digital (`FulfillmentService` auto-license) order closure.
- **Shahla Pro Creative Studio (`bf_creative`, 7 Authorized Tools):** Grants web/brand palette lookup (`fetch_webpage`, `web_search`), tenant-owned reference & product compositing (`edit_reference_image` with `FileRegistry` `HTTP 403` guard), vector-crisp RTL/LTR typography & logo banners (`render_typography_overlay` via `arabic-reshaper`, `python-bidi`, and `Pillow` with zero garbled AI text), 1-click multi-aspect export (`export_multi_aspect` for `9:16`, `1:1`, and `16:9`), timed `.srt`/`.ass` captions (`generate_synced_subtitles` preserving Cloud CPU Shield worker queueing), and pre-delivery Visual Self-QA (`run_visual_self_qa` strictly capped at `<= 1` retry) wired into `/api/creative/pro/*` and all 10 UI languages.
- **Mobile Simple Mode Lock, Portaled Header Popover, Real Bot Probe & Inline Meta Cross-Posting:** Mobile viewports (`<= 768px`) lock cleanly to `Simple Mode` with a 3-part `70vw` drawer footer (`#mobileDrawerProfileFooter` + 3-tab `#mobileSettingsModal` for `%`-only quotas/Logout/GDPR Delete, Language/Theme, and Essential Connections); `#headerUserDropdownMenu` portals to `document.body` (`z-index: 10550`) above `.chat-dropdowns-bar`; Unified Orders uses `.orders-compact-table` with wrapped buyer cells & icon-only delete while removing `#btnToggleFreeTest`; auto-detects and replies in each incoming customer language across all social surfaces (purging fixed language lists); `Smart Support Bot` verifies live Telegram `getMe` status (`off` until connected) locked to `sales_agent`; and inline `Meta Linked` / exclusive `Primary Meta Publisher` checkboxes live directly inside Instagram, Facebook, and WhatsApp cards (`?v=5.4.0`).
- **SaaS BYOK Tier Lock, Custom Agent 5-Layer Sandbox, Paid Mamali Healing, Multi-Site RAG & 80%/90% Smart Storage Cleanup:** Personal BYOK API keys (`byok_override_allowed`) require a Paid plan (`Free` locked with `HTTP 403` + UI upgrade badge while `Basic+` stays unlocked); tenant custom agents are capped strictly at `2/2` behind a 5-Layer `HARD DENY` sandbox blocking Infrastructure, Finance/Licenses, Admin/Core Control, Direct Publishing/Bulk Delete, and `private_customer`/`system_ops` memory scopes; Mamali (`bf_platform`) requires a Paid plan (`HTTP 403` on Free) with `web_search`, tenant self-healing, strict Anti-SSRF host denylist, `HTTP 428` HITL lock, automatic `.bak` backup, and `Fernet enc:v1:` credential vaulting; Asghar (`bf_support`) crawls multiple sites under shared plan budgets (`25/100/400/600/1500` pages tagged by `site_domain`) plus no-website social ingestion; uploads across all 8 core agents enforce executable/macro/magic-byte rejection + 4-lock anti-Zip-Bomb / anti-Zip-Slip `ZIP` extraction (`safe_ingest.py`); and storage auto-purges oldest non-pinned/non-editable/non-catalog assets at `>= 80%` with urgent `#storageCriticalAlertBanner` at `>= 90%` (`< 60%` target).
- **Desktop `Local-First` & Local `MCP` / `Skills`:** Isolated local `Plugins / Skills / MCP` ecosystem unlocked on Desktop & Linux (`Local-First` workspace Vault, `.fnbackup` migration, `BYOK` model routing, and `6 GB VRAM` local `ComfyUI` rendering).
- **AppSec Hardening (`Phase 22-C`):** CVE-patched runtime pins (`fastapi>=0.135.0`, `starlette>=0.49.1`, `pillow>=11.2.1`, `cryptography>=44.0.1`, `jinja2>=3.1.6`, `python-multipart>=0.0.20`, `defusedxml>=0.7.1`, `pyinstaller>=6.13.0`), strict Jinja2 `autoescape`, `defusedxml` SVG/XML parsing, `RejectPolicy()` SSH host-key verification, DOM API UI hardening (zero `document.write`/`innerHTML`), safe symlink-rejecting `TAR` extraction, outbound SSRF & path-containment guards, and `persist-credentials: false` CI workflows.
- **Executive Meeting Room, Turn-Based Voice Roundtable, Supervised Roadmap & Provider-Agnostic Vector Memory (`Phase 23`):** `Titil` automatically selects only relevant specialists (`In Session` vs dimmed `Standby`), orchestrates sequential multi-agent voice roundtables using each agent's own configured voice (`gv:speakerChanged` live avatar pulse + synced mascot eyes), synthesizes persistent categorized `Actionable Roadmap Cards` (`workspaces/{user_id}/roadmaps.db`) with real step delegation & completion checkmarks (`Run Step` / `Execute Full Roadmap`), and preserves `100%` of local SQLite `FTS5` + 64-dim vector memory and roadmap state across any API key, provider, or LLM model switch (`Gemini` / `OpenAI` / `Claude` / `DeepSeek`) across all plans (`?v=5.5.0`).

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
- Copyright © 2026 **Fox Next**.
