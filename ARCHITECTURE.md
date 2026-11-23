# Architecture Overview — Fox Next Automation Control

**Automation Control** is a multi-agent SaaS & Local-First desktop platform developed by **Fox Next** that coordinates **8 specialized AI agents** alongside the open-source **Smart Support Bot** companion (`smart-support-bot/`).

## High-Level Topology

```
+-------------------------------------------------------------------+
|                   User Interfaces & Channels                      |
|  - Web Control Panel (foxnext.online — 10 Languages, RTL/LTR)     |
|  - Unified Windows Desktop App (Local-First + ComfyUI + Voice)    |
|  - Telegram Smart Support Bot (smart-support-bot/src/)            |
+-------------------------------------------------------------------+
            |                                       |
            | HTTPS / WebSocket                     | CONTROL_PANEL_URL Relay
            v                                       v
+-------------------------------------------------------------------+
|               8-Agent Orchestration & Tool Runtime                |
|  1. Orchestrator (Titil)        5. Platform / DevOps (Mamali)     |
|  2. Knowledge & Sync (Updater)  6. Treasury & Finance (Reza)      |
|  3. Sales Consultant (Mandana)  7. Growth & Publishing (Nazi)     |
|  4. Tech Support (Asghar)       8. Creative Director (Shahla)     |
+-------------------------------------------------------------------+
            |                      |                      |
            v                      v                      v
+-------------------+   +--------------------+   +------------------+
| Encrypted Vault   |   | Shared Tools       |   | Media & Audio    |
| & .fnbackup Sync  |   | - Web Search <=10  |   | - Edge-TTS QC    |
| - Pre-LLM Redact  |   | - Anti-SSRF Fetch  |   | - FFmpeg 48kHz   |
| - Chat-to-Config  |   | - Desktop Bridge   |   | - Local ComfyUI  |
+-------------------+   +--------------------+   +------------------+
```

## Components Included in This Public Repository

- `smart-support-bot/src/`: Complete, sanitized runtime for the multilingual Telegram Smart Support Bot (`106` Python modules), including intent routing, catalog retrieval, scheduled jobs, and `src/panel_conversation_hook.py` (which integrates cleanly via `CONTROL_PANEL_URL`).
- `install.sh`: One-command Linux installer for bootstrapping Smart Support Bot + Python environment + systemd supervision.
- `scripts/setup-comfyui.ps1`: One-command Windows PowerShell helper for installing and launching a local ComfyUI image/video generation worker alongside the **Automation Control** Desktop App.
- Multilingual documentation (`README.md`, `README.fa.md`, `README.de.md`, `README.ru.md`, `README.zh.md`).

> Commercial SaaS multi-tenant control plane internals and billing engines remain hosted privately on `foxnext.online` and are not redistributed inside this public repository.
