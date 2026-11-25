[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control v3.0.0 — от Fox Next</h1>

<p align="center">
  <strong>Платформа оркестрации 8 ИИ-агентов, настольное приложение Local-First и открытый Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/ru/">Официальный сайт</a> •
  <a href="https://foxnext.net/ru/download.html">Страница загрузки (foxnext.net)</a> •
  <a href="https://github.com/Fox-Next/Automation-Control/releases/latest">GitHub Releases (v3.0.0)</a> •
  <a href="https://foxnext.online/ru/">Облачная панель</a> •
  <a href="ARCHITECTURE.md">Архитектура</a> •
  <a href="SECURITY.md">Безопасность</a>
</p>

---

## 1. Обзор и официальные релизы (`v3.0.0`)

**Automation Control** (от **Fox Next**) координирует **8 специализированных ИИ-агентов** для продаж, технической поддержки, мониторинга Linux-инфраструктуры, финансового контроля, омниканального маркетинга и креативного продакшена.

Все официальные сборки (`v3.0.0`) с контрольными суммами `SHA256SUMS.txt` опубликованы на **[GitHub Releases](https://github.com/Fox-Next/Automation-Control/releases/latest)** и **[foxnext.net/ru/download.html](https://foxnext.net/ru/download.html)**:

| Пакет | Платформа | Назначение |
| :--- | :--- | :--- |
| **`AutomationControl.exe`** | Windows | Единое приложение (~29 МБ) в светлой теме `foxnext.online` с автомаршрутизацией по email (`Cloud`, `Self-Hosted VPS`, `Local Engine`), шлюзом `connect_vps_strict`, Multi-GPU-воркером (`>= 6 ГБ VRAM`) и загрузкой `ComfyUI` / `FFmpeg` по требованию |
| **`automation-control-linux.tar.gz`** | Linux VPS | Очищенный пакет Self-Hosted для автоматической загрузки скриптом `install.sh` |
| **`SHA256SUMS.txt`** | Все | Криптографические хеши `SHA-256` для проверки подлинности пакетов |

---

## 2. Ключевые возможности

- **8 агентов в режимах Simple (`Grok Bot`) и Advanced:** компактный 3-колоночный чат или полная панель с 6 вкладками.
- **Вход через Google OAuth и One Tap:** быстрая авторизация с поддержкой 10 языков интерфейса.
- **Двустороннее голосовое управление:** непрерывная диктовка, очередь озвучивания ответов, режим Hands-Free и прерывание голосом (`Barge-in`).
- **Двухуровневый движок `Chat-First` для DM и комментариев:** экономичная обработка сообщений в Instagram и Telegram.
- **Трёхуровневая система памяти:** автоматическое сжатие контекста и база знаний бренда для снижения расхода токенов.
- **Интеграция `cPanel / SSH / SFTP` без браузера и Commerce Hub:** прямое подключение с немедленной очисткой временных паролей, а также единый центр финансов, магазина и склада (с сайтом или без него).
- **Единое приложение Windows и маршрутизация по лицензии:** Один компактный `AutomationControl.exe` (~29 МБ) в светлой теме `foxnext.online`, автовход по email/Google, строгая онлайн-проверка лицензии для VPS и загрузка `ComfyUI`/`FFmpeg` по требованию.
- **Двухслотовая политика сеансов (`Web + Desktop`):** Единообразно для всех тарифов (`Free`–`Lifetime`) разрешает **1 активный Web-сеанс + 1 активный Desktop-сеанс** одновременно; повторный вход на той же платформе заменяет только её предыдущий сеанс.
- **Поддержка Multi-GPU (`CUDA`, `ROCm`, `DirectML`):** Полный поиск всех GPU (`NVIDIA`, `AMD Radeon`, `Intel Arc`, `>= 6 ГБ VRAM`) и ручной выбор видеокарты в настройках.
- **Настройки → Инструменты и MCP (`find_tools` и `register_tool_or_mcp`):** Все 8 агентов автономно находят, регистрируют и вызывают инструменты; в Desktop и Self-Hosted доступны собственные MCP-серверы, а в Shared Cloud — изолированные безопасные `https://` webhook/API-инструменты (лимит 32 КБ).
- **Двухуровневое наследование ИИ, `Unlimited` Max Tokens и локализованные промпты 8 агентов:** Облачные подписчики хранят изолированные BYOK-ключи без доступа к бюджетам суперадмина; все 8 агентов используют нейтральные к бренду системные промпты на языке панели и значение `Max Tokens = 0` (`Unlimited`) по умолчанию.
- **Иерархия управления суперадмина, динамические `Annual USD` и `Storage MB`, пополнение `$1–$10` и Danger Zone:** Разделение Primary (закреплён в строке №1, защищён от удаления) и Secondary суперадминов с проверкой `Email OTP + Reason`, метрика `Online Now`, пагинация по 10 строк, живой редактор тарифов (`Monthly USD`, `Annual USD`, `Tokens / mo`, `Storage MB`) с мгновенным обновлением лимита загрузки `HTTP 413` без перезапуска, пополнение `$1–$10`, табличный журнал аудита (`update_pricing_policy`, без сырых ключей), двухстрочный режим кампаний (`Publish Immediately` + `datetime-local`), 5 полноширинных пулов API, локализованная диагностика на 10 языках и самоудаление аккаунта через Email OTP с мгновенным отзывом Web/Desktop-сеансов.
- **Локальные `MCP / Skills / Plugins` и `Local-First`:** локальная экосистема для ПК и Linux, шифрованный Vault, перенос `.fnbackup`, режим `BYOK` и локальный `ComfyUI`.

---

## 3. Тарифы и редакции

| Тариф | Цена | Активные агенты | Основные возможности |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 агентов** | Базовый дневной/месячный лимит токенов + бонус 48ч, 1 соцканал, 1 каталог, 20 МБ хранилища, локальный `ComfyUI` |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 агентов** | Расширенный месячный лимит, 10 соцканалов и каталогов, 200 МБ, Cloud Media API + перенос остатка до 3 месяцев |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 агентов** | Увеличенный пакет токенов, полная омниканальная публикация и облачные медиа + перенос остатка до 3 месяцев |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 агентов** | Максимальная производительность облака для команд и масштабных кампаний + перенос до 3 месяцев |
| **Lifetime** | **`$49`** (разово) | **8 агентов** | **1 переносимая установка** (единая `AutomationControl.exe` в режиме `Local Engine` для Windows **или** Linux VPS + Smart Support Bot), 48ч тест, `BYOK`, `.fnbackup` |

---

## 4. Команды установки в одну строку

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

## 5. Интеграция с панелью (`panel_conversation_hook.py`)

Модуль `smart-support-bot/src/panel_conversation_hook.py` подключается к панели исключительно через переменные окружения (`CONTROL_PANEL_URL`, `CONTROL_PANEL_TOKEN`, `CONTROL_PANEL_ROOT`).

---

## 6. Структура репозитория

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

## 7. Безопасность, этика и лицензия

- Политика безопасности и Vault: [SECURITY.md](SECURITY.md)
- Принципы этичного ИИ: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- Архитектура: [ARCHITECTURE.md](ARCHITECTURE.md)
- Лицензия [MIT License](LICENSE) — © 2026 **Fox Next**.
