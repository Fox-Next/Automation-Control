[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<div dir="rtl" align="right">

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control v3.0.0 — محصول شرکت Fox Next</h1>

<p align="center">
  <strong>پلتفرم هماهنگی ۸ ایجنت هوشمند، اپلیکیشن دسکتاپ یکپارچه Local-First و ربات متن‌باز Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/fa/">وب‌سایت رسمی</a> •
  <a href="https://foxnext.net/fa/download.html">صفحه دانلود (foxnext.net)</a> •
  <a href="https://github.com/Fox-Next/Automation-Control/releases/latest">گیت‌هاب ریلیز (v3.0.0)</a> •
  <a href="https://foxnext.online/fa/">پنل ابری کنترل</a> •
  <a href="ARCHITECTURE.md">معماری سیستم</a> •
  <a href="SECURITY.md">امنیت</a>
</p>

---

## ۱. معرفی و بسته‌های انتشار رسمی (`v3.0.0`)

نرم‌افزار **Automation Control** (ساخت شرکت **Fox Next**) تیمی شامل **۸ ایجنت هوش مصنوعی تخصصی** را برای فروش، پشتیبانی فنی چندسکویی، عملیات سرور لینوکس، تایید مالی و لایسنس، بازاریابی چندکاناله و استودیوی خلاقیت هماهنگ می‌کند.

تمامی فایل‌های رسمی نسخه `v3.0.0` همراه با فایل اصالت‌سنجی `SHA256SUMS.txt` در **[GitHub Releases](https://github.com/Fox-Next/Automation-Control/releases/latest)** و **[foxnext.net/fa/download.html](https://foxnext.net/fa/download.html)** منتشر شده‌اند:

| بسته نصبی | پلتفرم | توضیح |
| :--- | :--- | :--- |
| **`AutomationControl.exe`** | ویندوز | اپلیکیشن واحد یکپارچه (~۲۹ مگابایت) با تم روشن `foxnext.online`، مسیریابی ایمیلی پس از نصب (`Cloud` / `VPS` / `Local Engine`)، گیت `connect_vps_strict`، ورکر چندگرافیکه (`>= 6 GB VRAM`) و دریافت در زمان نیاز `ComfyUI` و `FFmpeg` |
| **`automation-control-linux.tar.gz`** | لینوکس VPS | بسته تمیز Self-Hosted لینوکس برای دانلود خودکار توسط `install.sh` |
| **`SHA256SUMS.txt`** | همه | فهرست هش‌های رمزینه `SHA-256` برای تایید اصالت همه بسته‌ها |

---

## ۲. قابلیت‌های کلیدی نسخه نهایی

- **تیم ۸ ایجنت با دو حالت ساده (`Grok Bot`) و پیشرفته:** رابط چت‌محور ۳ستونه تمام‌صفحه در حالت ساده و پنل ۶تبه کامل در حالت پیشرفته.
- **ورود با گوگل (`Google OAuth`) و `One Tap`:** احراز هویت سریع در کنار ورود با ایمیل، تایید کد امنیتی و پشتیبانی کامل از ۱۰ زبان.
- **نوار خلوت چت، دیکته اکولایزردار و حالت مکالمه صوتی زنده ربات مرکزصفحه:** دسته‌بندی تمام ابزارها و پلی‌بوک‌ها درون ۳ منوی کشویی بومی‌شده (`ابزارها و گفتگو`، `شروع سریع و اتصالات`، `کارهای آماده`) در جهت‌های LTR/RTL، نوار کامپوزر کاملاً آیکون‌محور همراه با اکولایزر ۴میله‌ای دیکته صوتی (درج متن در کادر بدون ارسال خودکار)، و دکمه سبز گفتگوی زنده دوطرفه که ربات مسکات را با پس‌زمینه بلور و چشمان آبی درخشان `#38bdf8` به مرکز صفحه می‌آورد و همگام با پاسخ صوتی ایجنت اکولایزر زنده اجرا می‌کند.
- **موتور دولایه پاسخگویی دایرکت و کامنت (`Chat-First`):** پردازش بهینه پیام‌های اینستاگرام و تلگرام با کمترین مصرف توکن.
- **حافظه ۳لایه هوشمند:** فشرده‌سازی خودکار حافظه، دانش برند و مدیریت بهینه کانتکست برای حفظ کیفیت و کاهش مصرف توکن.
- **اتصال بدون مرورگر `cPanel / SSH / SFTP` و هاب مالی/فروشگاهی:** اتصال مستقیم و سبک با پاک‌سازی فوری رمزهای موقت + مدیریت فروشگاه، سفارش و انبارداری (هم با سایت و هم بدون سایت).
- **اپلیکیشن واحد یکپارچه ویندوز با مسیریابی ایمیلی لایسنس:** تک‌فایل سبک `AutomationControl.exe` با تم روشن `foxnext.online`، تشخیص خودکار لایسنس ایمیلی پس از نصب، گیت آنلاین اجباری لایسنس VPS و دانلود در زمان نیاز `ComfyUI`/`FFmpeg`.
- **سیاست نشست دوگانه تفکیک‌شده (`Web + Desktop`):** در تمامی پلن‌ها (`Free` تا `Lifetime`) حداکثر **۱ نشست فعال وب + ۱ نشست فعال دسکتاپ** هم‌زمان مجاز است؛ ورود با مرورگر دوم یا دستگاه دسکتاپ دوم فقط نشست قبلی همان پلتفرم را جایگزین می‌کند و نشست پلتفرم دیگر قطع نمی‌شود.
- **پشتیبانی چندگرافیکه `CUDA`، `ROCm` و `DirectML`:** شناسایی هم‌زمان تمام گرافیک‌ها (`NVIDIA` ← `CUDA`/`NVENC`، `AMD Radeon` ← `ROCm`/`DirectML` + `AMF`، `Intel Arc`) با حداقل `6 GB VRAM` و انتخاب دستی GPU در تنظیمات.
- **مدیریت خودکار ابزارها و `MCP` (`find_tools` و `register_tool_or_mcp`):** هر ۸ ایجنت به‌صورت خودکار ابزارها را کشف، ثبت و اجرا می‌کنند؛ نسخه دسکتاپ و سرور شخصی امکان ثبت کامل سرورهای `MCP` را دارد و در کلود مشترک، ثبت ابزار صرفاً به وب‌هوک‌ها و APIهای امن `https://` در فضای ایزوله هر مستاجر محدود می‌شود.
- **معماری دولایه `AI`، پیش‌فرض `Max Tokens = Unlimited (0)` و پرامپت‌های بومی‌سازی‌شده ۸ ایجنت:** کاربران ابری تنظیمات شخصی (`BYOK`) هر ایجنت را به‌صورت ایزوله و بدون افشای کلید یا بودجه سوپرادمین ذخیره می‌کنند؛ هر ۸ ایجنت از پرامپت‌های خنثی متناسب با زبان فعال پنل بهره می‌برند و پیش‌فرض سقف توکن خروجی روی `Unlimited` (`0`) تنظیم شده است.
- **رابط ۱۰زبانه بدون فلش پیش‌رندر، آواتار گوگل و ۱۵ راهنمای `?`:** رندر فوری LTR/RTL پیش از نقاشی صفحه (`i18n-prepaint`)، قفل `MutationObserver` با دیبانس ۹۰ میلی‌ثانیه‌ای بدون لوپ، نمایش دایره‌ای آواتار گوگل در هدر و منو، و ۱۵ دکمه راهنمای `?` در همه تب‌ها و پنل‌های تنظیمات.
- **سهمیه روزانه/هفتگی به سبک ChatGPT، شمارش معکوس ریست و مالی فقط‌خواندنی با فیلتر پیامک شتاب:** تعریف و ویرایش سقف مصرف روزانه (`daily_token_cap`) و هفتگی (`weekly_token_cap`) برای پلن‌های ابری همراه با نوارهای پیشرفت و شمارش معکوس ریست (`Resets in ...`) بدون افشای عدد خام توکن، خطای مودبانه `HTTP 429`، و پنل مالی فقط‌خواندنی (بدون امکان برداشت وجه) با فیلتر ضد خطای پیامک‌های تبلیغاتی شتاب.
- **حاکمیت سلسله‌مراتبی سوپرادمین، همگام‌سازی زنده `Annual USD` و `Storage MB`، شارژ دلاری `$1–$10` و لاگ ممیزی:** تفکیک سوپرادمین اصلی (`#1` پین‌شده و غیرقابل حذف) و سوپرادمین ثانویه با گیت `Email OTP + Reason`، شاخص زنده `Online Now`، صفحه‌بندی ۱۰تایی و مرتب‌سازی، ویرایشگر زنده `Plans & Pricing` (شامل `Annual USD`، `Daily Cap`، `Weekly Cap` و `Storage MB` متصل به اعمال آنی سقف `HTTP 413` آپلود و `/api/public/pricing` بدون ری‌استارت)، شارژ دلاری پویا `$1–$10`، مودال لاگ ممیزی جدولی (`update_pricing_policy` بدون کلید خام)، کمپین ۲ردیفه (`Publish Immediately` + تقویم میلادی)، استخرهای ۵گانه تمام‌عرض و تست اتصال/عیب‌یابی ۱۰زبانه.
- **مجوزهای پروفایل، تغییر رمز دوعاملی و `Danger Zone` حذف اختیاری حساب:** نمایش مجوزهای واقعی پلن، تغییر رمز با کد ایمیل (`OTP`) و `Turnstile/Captcha` و امکان حذف اختیاری حساب توسط کاربر از کارت `Danger Zone` پروفایل با ابطال آنی نشست‌های وب و دسکتاپ.
- **اکوسیستم محلی `MCP / Skills / Plugins` و `Local-First`:** اجرای مستقل روی دسکتاپ و لینوکس با Vault رمزنگاری‌شده، کلید شخصی (`BYOK`)، بکاپ `.fnbackup` و رندر محلی `ComfyUI`.

---

## ۳. پلن‌ها و نسخه‌ها

| پلن | قیمت | ایجنت‌های فعال | امکانات کلیدی |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **۸ ایجنت** | سهمیه پایه توکن + بونوس خوشامدگویی ۴۸ ساعته (ایمیل معتبر)، ۱ کانال سوشال، ۱ کاتالوگ، ۲۰ مگابایت فضا، پشتیبانی `ComfyUI` محلی |
| **Basic** | **`$5/mo`** (`$50/yr`) | **۸ ایجنت** | سهمیه ماهانه ارتقایافته، ۱۰ کانال سوشال و کاتالوگ، ۲۰۰ مگابایت فضا، `Cloud Media API` فعال و ذخیره مازاد تا ۳ ماه |
| **Pro** | **`$12/mo`** (`$120/yr`) | **۸ ایجنت** | سهمیه بالای ماهانه، اتوماسیون کامل چندکاناله و رسانه‌های ابری به همراه انتقال مازاد تا ۳ ماه |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **۸ ایجنت** | بیشترین ظرفیت پردازش ابری برای تیم‌ها و کمپین‌های سنگین به همراه انتقال مازاد تا ۳ ماه |
| **Lifetime** | **`$49`** (یک‌بار) | **۸ ایجنت** | **۱ نصب فعال قابل انتقال** (اپلیکیشن واحد `AutomationControl.exe` در حالت `Local Engine` روی ویندوز **یا** سرور لینوکس + ربات پشتیبانی)، ۴۸ ساعت تست، پشتیبانی کامل `BYOK` و مهاجرت `.fnbackup` |

---

## ۴. دستورهای نصب تک‌خطی رسمی

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

## ۵. اتصال ماژولار به پنل (`panel_conversation_hook.py`)

فایل `smart-support-bot/src/panel_conversation_hook.py` اتصال ایمن با پنل را صرفاً از طریق متغیرهای محیطی (`CONTROL_PANEL_URL`، `CONTROL_PANEL_TOKEN`، `CONTROL_PANEL_ROOT`) برقرار می‌کند.

---

## ۶. ساختار مخزن

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

## ۷. امنیت، اصول اخلاقی و مجوز

- سیاست امنیت و Vault: [SECURITY.md](SECURITY.md)
- منشور اخلاقی هوش مصنوعی: [CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- راهنمای معماری: [ARCHITECTURE.md](ARCHITECTURE.md)
- منتشرشده تحت مجوز [MIT License](LICENSE) — © 2026 **Fox Next**.

</div>
