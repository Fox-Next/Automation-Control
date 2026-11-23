# ==============================================================================
# Fox Next — Automation Control: Windows Smart Support Bot One-Line Installer
# Downloads clean smart-support-bot/ source from Fox-Next/Automation-Control,
# creates Python .venv, installs requirements.txt, initializes .env, and adds shortcuts.
# Usage: irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/install-smart-support-bot.ps1 | iex
# ==============================================================================
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\FoxNext\SmartSupportBot",
    [string]$RepoUrl = "https://github.com/Fox-Next/Automation-Control.git"
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Fox Next — Smart Support Bot Windows Installer" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git for Windows is required: https://git-scm.com/download/win"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.10+ is required: https://www.python.org/downloads/"
}

$TmpClone = Join-Path ([System.IO.Path]::GetTempPath()) ("foxnext_ssb_" + [guid]::NewGuid().ToString("N"))
try {
    Write-Host "[1/4] Fetching clean Smart Support Bot source from $RepoUrl..." -ForegroundColor Yellow
    git clone --depth 1 $RepoUrl $TmpClone

    New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
    Copy-Item -Recurse -Force (Join-Path $TmpClone "smart-support-bot\src") (Join-Path $InstallDir "src")
    Copy-Item -Force (Join-Path $TmpClone "smart-support-bot\requirements.txt") (Join-Path $InstallDir "requirements.txt")
    Copy-Item -Force (Join-Path $TmpClone ".env.example") (Join-Path $InstallDir ".env.example")

    $EnvFile = Join-Path $InstallDir ".env"
    if (-not (Test-Path $EnvFile)) {
        Copy-Item -Force (Join-Path $InstallDir ".env.example") $EnvFile
        Write-Host "      Created $EnvFile from .env.example template." -ForegroundColor Green
    }
} finally {
    if (Test-Path $TmpClone) {
        Remove-Item -Recurse -Force $TmpClone -ErrorAction SilentlyContinue
    }
}

Write-Host "[2/4] Setting up isolated Python virtual environment (.venv)..." -ForegroundColor Yellow
$VenvDir = Join-Path $InstallDir ".venv"
$VenvPy = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPy)) {
    python -m venv $VenvDir
}

Write-Host "[3/4] Installing Smart Support Bot requirements..." -ForegroundColor Yellow
& $VenvPy -m pip install --upgrade pip wheel --quiet
& $VenvPy -m pip install -r (Join-Path $InstallDir "requirements.txt") --quiet

$RunnerBat = Join-Path $InstallDir "Start-SmartSupportBot.bat"
@"
@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONPATH=%~dp0
"%~dp0.venv\Scripts\python.exe" -m src.main
pause
"@ | Set-Content -Path $RunnerBat -Encoding UTF8

Write-Host "[4/4] Creating Desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -ComObject WScript.Shell
$DesktopLnk = Join-Path ([Environment]::GetFolderPath("Desktop")) "Smart Support Bot (Fox Next).lnk"
$Shortcut = $WshShell.CreateShortcut($DesktopLnk)
$Shortcut.TargetPath = $RunnerBat
$Shortcut.WorkingDirectory = $InstallDir
$Shortcut.Description = "Fox Next — Smart Support Bot"
$Shortcut.Save()

Write-Host "==> Smart Support Bot installed at: $InstallDir" -ForegroundColor Green
Write-Host "    Edit $InstallDir\.env (set TELEGRAM_BOT_TOKEN & CONTROL_PANEL_URL), then run Start-SmartSupportBot.bat" -ForegroundColor Cyan
