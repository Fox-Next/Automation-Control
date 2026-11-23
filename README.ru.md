[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control — от компании Fox Next</h1>

<p align="center">
  <strong>Платформа оркестрации 8 ИИ-агентов, единое настольное приложение Local-First и открытый код Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/ru/">Официальный сайт</a> •
  <a href="https://foxnext.net/ru/download.html">Скачать для Windows</a> •
  <a href="https://foxnext.online/ru/">Облачная панель</a> •
  <a href="ARCHITECTURE.md">Архитектура</a> •
  <a href="SECURITY.md">Безопасность</a>
</p>

---

## 1. Обзор проекта

**Automation Control** (разработка компании **Fox Next**) объединяет **8 специализированных ИИ-агентов** для консультаций и продаж, мультиязычной техподдержки, мониторинга Linux-инфраструктуры, финансового контроля, омниканального маркетинга и креативного медиа-продакшена.

Данный публичный репозиторий содержит:
- Очищенный исходный код **Smart Support Bot** (`smart-support-bot/src/`), извлечённый из рабочего сервиса.
- Скрипты установки в одну строку для **Linux VPS** (`install.sh`) и локального движка **ComfyUI** на Windows (`scripts/setup-comfyui.ps1`).
- Документацию по архитектуре, безопасности и этическим нормам (`ARCHITECTURE.md`, `SECURITY.md`, `CODE_OF_ETHICS.md`).

> Установочные файлы для Windows (`.exe`) не размещаются в Git и доступны только на официальной странице загрузки: [foxnext.net/ru/download.html](https://foxnext.net/ru/download.html).

---

## 2. Основные возможности

- **Слаженная команда из 8 агентов:** оркестратор, синхронизация каталогов, менеджер продаж, техподдержка, Linux DevOps-инженер, казначейство и верификация оплат, специалист по росту и публикациям, а также креативный директор.
- **Глобальное двустороннее голосовое управление:** непрерывная диктовка текста, очистка речевых пауз, последовательная очередь озвучивания ответов агентов, режим Hands-Free и мгновенное прерывание при голосе пользователя (Barge-in).
- **Веб-поиск и защита от SSRF:** ограниченный веб-поиск (до 10 результатов) и безопасная загрузка веб-страниц с блокировкой локальных и приватных IP-диапазонов.
- **Безопасный Desktop Bridge и `Chat-to-Config`:** защищённые формы в чате с прямой записью в шифрованный Vault (маскировка `[REDACTED_SECRET]` до вызова LLM) и строгий контроль SSH-доступа.
- **Единое приложение для ПК (`Local-First` + `ComfyUI`):** подключение собственных API-ключей (BYOK), локальный GPU-рендеринг изображений/видео и перенос рабочего пространства в шифрованном формате `.fnbackup`.

---

## 3. Прозрачные тарифы и редакции

| Тариф | Стоимость | Активные агенты | Основные возможности |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 агентов** | Дневной и месячный лимит токенов, бонус +48ч (для подтверждённого email), 1 соцканал (Telegram/Instagram), 1 каталог, 20 МБ хранилища (временные файлы 7 дней), 7 отложенных постов/неделю, 20 локальных рендеров ComfyUI/мес |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 агентов** | Увеличенный месячный лимит токенов, 10 соцканалов и каталогов, 200 МБ хранилища, Cloud Media API, помесячная выдача годового лимита (`1/12`) + перенос остатка до 3 месяцев |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 агентов** | Расширенный пакет токенов, полная омниканальная публикация и облачные медиа-инструменты с переносом остатка до 3 месяцев |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 агентов** | Максимальная облачная производительность для масштабных кампаний, Cloud Media API и перенос остатка до 3 месяцев |
| **Lifetime** | **`$49`** (разово) | **8 агентов** | **1 переносимая активная установка** (Windows Desktop **или** Linux VPS + `Smart Support Bot`), 48ч тест-драйв, режим BYOK и миграция `.fnbackup` |

Управление подпиской и облачный запуск: [foxnext.online/ru/](https://foxnext.online/ru/).

---

## 4. Быстрая установка

### Вариант A — Единое приложение для Windows (`Local-First` + `ComfyUI`)

1. Скачайте официальный установщик Windows со страницы [foxnext.net/ru/download.html](https://foxnext.net/ru/download.html).
2. *(Опционально)* Разверните локальный **ComfyUI** одной командой в PowerShell:

```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
```

### Вариант B — Установка в одну строку на Linux VPS (`Smart Support Bot`)

```bash
curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | bash
```

Затем заполните `/opt/smart-support/.env` по шаблону `.env.example` (`TELEGRAM_BOT_TOKEN`, `CONTROL_PANEL_URL`) и запустите системную службу `foxnext-smart-support`.

---

## 5. Интеграция с панелью управления (`panel_conversation_hook.py`)

Модуль `smart-support-bot/src/panel_conversation_hook.py` подключает диалоги Telegram к панели управления исключительно через переменные окружения:

- `CONTROL_PANEL_URL`: HTTP/HTTPS-адрес панели управления (без зашитых IP-адресов и приватных доменов).
- `CONTROL_PANEL_TOKEN`: опциональный Bearer-токен для авторизации запросов.
- `CONTROL_PANEL_ROOT`: опциональный локальный путь при совместном размещении.

---

## 6. Структура репозитория

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

## 7. Безопасность, этика и лицензия

- Политика безопасности и защита Vault: [SECURITY.md](SECURITY.md)
- Принципы ответственного ИИ: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- Распространяется по лицензии [MIT License](LICENSE) — © 2026 **Fox Next**.
