# ==============================================================================
# Fox Next — Automation Control: Windows Desktop One-Line Installer (install.ps1)
# Usage: irm https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.ps1 | iex
# ==============================================================================
param(
    [string]$InstallDir = "$env:LOCALAPPDATA\FoxNext\AutomationControl",
    [string]$ReleaseBaseUrl = "https://github.com/Fox-Next/Automation-Control/releases/latest/download",
    [switch]$NoLaunch
)

$ErrorActionPreference = "Stop"

Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Fox Next — Automation Control Windows Desktop Installer" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

$ExePath = Join-Path $InstallDir "AutomationControl.exe"
$TmpExe = Join-Path $InstallDir "AutomationControl.exe.part"
$ShaSumsUrl = "$ReleaseBaseUrl/SHA256SUMS.txt"
$ShaUrl = "$ReleaseBaseUrl/AutomationControl.exe.sha256"
$ExeUrl = "$ReleaseBaseUrl/AutomationControl.exe"

Write-Host "[1/4] Downloading AutomationControl.exe from GitHub Releases..." -ForegroundColor Yellow
if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
    & curl.exe -fL -C - --retry 3 -o $TmpExe $ExeUrl
    if ($LASTEXITCODE -ne 0) {
        throw "Failed to download AutomationControl.exe from $ExeUrl"
    }
} else {
    Invoke-WebRequest -Uri $ExeUrl -OutFile $TmpExe -UseBasicParsing
}

Write-Host "[2/4] Verifying SHA-256 integrity checksum..." -ForegroundColor Yellow
$ActualHash = (Get-FileHash -Path $TmpExe -Algorithm SHA256).Hash.ToLowerInvariant()
try {
    $ExpectedHash = ""
    try {
        $SumsRaw = (Invoke-WebRequest -Uri $ShaSumsUrl -UseBasicParsing -TimeoutSec 10).Content
        if ($SumsRaw -is [byte[]]) {
            $SumsRaw = [System.Text.Encoding]::UTF8.GetString($SumsRaw)
        }
        foreach ($line in ($SumsRaw -split "`r?`n")) {
            if ($line -match '^\s*([a-fA-F0-9]{64})\s+\*?AutomationControl\.exe\s*$') {
                $ExpectedHash = $Matches[1].ToLowerInvariant()
                break
            }
        }
    } catch {}
    if (-not $ExpectedHash) {
        $ExpectedRaw = (Invoke-WebRequest -Uri $ShaUrl -UseBasicParsing -TimeoutSec 10).Content
        if ($ExpectedRaw -is [byte[]]) {
            $ExpectedRaw = [System.Text.Encoding]::UTF8.GetString($ExpectedRaw)
        }
        $ExpectedHash = ($ExpectedRaw -split '\s+')[0].Trim().ToLowerInvariant()
    }
    if ($ExpectedHash -and ($ExpectedHash.Length -eq 64) -and ($ActualHash -ne $ExpectedHash)) {
        Remove-Item -Force $TmpExe -ErrorAction SilentlyContinue
        throw "SHA-256 checksum mismatch! Expected: $ExpectedHash, Got: $ActualHash"
    }
    Write-Host "      SHA-256 verified: $ActualHash" -ForegroundColor Green
} catch {
    if ($_.Exception.Message -match "SHA-256 checksum mismatch") {
        throw $_
    }
    Write-Host "      Computed SHA-256: $ActualHash" -ForegroundColor Gray
}

Move-Item -Force $TmpExe $ExePath

Write-Host "[3/4] Creating Desktop & Start Menu shortcuts..." -ForegroundColor Yellow
$WshShell = New-Object -ComObject WScript.Shell
$DesktopLnk = Join-Path ([Environment]::GetFolderPath("Desktop")) "Automation Control.lnk"
$StartMenuDir = Join-Path ([Environment]::GetFolderPath("Programs")) "Fox Next"
New-Item -ItemType Directory -Force -Path $StartMenuDir | Out-Null
$StartMenuLnk = Join-Path $StartMenuDir "Automation Control.lnk"

foreach ($LnkPath in @($DesktopLnk, $StartMenuLnk)) {
    $Shortcut = $WshShell.CreateShortcut($LnkPath)
    $Shortcut.TargetPath = $ExePath
    $Shortcut.WorkingDirectory = $InstallDir
    $Shortcut.Description = "Automation Control — Fox Next 8-Agent Desktop App"
    $Shortcut.IconLocation = "$ExePath,0"
    $Shortcut.Save()
}

Write-Host "[4/4] Installation complete at: $ExePath" -ForegroundColor Green
if (-not $NoLaunch) {
    Write-Host "==> Launching Automation Control..." -ForegroundColor Cyan
    Start-Process -FilePath $ExePath -WorkingDirectory $InstallDir
}
