# ==============================================================================
# Fox Next — Automation Control: Windows Local ComfyUI One-Line Setup
# Enforces 3-Tier 6 GB VRAM Hardware Gate, Resumable curl.exe -C - download,
# FFmpeg check, 127.0.0.1:8188 startup, and 100% automatic panel pairing.
# Usage: irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/scripts/setup-comfyui.ps1 | iex
# ==============================================================================
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\FoxNext\ComfyUI",
    [int]$Port = 8188,
    [string]$PanelUrl = "https://panel.foxnext.online",
    [string]$PairToken = "",
    [int]$OverrideVramMb = -1,
    [switch]$ProbeOnly,
    [switch]$NoStart
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Fox Next — Automation Control: ComfyUI Hardware Gate & Setup" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# 1. Hardware Gate: 6 GB VRAM + Free Disk Space
$GpuName = ""
$VramMb = 0
if ($OverrideVramMb -ge 0) {
    $GpuName = "NVIDIA GeForce RTX (Override)"
    $VramMb = $OverrideVramMb
} elseif (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
    try {
        $SmiOut = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null
        if ($LASTEXITCODE -eq 0 -and $SmiOut) {
            $First = ($SmiOut -split "`r?`n")[0]
            $Parts = $First -split ","
            if ($Parts.Count -ge 2) {
                $GpuName = $Parts[0].Trim()
                $VramMb = [int][double]($Parts[1].Trim())
            }
        }
    } catch {}
}

$DriveRoot = [System.IO.Path]::GetPathRoot($InstallDir)
if (-not $DriveRoot) { $DriveRoot = "C:\" }
$DriveInfo = New-Object System.IO.DriveInfo($DriveRoot)
$FreeDiskGb = [math]::Round($DriveInfo.AvailableFreeSpace / 1GB, 2)

$IsDedicatedNvidia = ($GpuName -match "(?i)(nvidia|geforce|rtx|gtx|quadro|tesla|a100|l4|titan)") -and ($GpuName -notmatch "(?i)(intel|uhd|iris)")

if (-not $IsDedicatedNvidia -or $VramMb -lt 6000) {
    Write-Host "[HARDWARE GATE LOCKED] GPU: '$GpuName' ($VramMb MB VRAM)." -ForegroundColor Red
    Write-Host "Local ComfyUI rendering requires a dedicated NVIDIA GPU with at least 6 GB VRAM." -ForegroundColor Yellow
    Write-Host "Quality Red-Line: Low-quality Pillow fallback is disabled. Please use Fox Next Cloud Studio ($PanelUrl)." -ForegroundColor Cyan
    if ($ProbeOnly) { exit 2 }
    throw "Hardware Gate blocked: NVIDIA GPU >= 6 GB VRAM required for local ComfyUI."
}

$Tier = if ($VramMb -ge 10000) { "flux_and_sdxl" } else { "sdxl_light" }
$RequiredDiskGb = if ($Tier -eq "flux_and_sdxl") { 30 } else { 20 }
$AllowedModels = if ($Tier -eq "flux_and_sdxl") { "FLUX + SDXL" } else { "SDXL Light / Turbo" }

if ($FreeDiskGb -lt $RequiredDiskGb) {
    Write-Host "[HARDWARE GATE LOCKED] Free disk: $FreeDiskGb GB (Required: $RequiredDiskGb GB for $AllowedModels)." -ForegroundColor Red
    if ($ProbeOnly) { exit 3 }
    throw "Insufficient free disk space ($FreeDiskGb GB < $RequiredDiskGb GB). Please use Cloud Studio."
}

Write-Host "[HARDWARE GATE PASSED] GPU: $GpuName ($VramMb MB VRAM) | Free Disk: $FreeDiskGb GB | Tier: $Tier ($AllowedModels)" -ForegroundColor Green
if ($ProbeOnly) { exit 0 }

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

# 2. Ensure FFmpeg is available (resumable curl.exe -C -)
$FfmpegDir = Join-Path $InstallDir "ffmpeg"
if (-not (Get-Command ffmpeg -ErrorAction SilentlyContinue)) {
    New-Item -ItemType Directory -Force -Path $FfmpegDir | Out-Null
    $FfmpegZip = Join-Path $FfmpegDir "ffmpeg-release-essentials.zip"
    $FfmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    Write-Host "[2/4] Downloading FFmpeg with resume support (curl.exe -C -)..." -ForegroundColor Yellow
    & curl.exe -fL -C - --retry 3 -o $FfmpegZip $FfmpegUrl
}

# 3. Clone or update ComfyUI
$RepoPath = Join-Path $InstallDir "ComfyUI"
if (-not (Test-Path (Join-Path $RepoPath ".git"))) {
    Write-Host "[3/4] Cloning ComfyUI into $RepoPath..." -ForegroundColor Yellow
    git clone --depth 1 https://github.com/comfyanonymous/ComfyUI.git $RepoPath
} else {
    Write-Host "[3/4] Updating existing ComfyUI checkout..." -ForegroundColor Yellow
    git -C $RepoPath pull --ff-only
}

$VenvDir = Join-Path $RepoPath ".venv"
$VenvPy = Join-Path $VenvDir "Scripts\python.exe"
if (-not (Test-Path $VenvPy)) {
    python -m venv $VenvDir
}
& $VenvPy -m pip install --upgrade pip --quiet
& $VenvPy -m pip install -r (Join-Path $RepoPath "requirements.txt") --quiet

# 4. Auto-pair with Fox Next Automation Control panel & desktop shell
$WorkerCfgDir = Join-Path $env:USERPROFILE ".foxnext_render_worker"
New-Item -ItemType Directory -Force -Path $WorkerCfgDir | Out-Null
$WorkerCfgPath = Join-Path $WorkerCfgDir "config.json"
$ComfyEndpoint = "http://127.0.0.1:$Port"

$CfgObj = @{
    panel_url = $PanelUrl
    pair_token = $PairToken
    comfyui_url = $ComfyEndpoint
    worker_name = $env:COMPUTERNAME
    hardware_tier = $Tier
    allowed_models = $AllowedModels
    vram_total_mb = $VramMb
    poll_interval_sec = 3.0
}
($CfgObj | ConvertTo-Json -Depth 4) | Set-Content -Path $WorkerCfgPath -Encoding UTF8
Write-Host "[4/4] Auto-paired ComfyUI ($ComfyEndpoint) in $WorkerCfgPath" -ForegroundColor Green

if (-not $NoStart) {
    Write-Host "==> Starting ComfyUI on 127.0.0.1:$Port..." -ForegroundColor Cyan
    Start-Process -FilePath $VenvPy -ArgumentList "main.py --listen 127.0.0.1 --port $Port" -WorkingDirectory $RepoPath
}
