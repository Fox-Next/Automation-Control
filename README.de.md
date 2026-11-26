[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control v3.0.0 — von Fox Next</h1>

<p align="center">
  <strong>8-Agenten-KI-Plattform, einheitliche Local-First-Desktop-App &amp; Open-Source Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/de/">Offizielle Website</a> •
  <a href="https://foxnext.net/de/download.html">Download-Seite (foxnext.net)</a> •
  <a href="https://github.com/Fox-Next/Automation-Control/releases/latest">GitHub Releases (v3.0.0)</a> •
  <a href="https://foxnext.online/de/">Cloud-Panel</a> •
  <a href="ARCHITECTURE.md">Architektur</a> •
  <a href="SECURITY.md">Sicherheit</a>
</p>

---

## 1. Überblick & Offizielle Releases (`v3.0.0`)

**Automation Control** (von **Fox Next**) koordiniert **8 spezialisierte KI-Agenten** für Vertrieb, technischen Multi-Plattform-Support, Linux-Betrieb, Lizenz- & Bestellprüfung, Omnichannel-Marketing sowie kreative Medienproduktion.

Alle offiziellen Pakete (`v3.0.0`) inklusive `SHA256SUMS.txt` sind auf **[GitHub Releases](https://github.com/Fox-Next/Automation-Control/releases/latest)** und **[foxnext.net/de/download.html](https://foxnext.net/de/download.html)** verfügbar:

| Paket | Zielsystem | Beschreibung |
| :--- | :--- | :--- |
| **`AutomationControl.exe`** | Windows | Einheitliche Windows-App (~29 MB) im hellen `foxnext.online`-Design mit E-Mail-Lizenzrouting (`Cloud`, `Self-Hosted VPS`, `Local Engine`), `connect_vps_strict`, Multi-GPU-Worker (`>= 6 GB VRAM`) und On-Demand-Setup für `ComfyUI` / `FFmpeg` |
| **`automation-control-linux.tar.gz`** | Linux VPS | Bereinigtes Self-Hosted-Laufzeitpaket für die automatische Installation via `install.sh` |
| **`SHA256SUMS.txt`** | Alle | Offizielle `SHA-256`-Prüfsummen aller Release-Dateien |

---

## 2. Zentrale Funktionen

- **8 Agenten mit Simple Mode (`Grok Bot`) & Advanced Mode:** Schlankes 3-Spalten-Chat-Layout oder vollständiges 6-Tab-Kontrollpanel.
- **Google OAuth & One Tap:** Schnelle Anmeldung per Google oder E-Mail-Verifizierung in 10 Sprachen.
- **Aufgeräumte Chat-Leiste, Diktat-Equalizer & Live-Zweiwege-Sprachmaskottchen:** Bündelt Chat-Aktionen, Schnelleinrichtung und Playbooks in 3 lokalisierten Dropdown-Menüs (`Tools & Chat`, `Quick Setup`, `Ready Playbooks`), bietet eine reine Symbolleiste mit 4-Balken-Equalizer fürs Sprachdiktat (ohne automatisches Absenden) sowie einen grünen Live-Sprachmodus, der das Maskottchen mit leuchtend blauen `#38bdf8`-Augen über einem weichgezeichneten Chat-Hintergrund zentriert und während TTS-Antworten dynamisch per Audio-Equalizer animiert.
- **Zweistufige `Chat-First`-DM- & Kommentar-Engine:** Token-sparende Verarbeitung für Instagram und Telegram.
- **3-Schichten-Speicherarchitektur:** Automatische Gedächtniskomprimierung und Brand-Brain-Kontext für präzise Antworten.
- **Browserlose `cPanel / SSH / SFTP`-Anbindung & Commerce-Hub:** Direkte Server-Integration (mit sofortiger Bereinigung temporärer Zugangsdaten) sowie Shop-, Bestell- und Lagerverwaltung mit oder ohne eigene Website.
- **Einheitliche Windows-App & E-Mail-Lizenzrouting:** Eine einzelne schlanke `AutomationControl.exe` (~29 MB) im hellen `foxnext.online`-Design mit automatischem Tarif-Routing nach Anmeldung, strengem Online-VPS-Lizenzgate und On-Demand-Download für `ComfyUI`/`FFmpeg`.
- **Dual-Slot-Sitzungsrichtlinie (`Web + Desktop`):** Erlaubt einheitlich für alle Tarife (`Free` bis `Lifetime`) **1 aktive Web-Sitzung + 1 aktive Desktop-Sitzung** gleichzeitig; eine erneute Anmeldung auf derselben Plattform ersetzt nur deren vorherige Sitzung.
- **Multi-GPU (`NVIDIA CUDA`, `AMD ROCm/DirectML`, `Intel Arc`):** Automatische Multi-GPU-Erkennung (`>= 6 GB VRAM`) und manuelle GPU-Auswahl.
- **Einstellungen → Tools & MCP (`find_tools` & `register_tool_or_mcp`):** Alle 8 Agenten entdecken, registrieren und nutzen Tools autonom; Desktop & Self-Hosted erlauben benutzerdefinierte MCP-Server, während Shared Cloud auf mandantenisolierte `https://`-API-/Webhook-Tools beschränkt ist (32-KB-Limit).
- **2-Schichten-KI-Vererbung, `Unlimited` Max Tokens & lokalisierte 8-Agenten-Prompts:** Cloud-Abonnenten speichern eigene BYOK-Konfigurationen isoliert pro Agent ohne Zugriff auf Superadmin-Keys/Budgets; alle 8 Agenten nutzen markenneutrale, sprachspezifische System-Prompts und setzen `Max Tokens` standardmäßig auf `0` (`Unlimited`).
- **Zero-Flash 10-Sprachen-UI, Google-Profilbild & 15 kontextuelle `?`-Hilfen:** Flackerfreier Pre-Paint-Sprachstart (`i18n-prepaint`), entprellte DOM-Übersetzung (`window.__bfI18nTranslating`), rundes Google-Profilbild im Header und 15 interaktive `?`-Hilfebuttons in allen Tabs und Einstellungen.
- **Tägliche/Wöchentliche Nutzungslimits mit Reset-Countdown & Read-Only-Finanzmonitor:** Konfigurierbare Tages- und Wochenlimits (`daily_token_cap`, `weekly_token_cap`), automatischer UTC-Reset mit Fortschrittsbalken und Countdown (`Resets in ...`, ohne rohe Token-Zahlen) im Dashboard, freundliche `HTTP 429`-Hinweise sowie strikt schreibgeschützte Zahlungsüberwachung ohne Auszahlungsfunktionen.
- **Superadmin-Governance, Live-`Annual USD` & `Storage MB`-Quoten, `$1–$10` Aufladung, Audit-Log & Danger Zone:** Hierarchie aus primärem (oben fixiert, unlöschbar) und sekundärem Superadmin mit `E-Mail-OTP + Begründung`-Pflicht, `Online Now`-KPI, 10-Zeilen-Paginierung & Sortierung, Live-Preiseditor (`Monthly USD`, `Annual USD`, `Daily Cap`, `Weekly Cap`, `Tokens / mo`, `Storage MB`) mit sofortiger `HTTP 413`-Upload-Durchsetzung ohne Neustart, dynamischem `$1–$10` Dollar-Top-Up, tabellarischem Audit-Log (`update_pricing_policy`, ohne Klartext-Keys), 2-zeiligem Kampagnenmodus (`Publish Immediately` + `datetime-local`), vollbreiten 5 Cloud-API-Pools, lokalisierten Diagnose-/Verbindungstests sowie Selbstlöschung im Profil (`Danger Zone` per E-Mail-OTP inkl. sofortiger Beendigung aller Web-/Desktop-Sitzungen).
- **Lokale `MCP / Skills / Plugins` & `Local-First`:** Lokales `MCP`-Ökosystem auf Desktop/Linux, verschlüsselter Vault, `.fnbackup`-Migration, `BYOK` und lokales `ComfyUI`.

---

## 3. Tarife & Editionen

| Tarif | Preis | Aktive Agenten | Leistungsumfang |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 Agenten** | Starter-Tages-/Monatskontingent + 48h-Willkommensbonus, 1 Social-Kanal, 1 Katalog, 20 MB Speicher, lokales `ComfyUI` |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 Agenten** | Erweitertes Monatskontingent, 10 Social-Kanäle & Kataloge, 200 MB Speicher, Cloud Media API + 3 Monate Rollover |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 Agenten** | Hohes Monatskontingent, vollständige Omnichannel- & Cloud-Media-Automatisierung + 3 Monate Rollover |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 Agenten** | Maximale Cloud-Kapazität für Teams & große Kampagnen + 3 Monate Rollover |
| **Lifetime** | **`$49`** (einmalig) | **8 Agenten** | **1 übertragbare Installation** (einheitliche `AutomationControl.exe` im `Local Engine`-Modus unter Windows **oder** Linux VPS + Smart Support Bot), 48h-Test, `BYOK`, `.fnbackup` |

---

## 4. Einzeilige Installationsbefehle

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

## 5. Kontrollpanel-Integration (`panel_conversation_hook.py`)

`smart-support-bot/src/panel_conversation_hook.py` verbindet Telegram-Sitzungen ausschließlich über Umgebungsvariablen (`CONTROL_PANEL_URL`, `CONTROL_PANEL_TOKEN`, `CONTROL_PANEL_ROOT`).

---

## 6. Repository-Struktur

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

## 7. Sicherheit, Ethik & Lizenz

- Sicherheit & Vault: [SECURITY.md](SECURITY.md)
- Ethik-Richtlinien: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- Architektur: [ARCHITECTURE.md](ARCHITECTURE.md)
- Lizenziert unter [MIT License](LICENSE) — Copyright © 2026 **Fox Next**.
