@echo off
chcp 65001 >nul
title Fox Next — Automation Control ComfyUI Setup
echo ==================================================================
echo   Fox Next — Automation Control: One-Click ComfyUI Setup
echo ==================================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup-comfyui.ps1" %*
pause
