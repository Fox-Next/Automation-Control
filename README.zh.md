[English](README.md) | [فارسی](README.fa.md) | [Deutsch](README.de.md) | [Русский](README.ru.md) | [简体中文](README.zh.md)

<p align="center">
  <img src="assets/foxnext-logo.png" alt="Fox Next Logo" width="88" />
</p>

<h1 align="center">Automation Control — Fox Next 出品</h1>

<p align="center">
  <strong>8 智能体协同自动化平台、Local-First 统一桌面应用与开源 Smart Support Bot</strong>
</p>

<p align="center">
  <a href="https://foxnext.net/zh/">官方网站</a> •
  <a href="https://foxnext.net/zh/download.html">下载 Windows 客户端</a> •
  <a href="https://foxnext.online/zh/">云端控制面板</a> •
  <a href="ARCHITECTURE.md">系统架构</a> •
  <a href="SECURITY.md">安全策略</a>
</p>

---

## 1. 项目简介

**Automation Control**（由 **Fox Next** 开发）协同调度 **8 位专业 AI 智能体**，覆盖客户销售咨询、多平台技术支持、Linux 运维监控、财务核验与授权管理、全渠道社媒营销以及音视频创意制作。

本开源仓库包含：
- 从生产环境严格脱敏提取的 **Smart Support Bot** 源码（`smart-support-bot/src/`）。
- 适用于 **Linux VPS** 的一键安装脚本（`install.sh`）以及 Windows 本地 **ComfyUI** 一键部署脚本（`scripts/setup-comfyui.ps1`）。
- 系统架构、安全防护与伦理规范文档（`ARCHITECTURE.md`、`SECURITY.md`、`CODE_OF_ETHICS.md`）。

> Windows 安装程序（`.exe`）不会上传至 Git 仓库，仅通过官方下载页发布：[foxnext.net/zh/download.html](https://foxnext.net/zh/download.html)。

---

## 2. 核心功能

- **8 智能体协同体系：** 总控调度、知识库与目录同步、销售顾问、技术支持工程师、Linux 平台运维、财务与订单核验、全渠道增长发布、创意音频与视频导演。
- **全局双向语音交互：** 连续语音听写输入、智能口语整理、有序语音播报队列、免提静音检测以及实时语音打断（Barge-in）。
- **网页搜索与抗 SSRF 抓取：** 受控网页检索（每次最多 10 条结果）及网络边界防护抓取，自动拦截私有网段和元数据地址。
- **安全桌面桥接与 `Chat-to-Config`：** 聊天内嵌安全凭据卡片直接写入加密 Vault（发送至模型前自动脱敏为 `[REDACTED_SECRET]`），并对 SSH 桥接实行严格角色权限隔离。
- **统一桌面应用（`Local-First` + `ComfyUI`）：** 支持自有 API 密钥（BYOK）与本地显卡图像/视频生成，并支持一键生成加密 `.fnbackup` 工作区迁移包。

---

## 3. 透明版本与定价方案

| 方案 | 价格 | 启用智能体 | 核心权益 |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 位智能体** | 每日与每月 Token 额度、首 48 小时迎新加赠（限实名非一次性邮箱）、1 个社交渠道（Telegram/Instagram）、1 个商品目录、20 MB 存储（临时媒体保留 7 天）、每周 7 条定时发布、每月 20 次本地 ComfyUI 生成 |
| **Basic** | **`$5/mo`**（`$50/yr`） | **8 位智能体** | 更高月度 Token 额度、10 个社交渠道与目录、200 MB 存储、开启云端媒体 API、年付按月（`1/12`）释放额度且未用部分最多顺延 3 个月 |
| **Pro** | **`$12/mo`**（`$120/yr`） | **8 位智能体** | 大容量月度 Token、全功能多渠道发布与云端媒体自动化，未使用额度最多顺延 3 个月 |
| **Pro Plus** | **`$19/mo`**（`$190/yr`） | **8 位智能体** | 面向高频团队与重度营销活动的最大云端吞吐量，支持云端媒体 API 及最长 3 个月额度顺延 |
| **Lifetime** | **`$49`**（一次性） | **8 位智能体** | **1 台可迁移活跃设备授权**（Windows 桌面端 **或** Linux VPS + `Smart Support Bot`）、48 小时试用、完整 BYOK 模式与 `.fnbackup` 加密迁移 |

访问云端控制面板管理订阅：[foxnext.online/zh/](https://foxnext.online/zh/)。

---

## 4. 快速安装

### 方式 A — Windows 统一桌面客户端（`Local-First` + `ComfyUI`）

1. 前往官方下载页获取 Windows 安装程序：[foxnext.net/zh/download.html](https://foxnext.net/zh/download.html)。
2. *（可选）* 在 PowerShell 中一键安装并接入本地 **ComfyUI** 渲染节点：

```powershell
irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
```

### 方式 B — Linux VPS 一键部署（`Smart Support Bot`）

```bash
curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | bash
```

随后参照 `.env.example` 配置 `/opt/smart-support/.env`（填写 `TELEGRAM_BOT_TOKEN` 与 `CONTROL_PANEL_URL`），并启动 `foxnext-smart-support` 系统服务。

---

## 5. 控制面板集成（`panel_conversation_hook.py`）

`smart-support-bot/src/panel_conversation_hook.py` 仅通过标准环境变量与控制面板对接，不包含任何硬编码地址或旧品牌标识：

- `CONTROL_PANEL_URL`：控制面板 HTTP/HTTPS 根地址。
- `CONTROL_PANEL_TOKEN`：可选的中继鉴权令牌。
- `CONTROL_PANEL_ROOT`：同机部署时的可选本地路径。

---

## 6. 仓库目录结构

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

## 7. 安全、伦理与开源许可

- 漏洞披露与 Vault 安全隔离规范：[SECURITY.md](SECURITY.md)
- 负责任的 AI 与反滥用原则：[CODE_OF_ETHICS.md](CODE_OF_ETHICS.md)
- 本项目基于 [MIT License](LICENSE) 开源发布 — Copyright © 2026 **Fox Next**。
