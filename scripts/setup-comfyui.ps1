# ==============================================================================
# Fox Next — Automation Control: Windows Local ComfyUI One-Line Setup
# Installs/starts a local ComfyUI node for Local-First image & short video generation
# alongside the Automation Control Desktop Application.
# Usage: irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
# ==============================================================================
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\FoxNext\ComfyUI",
    [int]$Port = 8188,
    [switch]$StartAfterSetup
)

$ErrorActionPreference = "Stop"

Write-Host "==> Fox Next Automation Control: Local ComfyUI Setup" -ForegroundColor Cyan
Write-Host "    Target directory: $InstallDir" -ForegroundColor Gray

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "Git is required. Install Git for Windows first: https://git-scm.com/download/win"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python 3.10+ is required. Install Python from https://www.python.org/downloads/"
}

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

$RepoPath = Join-Path $InstallDir "ComfyUI"
if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    Write-Host "==> Cloning ComfyUI..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git $RepoPath
} else {
    Write-Host "==> Updating existing ComfyUI checkout..." -ForegroundColor Yellow
    git -C $RepoPath pull --ff-only
}

$VenvDir = Join-Path $RepoPath ".venv"
$VenvPy = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPy)) {
    Write-Host "==> Creating virtual environment..." -ForegroundColor Yellow
    python -m venv $VenvDir
}

Write-Host "==> Upgrading pip & installing requirements..." -ForegroundColor Yellow
& $VenvPy -m pip install --upgrade pip
& $VenvPy -m pip install -r (Join-Path $RepoPath "requirements.txt")

Write-Host "==> ComfyUI ready at $RepoPath (Endpoint: http://127.0.0.1:$Port)" -ForegroundColor Green

if ($StartAfterSetup) {
    Write-Host "==> Launching ComfyUI on port $Port..." -ForegroundColor Cyan
    Start-Process -FilePath $VenvPy -ArgumentList "main.py --listen 127.0.0.1 --port $Port" -WorkingDirectory $RepoPath
}
