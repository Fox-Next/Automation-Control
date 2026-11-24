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

# 1. Hardware Gate: Multi-GPU (NVIDIA CUDA / AMD ROCm or DirectML / Intel) >= 6 GB VRAM + Disk
$DetectedGpus = @()
$GpuName = ""
$GpuVendor = "other"
$VramMb = 0
$ComfyBackend = "cloud_or_cpu"
$FfmpegEncoder = "libx264"

if ($OverrideVramMb -ge 0) {
    $GpuName = "NVIDIA GeForce RTX (Override)"
    $GpuVendor = "nvidia"
    $VramMb = $OverrideVramMb
    $DetectedGpus = @(@{ name = $GpuName; vendor = $GpuVendor; vram_mb = $VramMb })
} else {
    $RegVramMap = @{}
    $ClassKey = "HKLM:\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
    Get-ChildItem -Path $ClassKey -ErrorAction SilentlyContinue | ForEach-Object {
        $Props = Get-ItemProperty -Path $_.PSPath -ErrorAction SilentlyContinue
        if ($Props -and $Props.DriverDesc -and $Props.'HardwareInformation.qwMemorySize') {
            try {
                $Qw = $Props.'HardwareInformation.qwMemorySize'
                $Bytes = if ($Qw -is [byte[]]) { [BitConverter]::ToUInt64($Qw, 0) } else { [uint64]$Qw }
                $RegMb = [int][math]::Round($Bytes / 1MB)
                $K = ([string]$Props.DriverDesc).Trim().ToLower()
                if (-not $RegVramMap.ContainsKey($K) -or $RegMb -gt $RegVramMap[$K]) {
                    $RegVramMap[$K] = $RegMb
                }
            } catch {}
        }
    }
    $SmiMap = @{}
    if (Get-Command nvidia-smi -ErrorAction SilentlyContinue) {
        try {
            $SmiOut = & nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits 2>$null
            if ($LASTEXITCODE -eq 0 -and $SmiOut) {
                foreach ($Line in ($SmiOut -split "`r?`n")) {
                    $Parts = $Line -split ","
                    if ($Parts.Count -ge 2) {
                        $SmiMap[$Parts[0].Trim().ToLower()] = [int][double]($Parts[1].Trim())
                    }
                }
            }
        } catch {}
    }
    Get-CimInstance Win32_VideoController -ErrorAction SilentlyContinue | ForEach-Object {
        $Name = ([string]$_.Name).Trim()
        if (-not $Name -or ($Name -match "(?i)(microsoft basic|remote desktop|parsec|virtual display|citrix|vmware)")) { return }
        $WmiMb = if ($_.AdapterRAM) { [int][math]::Round(([uint64]$_.AdapterRAM) / 1MB) } else { 0 }
        $RegMb = if ($RegVramMap.ContainsKey($Name.ToLower())) { $RegVramMap[$Name.ToLower()] } else { 0 }
        $BestMb = [math]::Max($WmiMb, $RegMb)
        foreach ($Sk in $SmiMap.Keys) {
            if ($Name.ToLower().Contains($Sk) -or $Sk.Contains($Name.ToLower())) {
                $BestMb = [math]::Max($BestMb, $SmiMap[$Sk])
            }
        }
        $Vendor = if ($Name -match "(?i)(nvidia|geforce|rtx|gtx|quadro|tesla|titan)") { "nvidia" }
                  elseif ($Name -match "(?i)(amd|radeon|rx |firepro|vega|rdna)") { "amd" }
                  elseif ($Name -match "(?i)intel") { "intel" } else { "other" }
        $DetectedGpus += @{ name = $Name; vendor = $Vendor; vram_mb = $BestMb }
    }
    if ($DetectedGpus.Count -gt 0) {
        $Best = $DetectedGpus | Sort-Object { $_.vram_mb } -Descending | Select-Object -First 1
        $GpuName = $Best.name
        $GpuVendor = $Best.vendor
        $VramMb = [int]$Best.vram_mb
    }
}

