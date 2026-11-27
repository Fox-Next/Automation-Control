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
- **Aufgeräumte Chat-Leiste, Meeting-Room Live-Sprache & klappbare Swarm-Tabelle:** Bündelt Chat-Aktionen, Schnelleinrichtung und Playbooks in 3 lokalisierten Dropdown-Menüs (`Tools & Chat`, `Quick Setup`, `Ready Playbooks`), reine Symbolleiste mit 4-Balken-Diktat-Equalizer (ohne automatisches Absenden), Live-Sprachmodus mit zentriertem `#38bdf8`-Maskottchen über weichgezeichnetem Hintergrund in Einzelchat & Meeting Room sowie ein standardmäßig eingeklapptes einheitliches Swarm-Akkordeon (10 Einträge/Seite, neuestes Datum oben, Mehrfach-Löschung und `In Chat senden`).
- **Zweistufige `Chat-First`-DM- & Kommentar-Engine:** Token-sparende Verarbeitung für Instagram und Telegram.
- **3-Schichten-Speicherarchitektur:** Automatische Gedächtniskomprimierung und Brand-Brain-Kontext für präzise Antworten.
- **Browserlose `cPanel / SSH / SFTP`-Anbindung & Commerce-Hub:** Direkte Server-Integration (mit sofortiger Bereinigung temporärer Zugangsdaten) sowie Shop-, Bestell- und Lagerverwaltung mit oder ohne eigene Website.
- **Einheitliche Windows-App & E-Mail-Lizenzrouting:** Eine einzelne schlanke `AutomationControl.exe` (~29 MB) im hellen `foxnext.online`-Design mit automatischem Tarif-Routing nach Anmeldung, strengem Online-VPS-Lizenzgate und On-Demand-Download für `ComfyUI`/`FFmpeg`.
- **Dual-Slot-Sitzungsrichtlinie (`Web + Desktop`):** Erlaubt einheitlich für alle Tarife (`Free` bis `Lifetime`) **1 aktive Web-Sitzung + 1 aktive Desktop-Sitzung** gleichzeitig; eine erneute Anmeldung auf derselben Plattform ersetzt nur deren vorherige Sitzung.
- **Multi-GPU (`NVIDIA CUDA`, `AMD ROCm/DirectML`, `Intel Arc`):** Automatische Multi-GPU-Erkennung (`>= 6 GB VRAM`) und manuelle GPU-Auswahl.
- **Einstellungen → Tools & MCP (`find_tools` & `register_tool_or_mcp`):** Alle 8 Agenten entdecken, registrieren und nutzen Tools autonom; Desktop & Self-Hosted erlauben benutzerdefinierte MCP-Server, während Shared Cloud auf mandantenisolierte `https://`-API-/Webhook-Tools beschränkt ist (32-KB-Limit).
- **2-Schichten-KI-Vererbung, BYOK-Kontingentbefreiung & Studio-Standarddesign:** Saubere Erstellung eigener Agenten mit verschlüsselten BYOK-Schlüsseln (`enc:v1:`), `?`-Hilfe für kostenlose Gemini-Keys (`aistudio.google.com`) und **0 Cloud-Token-Abzug** in Chat, Meeting Room & Creative Studio; alle 8 Kernagenten nutzen markenneutrale, in 10 Sprachen lokalisierte Verhaltensregeln inkl. großem Bearbeitungsdialog, dauerhafte Chat-Löschung auf Datenträger, `Max Tokens = 0` (`Unlimited`), `16` `?`-Hilfen sowie sofortige DSGVO-Arbeitsbereichsbereinigung (`shutil.rmtree`) bei bestätigter Kontolöschung in der Profile Danger Zone.
- **Zero-Flash 10-Sprachen-UI, Google-Profilbild & 16 kontextuelle `?`-Hilfen:** Flackerfreier Pre-Paint-Sprachstart (`i18n-prepaint`), entprellte DOM-Übersetzung (`window.__bfI18nTranslating`), rundes Google-Profilbild im Header und 16 interaktive `?`-Hilfebuttons in allen Tabs und Einstellungen.
- **Tägliche/Wöchentliche Nutzungslimits mit Reset-Countdown & Read-Only-Finanzmonitor:** Konfigurierbare Tages- und Wochenlimits (`daily_token_cap`, `weekly_token_cap`), automatischer UTC-Reset mit Fortschrittsbalken und Countdown (`Resets in ...`, ohne rohe Token-Zahlen) im Dashboard, freundliche `HTTP 429`-Hinweise sowie strikt schreibgeschützte Zahlungsüberwachung ohne Auszahlungsfunktionen.
- **Superadmin-Governance, Live-`Annual USD` & `Storage MB`-Quoten, `$1–$10` Aufladung, Audit-Log & Danger Zone:** Hierarchie aus primärem (oben fixiert, unlöschbar) und sekundärem Superadmin mit `E-Mail-OTP + Begründung`-Pflicht, `Online Now`-KPI, 10-Zeilen-Paginierung & Sortierung, Live-Preiseditor (`Monthly USD`, `Annual USD`, `Daily Cap`, `Weekly Cap`, `Tokens / mo`, `Storage MB`) mit sofortiger `HTTP 413`-Upload-Durchsetzung ohne Neustart, dynamischem `$1–$10` Dollar-Top-Up, tabellarischem Audit-Log (`update_pricing_policy`, ohne Klartext-Keys), 2-zeiligem Kampagnenmodus (`Publish Immediately` + `datetime-local`), vollbreiten 5 Cloud-API-Pools, lokalisierten Diagnose-/Verbindungstests sowie Selbstlöschung im Profil (`Danger Zone` per E-Mail-OTP inkl. sofortiger Beendigung aller Web-/Desktop-Sitzungen).
- **Interaktiver `Spotlight`-Workflow-Graph, 8 Social-Gateways, Mobile-Fallback & Meta Cross-Posting (`∞ Meta`):** Dezente Ruhelinien (`0.10` Deckkraft) blenden bei Hover/Klick nur verbundene Pfade animiert ein, dimmen fremde Knoten (`0.28`) und platzieren kollisionsfreie Kantenlabels über den Karten für alle 8 Social-Output-Gateways (`Telegram`, `Instagram`, `Facebook`, `WhatsApp`, `YouTube`, `LinkedIn`, `X`, `Reddit`) sowie dynamische Brand-Brain-Domains; unkonfigurierte Gateways sind strikt gesperrt (`HTTP 400 gateway_not_configured` + direkter Sprung zu `Einstellungen → Social Media`), Mobilansichten (`<= 768px`) zeigen nur die unteren Statuskarten und `Meta Accounts Center Cross-Posting` blendet `∞ Meta`-Badges ein und dedupliziert API-Publikationen über den primären Meta-Publisher (DMs und Kommentare bleiben unabhängig).
- **Mobile-70%-Drawer, UUID-Zitate, `FileRegistry` & Range-Medienstreaming:** Mobil-Drawer (`<= 768px`), serverseitige `UUID`-Antworten mit Sprungmarkierung, mandantenisolierte `FileRegistry` inkl. `SVG`-Bereinigung und `HTTP 206` Byte-Range-Vorschau (`media_preview.js`).
- **Einheitlicher `StorageManager` (`Google Drive drive.file`, `Cloudflare R2`, Lokal):** Verschlüsseltes `drive.file`-OAuth (`enc:v1:`), direkte Transfers, Formatoptimierung und geschützte Lebenszyklus-Bereinigung.
- **4-Schichten-`MemoryManager` & editierbarer `Timeline Manifest`-Workflow:** Hybrid-Suche per `SQLite FTS5` + 64-Dim-Vektoren, Secret-Blocker (`HTTP 422`), Versionshistorie sowie Mehrszenen-Videotimelines (`style_bible`-Kontinuität, Einzelszenen-Regenerierung, Cloud-CPU-Schild und `ffprobe`/`blackdetect`-QA).
- **Google One Tap, Pflicht-AGB-Gate, Sicherheitsheader & eigene Fonts:** `One Tap`-Login mit `CORS` für `foxnext.online` & `app.foxnext.online`, einmalige `terms_accepted_at`-Prüfung (`HTTP 403 terms_not_accepted` bis `#modalMandatoryTermsGate`), `HSTS`/`XFO: DENY`/CSP-Header sowie 35 lokal gehostete `.woff2`-Schriften ohne externe CDN-Abrufe.
- **5-Stunden-Rollenlimit, 12-Feld-Cloud-Media-Pool & Live-Wechselkurs:** 12-Feld-Media-Pool (`span 2`, Bild/Audio/Video, an `HybridComputeRouter` angebunden), einzeilige Pool-Badges, rotierendes **5-Stunden-Nutzungslimit** inkl. Countdown und Live-Wechselkurs-Editor (`275.000` Toman/USD).
- **Omnichannel-Commerce mit hoher Nebenläufigkeit (`70+` Kunden), Universal-Beleg-OCR & Bestellabschluss:** Mandantenisolierte SQLite-`WAL`-Konversationen (`168h` Speicherung über Telegram, Instagram, WhatsApp & Facebook) mit geprüfter `70+`-Parallelitätsstabilität; multimodale Beleg-OCR mit streng schreibgeschützter Prüfung angeschlossener Gateways (`BEP-20`/`TRC-20`/`TON`, `Dodo Payments`, `Stripe`, `PayPal`, `Visa/Mastercard` per `HTTP GET`, ohne Auszahlungszugriff); natürliches `Comment-to-DM` aus dem `Brand Brain` sowie automatisierter Versand- (inkl. 10-stelliger PLZ) und Lizenzabschluss (`FulfillmentService`).
- **Shahla Pro Creative Studio (`bf_creative`, 7 autorisierte Tools):** Web- & Markenpaletten-Erkennung (`fetch_webpage`, `web_search`), mandantenisolierte Produkt- & Logo-Komposition (`edit_reference_image` mit `HTTP 403` Eigentumsschutz), gestochen scharfe RTL/LTR-Typografie ohne KI-Textfehler (`render_typography_overlay` via `Pillow`, `arabic-reshaper` & `python-bidi`), 1-Klick-Export in `9:16`, `1:1` & `16:9` in `FileRegistry`, synchrone `.srt`/`.ass`-Untertitel (Cloud-CPU-Schild-konform) sowie visueller Selbst-QA mit hartem Limit von max. 1 Wiederholungsversuch.
- **Mobile Simple-Mode-Sperre, Header-Portal-Menü, echte Bot-Prüfung & Inline-Meta-Optionen:** Mobilgeräte (`<= 768px`) bleiben fest im `Simple Mode` mit 3-teiligem `70vw`-Drawer (`#mobileDrawerProfileFooter` + kategorisiertes `#mobileSettingsModal` für Kontingente/Logout/DSGVO-Löschung, Sprache/Theme & Verbindungen); `#headerUserDropdownMenu` wird mit `z-index: 10550` über `.chat-dropdowns-bar` gerendert; kompakte Bestelltabelle `.orders-compact-table` mit Zeilenumbruch & ohne Test-Toggles; automatische Kundenspracherkennung über alle Kanäle hinweg; echte `Telegram getMe`-Statusprüfung für `Smart Support Bot` (`off` bis verbunden) und exklusive Inline-Meta-Checkboxen direkt in Instagram-, Facebook- & WhatsApp-Kontokarten (`?v=5.4.0`).
- **Free-BYOK-Sperre, 5-Schichten-Sandbox für max. 2 Custom-Agenten, Mamali-Upgrade, Multi-Site-Crawler & 80%/90%-Bereinigung:** Persönliche BYOK-Schlüssel erfordern einen bezahlten Tarif (`Free` mit `HTTP 403` & UI-Hinweis gesperrt, `Basic+` freigeschaltet); eigene Agenten sind strikt auf `2/2` mit einer 5-Schichten-`HARD DENY`-Sandbox (Infrastruktur, Finanzen/Lizenzen, Admin-Kern, Direktveröffentlichung/Massenlöschung & private Speicherbereiche) begrenzt; Mamali (`bf_platform`) bietet zahlenden Nutzern `web_search`, Mandanten-Selbstheilung, Anti-SSRF-Sperrliste, `HTTP 428` HITL-Gate, automatisches `.bak`-Backup & `Fernet enc:v1:`; Asghar (`bf_support`) crawlt mehrere Websites mit Tarifbudget (`25/100/400/600/1500` Seiten inkl. `site_domain`-Tagging & Social-Ingestion); alle 8 Agenten nutzen ausführbare/Magic-Byte-Filter + 4-fach geschützte `ZIP`-Entpackung (`safe_ingest.py`); und die Speicherautomatik bereinigt ab `>= 80%` bzw. warnt per `#storageCriticalAlertBanner` ab `>= 90%` (`< 60%`-Ziel).
- **Lokale `MCP / Skills / Plugins` & `Local-First`:** Lokales `MCP`-Ökosystem auf Desktop/Linux, verschlüsselter Vault, `.fnbackup`-Migration, `BYOK` und lokales `ComfyUI`.
- **AppSec-Härtung (`Phase 22-C`):** CVE-gepatchte Abhängigkeiten (`fastapi`, `starlette`, `pillow`, `cryptography`, `jinja2`, `python-multipart`, `defusedxml`, `pyinstaller`), striktes Jinja2-`autoescape`, `defusedxml`-SVG-Analyse, sichere SSH-Host-Key-Prüfung (`known_hosts` / `RejectPolicy()`), DOM-APIs ohne `document.write`/`innerHTML`, sicheres `TAR`-Entpacken ohne Symlink-Escape, SSRF-/Pfadschutz sowie `persist-credentials: false` im CI-Workflow.
- **Executive Meeting Room, Stimm-Roundtable, überwachte Roadmap & anbieterunabhängiger Vektorspeicher (`Phase 23`):** `Titil` wählt automatisch nur relevante Spezialisten (`Im Meeting` vs. abgeblendetes `Bereitschaft`), führt sequenzielle Multi-Agenten-Sprachrunden mit je eigener Stimme (`gv:speakerChanged`-Avatar-Puls) durch, speichert ausführbare `Roadmap-Karten` isoliert in `workspaces/{user_id}/roadmaps.db` mit echter Schritt-Delegation (`✅ Erledigt`) und sichert dank lokalem `SQLite FTS5` + 64-Dim-Vektoren `100%` Kontinuität bei jedem API-Key- oder Modellwechsel (`?v=5.5.0`).

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
