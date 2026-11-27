[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control v3.0.0 — Fox Next 出品</h1>

<p align="center">
  <strong>8 智能体协同平台、Local-First 统一桌面客户端与开源 Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/zh/">官方网站</a> •
  <a href="https://foxnext.net/zh/download.html">下载中心 (foxnext.net)</a> •
  <a href="https://github.com/Fox-Next/Automation-Control/releases/latest">GitHub Releases (v3.0.0)</a> •
  <a href="https://foxnext.online/zh/">云端控制面板</a> •
  <a href="ARCHITECTURE.md">系统架构</a> •
  <a href="SECURITY.md">安全策略</a>
</p>

---

## 1. 概述与官方发行包 (`v3.0.0`)

**Automation Control**（由 **Fox Next** 开发）协同调度 **8 位专业 AI 智能体**，涵盖销售转化、多平台技术支持、Linux 运维监控、财务与授权核验、全渠道社媒推广及创意媒体生成。

所有经过校验的 `v3.0.0` 官方安装程序与 `SHA256SUMS.txt` 均发布于 **[GitHub Releases](https://github.com/Fox-Next/Automation-Control/releases/latest)** 与 **[foxnext.net/zh/download.html](https://foxnext.net/zh/download.html)**：

| 发行文件 | 适用系统 | 说明 |
| :--- | :--- | :--- |
| **`AutomationControl.exe`** | Windows | 统一 Windows 客户端（约 29 MB），采用明亮 `foxnext.online` 主题，登录后自动分流（`Cloud` / `VPS` / `Local Engine`）、`connect_vps_strict` 验证与多显卡后台渲染（`>= 6 GB VRAM`，按需下载 `ComfyUI`/`FFmpeg`） |
| **`automation-control-linux.tar.gz`** | Linux VPS | 洁净版自托管运行时包，由 `install.sh` 自动下载并校验 |
| **`SHA256SUMS.txt`** | 全部 | 官方发行包 `SHA-256` 完整性校验清单 |

---

## 2. 核心功能亮点

- **8 智能体与双界面模式（简洁 `Grok Bot` / 高级面板）：** 简洁模式提供三栏沉浸式对话体验，高级模式开放完整六大工作区。
- **Google OAuth 与 One Tap 一键登录：** 支持 Google 快速登录与邮箱验证，原生适配 10 种语言。
- **精简聊天栏、会议室实时语音与统一折叠 Swarm 表格：** 3 个多语言下拉菜单（`工具与对话`、`快速设置`、`预设任务`），纯图标输入栏配 4 柱动态听写均衡器（不自动发送），单聊与智能体会议室均支持绿色实时语音模式（居中 `#38bdf8` 发光蓝眼机器吉祥物 + 背景模糊 + `Escape` 退出），并新增默认折叠的统一 Swarm 协调分页表格（按最新时间置顶、每页 10 条、多选删除及一键发送到会议室）。
- **双层 `Chat-First` 私信与评论引擎：** 低消耗、响应迅速的 Instagram 与 Telegram 自动回复架构。
- **3 层 Token 优化记忆系统：** 自动压缩对话历史、整合品牌知识库并精简上下文。
- **无浏览器 `cPanel / SSH / SFTP` 与商务中枢：** 直连服务器（用后立即清除临时凭据），并支持有无独立网站均可使用的商店、库存与财务管理。
- **统一 Windows 客户端与邮箱授权自动路由：** 单一轻量 `AutomationControl.exe`（约 29 MB），采用明亮的 `foxnext.online` 主题，支持登录后自动分流、VPS 严格在线授权验证及按需下载 `ComfyUI`/`FFmpeg`。
- **双槽位单端唯一会话策略（`Web + Desktop`）：** 全版本（`Free` 至 `Lifetime`）统一支持同时保留 **1 个活跃 Web 会话 + 1 个活跃桌面端会话**；同平台新登录仅自动替换该平台先前的会话，互不干扰。
- **多显卡加速（`NVIDIA CUDA`、`AMD ROCm/DirectML`、`Intel Arc`）：** 自动枚举全部 GPU（`>= 6 GB VRAM`）并支持设置内手动切换显卡。
- **设置 → 工具与 MCP 管理（`find_tools` 与 `register_tool_or_mcp`）：** 全部 8 位智能体可自主发现、注册并调用工具；桌面端与自托管模式支持自定义 MCP 服务器，共享云端仅允许租户隔离的安全 `https://` Webhook/API 工具（保留 32 KB 输出上限）。
- **两层 AI 配置继承、BYOK 云端配额全免、`Studio` 默认主题与即时 GDPR 清理：** 干净的自定义智能体创建弹窗（配备免费 Google AI Studio 密钥 `?` 指南），个人密钥加密保存（`enc:v1:`）并在单聊、会议室及创意工作室享受 **0 云端令牌扣减**；8 位核心智能体规则全面实现 10 语言品牌中性化与大尺寸多行编辑弹窗，支持磁盘级永久清除对话历史，提供 16 处 `?` 上下文帮助，并在 OTP 确认注销账号后立即物理清理租户工作区目录。
- **零闪烁 10 语言界面、Google 头像显示与 16 处 `?` 上下文帮助提示：** 基于 `<head>` 预渲染引导的零延迟语言切换（`i18n-prepaint`）、带防抖与重入锁的 DOM 翻译引擎（`window.__bfI18nTranslating`）、顶栏圆形 Google 头像呈现，以及覆盖全部 6 大标签页与 7 个设置面板的 `?` 帮助弹窗。
- **每日/每周用量上限与倒计时进度条 + 只读财务监控中心：** 支持在超级管理员面板实时配置云端各套餐每日与每周用量上限（`daily_token_cap`、`weekly_token_cap`），仪表盘展示百分比与重置倒计时进度条（不暴露原始 Token 数量），超限返回友好升级提示（`HTTP 429`）；财务面板保持严格只读核验，无任何对外转账或提现入口。
- **超级管理员分层治理、实时 `Annual USD` 与 `Storage MB` 配额、`$1–$10` 充值与 Danger Zone：** 区分主超管（置顶第 1 行、不可删除）与次级超管（`Email OTP + 原因`双重校验）、实时在线指标（`Online Now`）、10 行分页排序、支持实时修改并立即生效的 `Plans & Pricing`（`Monthly USD`、`Annual USD`、`Daily Cap`、`Weekly Cap`、`Tokens / mo`、`Storage MB` 无需重启即同步 `HTTP 413` 上传上限与 `/api/public/pricing`）、动态 `$1–$10` 额度充值、不含明文密钥的表格化审计日志（`update_pricing_policy`）、两行布局活动模式（`Publish Immediately` 与日期选择器）、全宽 5 大云端 API 池、10 语言诊断与连接测试，以及个人资料 Danger Zone 邮箱 OTP 自助注销账号（立即吊销 Web 与桌面端会话）。
- **交互式 `Spotlight` 流程图、8 大社交发布网关、移动端自适应与 `Meta Cross-Posting` 去重（`∞ Meta`）：** 静态模式下连线保持微弱透明（`0.10`），悬停或点击节点时仅高亮相关流向并淡化无关节点（`0.28`），在节点上方自动避障排布零重叠连接标签；支持全部 8 个输出网关（`Telegram`、`Instagram`、`Facebook`、`WhatsApp`、`YouTube`、`LinkedIn`、`X`、`Reddit`）及 Brand Brain 动态站点；未配置网关严格拦截启用（前端禁用并跳转 `设置 → 社交媒体`，后端返回 `HTTP 400 gateway_not_configured`）；移动端（`<= 768px`）自动隐藏画布仅显示底部状态卡片；启用 Meta 账户中心跨平台发布后节点下方显示 `∞ Meta` 标识，仅向主发布渠道发送 API 请求（私信与评论回复保持 100% 独立）。
- **移动端 `70%` 抽屉、`UUID` 引用回复、中央文件注册表与 `HTTP 206` 媒体预览：** 适配移动端（`<= 768px`）侧滑抽屉、消息 `UUID` 回复定位高亮、多租户隔离 `FileRegistry` 与 `SVG` 脚本清理及字节范围音视频模态预览（`media_preview.js`）。
- **统一 `StorageManager`（`Google Drive drive.file`、`Cloudflare R2` 与本地存储）：** 最小权限 `drive.file` OAuth 加密托管（`enc:v1:`）、断点直传、格式优化与发布保护清理周期。
- **四层混合 `MemoryManager` 与可编辑 `Timeline Manifest` 时间线：** 基于 `SQLite FTS5` + 64 维向量的隔离记忆系统（支持防注入、`HTTP 422` 密钥拦截与版本恢复），以及多场景视频时间线（`style_bible` 视觉连贯性、单场景重生成、云端 CPU 防护与 `ffprobe`/`blackdetect` 质检）。
- **Google One Tap 登录、强制条款确认门禁、Aikido 安全头与本地自托管字体：** 支持 `foxnext.online` 与 `app.foxnext.online` 跨域 `One Tap`、一次性 `terms_accepted_at` 门禁校验（未确认返回 `403 terms_not_accepted` 并弹出 `#modalMandatoryTermsGate`）、`HSTS`/`XFO: DENY`/`CSP` 安全响应头及 35 个本地 `.woff2` 字体文件（零外部 CDN 请求）。
- **5 小时滚动配额上限、12 字段云端媒体池与实时汇率编辑器：** 超级管理员两倍宽（`span 2`）3×4 图像/音频/视频媒体池（Fernet 加密并直连 `HybridComputeRouter`）、单行对齐状态徽章、滚动 **5 小时配额** 进度条（不暴露原始 Token 数）及实时托曼汇率编辑器（默认 `275,000`）。
- **高并发全渠道电商（`70+` 并发客户）、通用付款凭证 OCR 与端到端履约闭环：** 基于 SQLite `WAL` 的多租户隔离会话引擎（横跨 Telegram、Instagram、WhatsApp 与 Facebook，保留 `168` 小时上下文）并通过 `70+` 并发压测零锁死；多模态 OCR 与仅限已连接网关的只读核验（`BEP-20`/`TRC-20`/`TON` 链上交易及 `Dodo Payments`、`Stripe`、`PayPal`、`Visa/Mastercard` 只读 `GET` 查询，严禁对外转账）；基于品牌知识库的拟人化 `Comment-to-DM` 转私信以及实体订单（地址与 10 位邮编校验）与数字授权（`FulfillmentService` 自动发卡）闭环。
- **Shahla 专业创意工作室（`bf_creative` 授权 7 大工具）：** 自动抓取品牌配色与网页灵感（`fetch_webpage`、`web_search`）、受严格跨租户 `HTTP 403` 隔离保护的商品/徽标参考图合成（`edit_reference_image`）、基于 `Pillow` + `arabic-reshaper` + `python-bidi` 的高清 RTL/LTR 文字与 CTA 排版图层（彻底消除 AI 乱码文字）、一键导出注册至 `FileRegistry` 的 `9:16` · `1:1` · `16:9` 多比例素材包、受云端 CPU 防护保护的 `.srt`/`.ass` 同步字幕生成以及最多限制 `1` 次自动重试的视觉自检 QA 门禁。
- **移动端极简模式锁定、顶部资料弹窗置顶、真实机器人检测与内联 Meta 同步选项：** 小于等于 `768px` 视口强制锁定 `Simple Mode` 并提供三段式 `70vw` 右侧抽屉（固定底部 `#mobileDrawerProfileFooter` 与三标签 `#mobileSettingsModal` 分类设置）；`#headerUserDropdownMenu` 通过 Portal 置顶（`z-index: 10550`）解决遮挡；订单表升级为紧凑换行布局并清理测试残留，同时移除 1 小时试用开关；全平台自动识别并使用客户消息语言回复；`Smart Support Bot` 经真实 `Telegram getMe` 探测反馈状态并锁定绑定销售专员；Instagram、Facebook 与 WhatsApp 表单内直接集成专属内联 `Meta` 关联与主发布者互斥复选框（`?v=5.4.0`）。
- **免费版 BYOK 封锁、双自定义智能体 5 层沙盒、付费 Mamali 自愈、多站点抓取与 80%/90% 自动清理：** 免费版严格禁止填写个人 BYOK 密钥（后端返回 `HTTP 403`，UI 锁定并显示升级提示），付费版（`Basic+`）正常可用；每位租户最多创建 `2/2` 个自定义智能体并受 5 层 `HARD DENY` 沙盒隔离（严禁基础设施、财务/授权、核心管理、直接发布/批量删除及隐私记忆域）；Mamali（`bf_platform`）面向付费用户开放 `web_search`、租户自愈、反 `SSRF` 主机黑名单、`HTTP 428` 人工确认门禁、自动 `.bak` 备份与 `Fernet enc:v1:` 加密；Asghar（`bf_support`）支持多站点共享预算爬虫（`25/100/400/600/1500` 页与 `site_domain` 标记）及无官网社媒知识抓取；全部 8 位智能体上传均启用可执行/宏/魔数拦截及四重防护 `ZIP` 安全解压（`safe_ingest.py`）；存储达 `>= 80%` 自动清理并保护固定/可编辑/目录资产，达 `>= 90%` 触发 `#storageCriticalAlertBanner` 警报（目标 `< 60%`）。
- **桌面端本地 `MCP / Skills / Plugins` 与 `Local-First`：** 桌面端与 Linux 原生支持本地插件/技能扩展、加密 Vault、`.fnbackup` 迁移、`BYOK` 与本地 `ComfyUI` GPU 渲染。
- **应用安全全面加固（`Phase 22-C`）：** 锁定已修复 CVE 的安全依赖（`fastapi`、`starlette`、`pillow`、`cryptography`、`jinja2`、`python-multipart`、`defusedxml`、`pyinstaller`），启用严格 Jinja2 `autoescape`，全面改用 `defusedxml` 解析 SVG/XML，强制执行 SSH 主机密钥校验（`known_hosts` / `RejectPolicy()`），彻底移除 `document.write`/`innerHTML`，严防 `TAR` 符号链接与路径穿越，增加出站 SSRF 与路径包含校验，并在 CI 中启用 `persist-credentials: false` 及移除生产环境 `assert`。
- **智能高管会议室、多智能体语音圆桌、监督式路线图与跨模型本地向量记忆（`Phase 23`）：** `Titil` 自动分析目标并仅激活相关专家（区分 `会议中` 与变暗的 `待命` 状态），支持按发言顺序切换各智能体专属音色的语音圆桌会议（含头像脉冲动画 `gv:speakerChanged` 与实时字幕），生成持久化分类 `可执行路线图`（`workspaces/{user_id}/roadmaps.db`，支持单步与全流程真实委托并自动勾选 `✅ 已完成`），并通过本地 `SQLite FTS5` + 64 维向量记忆保证在任意套餐下切换 API 密钥、服务商或模型后记忆与进度 `100%` 零丢失。
- **六站点全流程 Playwright QA 巡检与国际化 SaaS 界面精简（`Phase 24`）：** 通过涵盖 6 大站点 × 3 种角色 × 2 种视口 × 2 种语言的自动化浏览器巡检以及 OpenAPI 与 `onclick` 契约校验（`scripts/qa_full_crawl.py`，`0` 错误）；对齐 10 种语言与 8 大社交平台首行表单，彻底分离界面日历/徽章与对话语言，全面本地化工具桥与记忆弹窗并默认开启 `Auto-Memory = ON`，打通全部 5 项 `Quick Setup` 快捷设置并清理 10 种语言中的开发术语（`?v=5.6.0`）。

---

## 3. 版本与透明方案

| 方案 | 价格 | 启用智能体 | 核心权益 |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 位智能体** | 基础每日/每月 Token 额度 + 48 小时迎新加赠、1 个社交渠道、1 个目录、20 MB 空间、本地 `ComfyUI` |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 位智能体** | 更高月度额度、10 个社交渠道与目录、200 MB 空间、云端媒体 API + 最长 3 个月额度顺延 |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 位智能体** | 大容量月度额度、全渠道与云端媒体自动化 + 最长 3 个月额度顺延 |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 位智能体** | 面向团队与高频活动的最大云端吞吐量 + 最长 3 个月额度顺延 |
| **Lifetime** | **`$49`** (买断) | **8 位智能体** | **1 台可迁移活跃授权**（统一客户端 `AutomationControl.exe` 本地 `Local Engine` 模式 **或** Linux VPS + Smart Support Bot）、48 小时试用、`BYOK`、`.fnbackup` |

---

## 4. 一键安装命令

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

## 5. 控制面板对接 (`panel_conversation_hook.py`)

`smart-support-bot/src/panel_conversation_hook.py` 仅通过环境变量（`CONTROL_PANEL_URL`、`CONTROL_PANEL_TOKEN`、`CONTROL_PANEL_ROOT`）连接控制面板。

---

## 6. 仓库目录结构

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

## 7. 安全、伦理与开源许可

- 安全与 Vault 规范：[SECURITY.md](SECURITY.md)
- 负责任的 AI 准则：[CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- 系统架构文档：[ARCHITECTURE.md](ARCHITECTURE.md)
- Copyright © 2026 **Fox Next**。