$DriveRoot = [System.IO.Path]::GetPathRoot($InstallDir)
if (-not $DriveRoot) { $DriveRoot = "C:\" }
$DriveInfo = New-Object System.IO.DriveInfo($DriveRoot)
$FreeDiskGb = [math]::Round($DriveInfo.AvailableFreeSpace / 1GB, 2)

$HasQualifyingGpu = ($VramMb -ge 6000) -and ($GpuVendor -in @("nvidia", "amd", "intel"))

if (-not $HasQualifyingGpu) {
    Write-Host "[HARDWARE GATE LOCKED] Best GPU: '$GpuName' ($GpuVendor, $VramMb MB VRAM)." -ForegroundColor Red
    Write-Host "Local ComfyUI rendering requires a GPU (NVIDIA / AMD / Intel) with at least 6 GB VRAM." -ForegroundColor Yellow
    Write-Host "Please use Fox Next Cloud Studio ($PanelUrl)." -ForegroundColor Cyan
    if ($ProbeOnly) { exit 2 }
    throw "Hardware Gate blocked: >= 6 GB VRAM GPU required for local ComfyUI."
}

if ($GpuVendor -eq "nvidia") {
    $ComfyBackend = "cuda"
    $FfmpegEncoder = "h264_nvenc"
} elseif ($GpuVendor -eq "amd") {
    if ((Get-Command rocm-smi -ErrorAction SilentlyContinue) -or $env:HIP_PATH) {
        $ComfyBackend = "rocm"
    } else {
        $ComfyBackend = "directml"
    }
    $FfmpegEncoder = "h264_amf"
} else {
    $ComfyBackend = "directml"
    $FfmpegEncoder = "h264_qsv"
}

$Tier = if ($VramMb -ge 10000) { "flux_and_sdxl" } else { "sdxl_light" }
$RequiredDiskGb = if ($Tier -eq "flux_and_sdxl") { 30 } else { 20 }
$AllowedModels = if ($Tier -eq "flux_and_sdxl") { "FLUX + SDXL" } else { "SDXL Light / Turbo" }

if ($FreeDiskGb -lt $RequiredDiskGb) {
    Write-Host "[HARDWARE GATE LOCKED] Free disk: $FreeDiskGb GB (Required: $RequiredDiskGb GB for $AllowedModels)." -ForegroundColor Red
    if ($ProbeOnly) { exit 3 }
    throw "Insufficient free disk space ($FreeDiskGb GB < $RequiredDiskGb GB). Please use Cloud Studio."
}

Write-Host "[HARDWARE GATE PASSED] GPU: $GpuName ($GpuVendor, $VramMb MB VRAM) | Backend: $ComfyBackend | FFmpeg: $FfmpegEncoder | Free Disk: $FreeDiskGb GB" -ForegroundColor Green
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

# 3. Clone or update ComfyUI & install backend packages (CUDA / ROCm / DirectML)
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
if ($ComfyBackend -eq "directml") {
    & $VenvPy -m pip install torch-directml --quiet
}

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
    gpu_name = $GpuName
    gpu_vendor = $GpuVendor
    comfy_backend = $ComfyBackend
    ffmpeg_encoder = $FfmpegEncoder
    hardware_tier = $Tier
    allowed_models = $AllowedModels
    vram_total_mb = $VramMb
    all_gpus = $DetectedGpus
    poll_interval_sec = 3.0
}
($CfgObj | ConvertTo-Json -Depth 4) | Set-Content -Path $WorkerCfgPath -Encoding UTF8
Write-Host "[4/4] Auto-paired ComfyUI ($ComfyEndpoint) in $WorkerCfgPath" -ForegroundColor Green

if (-not $NoStart) {
    Write-Host "==> Starting ComfyUI on 127.0.0.1:$Port..." -ForegroundColor Cyan
    Start-Process -FilePath $VenvPy -ArgumentList "main.py --listen 127.0.0.1 --port $Port" -WorkingDirectory $RepoPath
}
