[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control — von Fox Next</h1>

<p align="center">
  <strong>8-Agenten-KI-Orchestrierungsplattform, einheitliche Local-First-Desktop-App &amp; Open-Source Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/de/">Offizielle Website</a> •
  <a href="https://foxnext.net/de/download.html">Windows-App herunterladen</a> •
  <a href="https://foxnext.online/de/">Cloud-Kontrollpanel</a> •
  <a href="ARCHITECTURE.md">Architektur</a> •
  <a href="SECURITY.md">Sicherheit</a>
</p>

---

## 1. Überblick

**Automation Control** (entwickelt von **Fox Next**) koordiniert **8 spezialisierte KI-Agenten** für Vertrieb, technischen Multi-Plattform-Support, Linux-DevOps-Überwachung, Finanzprüfung, Omnichannel-Publishing sowie Audio- und Videoproduktion.

Dieses öffentliche Repository enthält:
- Den bereinigten Open-Source-Code von **Smart Support Bot** (`smart-support-bot/src/`), direkt aus dem Live-Produktionspfad extrahiert.
- Einzeilige Installationsskripte für **Linux VPS** (`install.sh`) und lokales **ComfyUI** unter Windows (`scripts/setup-comfyui.ps1`).
- Architektur-, Sicherheits- und Ethikdokumentation (`ARCHITECTURE.md`, `SECURITY.md`, `CODE_OF_ETHICS.md`).

> Ausführbare Windows-Installer (`.exe`) werden nicht in Git gespeichert, sondern ausschließlich über die offizielle Download-Seite bereitgestellt: [foxnext.net/de/download.html](https://foxnext.net/de/download.html).

---

## 2. Kernfunktionen

- **Koordiniertes 8-Agenten-Team:** Orchestrator, Wissens- & Katalog-Sync, Verkaufsberater, technischer Support, Linux-Plattformingenieur, Finanz- & Lizenzprüfung, Omnichannel-Marketing und Creative Director.
- **Globale Zwei-Wege-Sprachsteuerung:** Kontinuierliches Diktat, automatische Textbereinigung, geordnete TTS-Warteschlange, Hands-Free-Stilleerkennung und sofortiges Barge-in bei Benutzereingaben.
- **Websuche & Anti-SSRF-Abruf:** Begrenzte Websuche (max. 10 Treffer) sowie netzwerksicherer Seitenabruf mit Blockierung privater/interner IP-Bereiche.
- **Sicherer Desktop-Bridge & `Chat-to-Config`:** Verschlüsselte Formular-Karten direkt im Chat für den Vault (`[REDACTED_SECRET]`-Maskierung vor jedem LLM) sowie SSH-geschützte Plattformbefehle.
- **Einheitliche Desktop-App (`Local-First` + `ComfyUI`):** Eigene API-Schlüssel (BYOK) und lokale GPU-Medienrenderings offline nutzen – mit verschlüsselter `.fnbackup`-Migration.

---

## 3. Transparente Tarife & Editionen

| Tarif | Preis | Aktive Agenten | Leistungsumfang |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 Agenten** | Tägliches & monatliches Token-Kontingent, +48h-Willkommensbonus (verifizierte E-Mail), 1 Social-Kanal (Telegram/Instagram), 1 Katalog, 20 MB Speicher (7 Tage Temp-TTL), 7 geplante Posts/Woche, 20 lokale ComfyUI-Outputs/Monat |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 Agenten** | Erweitertes Monatskontingent, 10 Social-Kanäle & Kataloge, 200 MB Speicher, Cloud Media API aktiv, jährliche Monatsfreigabe (`1/12`) + bis zu 3 Monate Rollover |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 Agenten** | Hohes monatliches Token-Kontingent, vollständige Omnichannel- & Cloud-Media-Automatisierung inkl. bis zu 3 Monate Rollover |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 Agenten** | Maximale Cloud-Kapazität für Teams & intensive Kampagnen, Cloud Media APIs inkl. bis zu 3 Monate Rollover |
| **Lifetime** | **`$49`** (einmalig) | **8 Agenten** | **1 übertragbare aktive Installation** (Windows-Desktop **oder** Linux VPS + `Smart Support Bot`), 48h-Testphase, BYOK-Unterstützung & `.fnbackup`-Migration |

Verwalten Sie Ihr Konto direkt über das Cloud-Panel: [foxnext.online/de/](https://foxnext.online/de/).

---

## 4. Schnellinstallation

### Option A — Einheitliche Windows-Desktop-App (`Local-First` + `ComfyUI`)

1. Laden Sie das offizielle Windows-Paket herunter: [foxnext.net/de/download.html](https://foxnext.net/de/download.html).
2. *(Optional)* Lokales **ComfyUI** per PowerShell-Einzeiler einrichten:

```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
```

### Option B — Einzeilige Linux-VPS-Installation (`Smart Support Bot`)

```bash
curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | bash
```

Passen Sie anschließend `/opt/smart-support/.env` anhand von `.env.example` an (`TELEGRAM_BOT_TOKEN`, `CONTROL_PANEL_URL`) und starten Sie den Dienst `foxnext-smart-support`.

---

## 5. Kontrollpanel-Integration (`panel_conversation_hook.py`)

`smart-support-bot/src/panel_conversation_hook.py` verbindet Telegram-Sitzungen herstellerneutral ausschließlich über Umgebungsvariablen mit dem Kontrollpanel:

- `CONTROL_PANEL_URL`: Ziel-URL des Kontrollpanels (ohne fest einprogrammierte IPs oder private Hosts).
- `CONTROL_PANEL_TOKEN`: Optionales Bearer-Token für signierte Relay-Aufrufe.
- `CONTROL_PANEL_ROOT`: Optionaler lokaler Pfad bei gemeinsamem Host-Deployment.

---

## 6. Repository-Struktur

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

## 7. Sicherheit, Ethik & Lizenz

- Schwachstellenmeldung & Vault-Schutz: [SECURITY.md](SECURITY.md)
- Verantwortungsvolle KI-Nutzung: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- Lizenziert unter der [MIT-Lizenz](LICENSE) — Copyright © 2026 **Fox Next**.
