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
| **`AutomationControl.exe`** | Windows | 轻量级 `Modular Shell` 桌面端，支持云端、VPS 与本地连接 |
| **`AutomationControl_LocalEngine.exe`** | Windows | 独立 `Local-First` 桌面引擎（`Lifetime $49`），含 48 小时试用与完整 `BYOK` |
| **`AutomationControl_RenderWorker.exe`** | Windows | 独立 `ComfyUI` 本地 GPU 渲染工作节点（支持 `6 GB VRAM` 硬件门禁） |
| **`automation-control-linux.tar.gz`** | Linux VPS | 洁净版自托管运行时包，由 `install.sh` 自动下载并校验 |
| **`SHA256SUMS.txt`** | 全部 | 官方发行包 `SHA-256` 完整性校验清单 |

---

## 2. 核心功能亮点

- **8 智能体与双界面模式（简洁 `Grok Bot` / 高级面板）：** 简洁模式提供三栏沉浸式对话体验，高级模式开放完整六大工作区。
- **Google OAuth 与 One Tap 一键登录：** 支持 Google 快速登录与邮箱验证，原生适配 10 种语言。
- **全局双向语音交互：** 持续多语种语音听写、有序语音播报队列、免提交互与实时语音打断（`Barge-in`）。
- **双层 `Chat-First` 私信与评论引擎：** 低消耗、响应迅速的 Instagram 与 Telegram 自动回复架构。
- **3 层 Token 优化记忆系统：** 自动压缩对话历史、整合品牌知识库并精简上下文。
- **无浏览器 `cPanel / SSH / SFTP` 与商务中枢：** 直连服务器（用后立即清除临时凭据），并支持有无独立网站均可使用的商店、库存与财务管理。
- **统一 Windows 客户端与邮箱授权自动路由：** 单一轻量 `AutomationControl.exe`（约 29 MB），采用明亮的 `foxnext.online` 主题，支持登录后自动分流、VPS 严格在线授权验证及按需下载 `ComfyUI`/`FFmpeg`。
- **双槽位单端唯一会话策略（`Web + Desktop`）：** 全版本（`Free` 至 `Lifetime`）统一支持同时保留 **1 个活跃 Web 会话 + 1 个活跃桌面端会话**；同平台新登录仅自动替换该平台先前的会话，互不干扰。
- **多显卡加速（`NVIDIA CUDA`、`AMD ROCm/DirectML`、`Intel Arc`）：** 自动枚举全部 GPU（`>= 6 GB VRAM`）并支持设置内手动切换显卡。
- **设置 → 工具与 MCP 管理（`find_tools`）：** 查看 8 位智能体内置工具权限，并在桌面端/自托管模式添加、启停与测试自定义 MCP 服务器（云端网页保持 32 KB 沙箱限制），智能体可自动发现并调用。
- **仪表板智能分析双引擎（网站 + 多账号 Instagram）：** 并排支持网站只读诊断报告与 Instagram 账号分析，支持多目标选择器并将 Instagram 报告一键发送给智能体创作或存入品牌记忆。
- **超级管理员 SaaS 中心与云端配额圆环：** 集中管理用户与配额、实时定价策略、活动横幅、5 个 API 池及云端用户百分比进度环。
- **桌面端本地 `MCP / Skills / Plugins` 与 `Local-First`：** 桌面端与 Linux 原生支持本地插件/技能扩展、加密 Vault、`.fnbackup` 迁移、`BYOK` 与本地 `ComfyUI` GPU 渲染。

---

## 3. 版本与透明方案

| 方案 | 价格 | 启用智能体 | 核心权益 |
| :--- | :--- | :--- | :--- |
| **Free** | **`$0`** | **8 位智能体** | 基础每日/每月 Token 额度 + 48 小时迎新加赠、1 个社交渠道、1 个目录、20 MB 空间、本地 `ComfyUI` |
| **Basic** | **`$5/mo`** (`$50/yr`) | **8 位智能体** | 更高月度额度、10 个社交渠道与目录、200 MB 空间、云端媒体 API + 最长 3 个月额度顺延 |
| **Pro** | **`$12/mo`** (`$120/yr`) | **8 位智能体** | 大容量月度额度、全渠道与云端媒体自动化 + 最长 3 个月额度顺延 |
| **Pro Plus** | **`$19/mo`** (`$190/yr`) | **8 位智能体** | 面向团队与高频活动的最大云端吞吐量 + 最长 3 个月额度顺延 |
| **Lifetime** | **`$49`** (买断) | **8 位智能体** | **1 台可迁移活跃授权**（Windows 桌面引擎 `AutomationControl_LocalEngine.exe` **或** Linux VPS + Smart Support Bot）、48 小时试用、`BYOK`、`.fnbackup` |

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
- 基于 [MIT License](LICENSE) 开源 — Copyright © 2026 **Fox Next**。
