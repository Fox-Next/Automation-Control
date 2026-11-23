[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<div dir="rtl" align="right">

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control — محصول شرکت Fox Next</h1>

<p align="center">
  <strong>پلتفرم هوشمند ۸ ایجنت، اپلیکیشن دسکتاپ یکپارچه Local-First و سورس باز Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/fa/">وب‌سایت رسمی</a> •
  <a href="https://foxnext.net/fa/download.html">دانلود نسخه ویندوز</a> •
  <a href="https://foxnext.online/fa/">پنل ابری کنترل</a> •
  <a href="ARCHITECTURE.md">معماری سیستم</a> •
  <a href="SECURITY.md">سیاست امنیت</a>
</p>

---

## ۱. معرفی پروژه

نرم‌افزار **Automation Control** (ساخت شرکت **Fox Next**) تیمی متشکل از **۸ ایجنت هوش مصنوعی تخصصی** را برای فروش، پشتیبانی فنی چندسکویی، نظارت زیرساخت لینوکس، امور مالی و صدور لایسنس، بازاریابی چندکاناله و تولید محتوای صوتی و ویدیویی هماهنگ می‌کند.

این مخزن عمومی شامل موارد زیر است:
- کد پاک‌سازی‌شده و متن‌باز **Smart Support Bot** (`smart-support-bot/src/`) استخراج‌شده از سرویس زنده عملیاتی.
- اسکریپت‌های نصب تک‌خطی برای **سرور لینوکس** (`install.sh`) و موتور محلی **ComfyUI** روی ویندوز (`scripts/setup-comfyui.ps1`).
- مستندات معماری، امنیت و منشور اخلاقی (`ARCHITECTURE.md`، `SECURITY.md`، `CODE_OF_ETHICS.md`).

> فایل‌های نصاب اجرایی ویندوز (`.exe`) در گیت‌هاب آپلود نمی‌شوند و منحصراً از صفحه رسمی دانلود ارائه می‌گردند: [foxnext.net/fa/download.html](https://foxnext.net/fa/download.html).

---

## ۲. قابلیت‌های کلیدی

- **تیم هماهنگ ۸ ایجنت هوشمند:** هماهنگ‌کننده ارشد ناوگان، مدیر پایگاه دانش، مشاور فروش، مهندس پشتیبانی فنی، ناظر زیرساخت لینوکس، خزانه‌داری و تایید پرداخت، متخصص رشد و انتشار، و مدیر خلاقیت و صدا.
- **مکالمه صوتی دوطرفه سراسری:** دیکته پیوسته گفتار به متن، پاک‌سازی خودکار، صف پخش منظم پاسخ صوتی ایجنت‌ها، حالت هندزفری هوشمند و توقف فوری هنگام صحبت کاربر (Barge-in).
- **جستجوی وب و واکشی امن صفحات:** ابزار `web_search` (حداکثر ۱۰ نتیجه) و `fetch_webpage` با محافظت ضد-SSRF برای مسدودسازی IPهای داخلی و متادیتا.
- **پل امن دسکتاپ و `Chat-to-Config`:** ثبت رمزنگاری‌شده کلیدها و توکن‌ها از طریق کارت امن چت مستقیم به Vault (بدون ارسال به مدل هوش مصنوعی و با ماسک `[REDACTED_SECRET]`) و اجرای امن دستورات لینوکس با محدودیت دسترسی.
- **اپلیکیشن واحد دسکتاپ (`Local-First` + `ComfyUI`):** اجرای خصوصی با کلید API شخصی (BYOK)، رندر تصویر و ویدیو روی کارت گرافیک محلی و جابه‌جایی تک‌کلیکی فضای کاری با فایل رمزنگاری‌شده `.fnbackup`.

---

## ۳. مدل‌های دسترسی و تعرفه‌های شفاف

| پلن | هزینه | ایجنت‌های فعال | امکانات اصلی |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **۸ ایجنت** | سهمیه توکن روزانه و ماهانه، بونوس ۴۸ ساعت اول (یک‌بار به ازای ایمیل معتبر)، ۱ کانال سوشال (تلگرام یا اینستاگرام)، ۱ کاتالوگ، ۲۰ مگابایت فضا (فایل موقت ۷ روزه)، ۷ پست زمان‌بندی هفتگی و ۲۰ خروجی محلی ComfyUI در ماه |
| **Basic** | **`$5/mo`** (`$50/yr`) | **۸ ایجنت** | سهمیه توکن ارتقایافته ماهانه، ۱۰ کانال سوشال و کاتالوگ، ۲۰۰ مگابایت فضا، دسترسی به Cloud Media API، آزادسازی ماهانه سهمیه سالانه (`1/12`) با قابلیت ذخیره مازاد تا ۳ ماه |
| **Pro** | **`$12/mo`** (`$120/yr`) | **۸ ایجنت** | حجم بالای توکن ماهانه، اتوماسیون کامل چندکاناله و رسانه‌های ابری به همراه انتقال مازاد تا ۳ ماه |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **۸ ایجنت** | حداکثر توان پردازش ابری برای کمپین‌های سنگین، Cloud Media API و انتقال مازاد تا ۳ ماه |
| **Lifetime** | **`$49`** (یک‌بار) | **۸ ایجنت** | **۱ نصب فعال قابل انتقال** (اپلیکیشن ویندوز **یا** نصب روی VPS لینوکس + `Smart Support Bot`)، ۴۸ ساعت تست، پشتیبانی کامل BYOK و مهاجرت `.fnbackup` |

برای استفاده ابری و مدیریت اشتراک به پنل رسمی مراجعه کنید: [foxnext.online/fa/](https://foxnext.online/fa/).

---

## ۴. نصب سریع

### روش اول — اپلیکیشن یکپارچه ویندوز (`Local-First` + `ComfyUI`)

۱. نسخه رسمی ویندوز را از صفحه دانلود دریافت کنید: [foxnext.net/fa/download.html](https://foxnext.net/fa/download.html).
۲. *(اختیاری)* نصب و آماده‌سازی موتور محلی **ComfyUI** با دستور تک‌خطی زیر در PowerShell:

```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
```

### روش دوم — نصب تک‌خطی لینوکس (`Smart Support Bot`)

```bash
curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | bash
```

سپس فایل `/opt/smart-support/.env` را مطابق `.env.example` (شامل `TELEGRAM_BOT_TOKEN` و `CONTROL_PANEL_URL`) تنظیم کرده و سرویس `foxnext-smart-support` را راه‌اندازی کنید.

---

## ۵. اتصال ماژولار به پنل کنترل (`panel_conversation_hook.py`)

فایل `smart-support-bot/src/panel_conversation_hook.py` به‌صورت استاندارد و بی‌برند طراحی شده و اتصال به پنل کنترل را صرفاً از طریق متغیرهای محیطی برقرار می‌کند:

- `CONTROL_PANEL_URL`: آدرس کامل HTTP/HTTPS پنل کنترل (بدون هیچ IP یا دامنه هاردکدشده).
- `CONTROL_PANEL_TOKEN`: توکن احراز هویت اختیاری برای ارتباط ایمن Webhook.
- `CONTROL_PANEL_ROOT`: مسیر محلی اختیاری در استقرارهای یک‌پارچه.

---

## ۶. ساختار مخزن

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

## ۷. امنیت، منشور اخلاقی و مجوز

- سیاست گزارش آسیب‌پذیری و امنیت Vault: [SECURITY.md](SECURITY.md)
- اصول اخلاقی و استفاده مسئولانه: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- منتشرشده تحت مجوز [MIT License](LICENSE) — تمامی حقوق برای **Fox Next** محفوظ است (۲۰۲۶).

</div>
