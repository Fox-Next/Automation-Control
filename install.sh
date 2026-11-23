#!/usr/bin/env bash
# ==============================================================================
# Fox Next — Automation Control: Smart Support Bot Linux One-Line Installer
# Installs dependencies, Python virtualenv, .env template, and systemd unit.
# Usage: curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | bash
# ==============================================================================
set -euo pipefail

APP_DIR="${AUTOMATION_INSTALL_DIR:-/opt/smart-support}"
REPO_URL="${AUTOMATION_REPO_URL:-https://github.com/Fox-Next/Automation-Control.git}"
SERVICE_NAME="foxnext-smart-support"

echo "==> Installing Fox Next Smart Support Bot into ${APP_DIR}..."

if command -v apt-get >/dev/null 2>&1; then
  sudo apt-get update -y
  sudo apt-get install -y git python3 python3-venv python3-pip ffmpeg curl
elif command -v dnf >/dev/null 2>&1; then
  sudo dnf install -y git python3 python3-pip ffmpeg curl
fi

TMP_CLONE="$(mktemp -d)"
trap 'rm -rf "${TMP_CLONE}"' EXIT

git clone --depth 1 "${REPO_URL}" "${TMP_CLONE}/repo"

sudo mkdir -p "${APP_DIR}"
sudo cp -r "${TMP_CLONE}/repo/smart-support-bot/src" "${APP_DIR}/src"
sudo cp "${TMP_CLONE}/repo/smart-support-bot/requirements.txt" "${APP_DIR}/requirements.txt"

if [ ! -f "${APP_DIR}/.env" ]; then
  sudo cp "${TMP_CLONE}/repo/.env.example" "${APP_DIR}/.env"
  echo "==> Created ${APP_DIR}/.env from template. Update TELEGRAM_BOT_TOKEN and CONTROL_PANEL_URL before starting."
fi

if [ ! -d "${APP_DIR}/.venv" ]; then
  sudo python3 -m venv "${APP_DIR}/.venv"
fi

sudo "${APP_DIR}/.venv/bin/pip" install --upgrade pip wheel
sudo "${APP_DIR}/.venv/bin/pip" install -r "${APP_DIR}/requirements.txt"

if command -v systemctl >/dev/null 2>&1; then
  sudo tee "/etc/systemd/system/${SERVICE_NAME}.service" >/dev/null <<EOF
[Unit]
Description=Fox Next Automation Control - Smart Support Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${APP_DIR}
EnvironmentFile=${APP_DIR}/.env
Environment=PYTHONPATH=${APP_DIR}
ExecStart=${APP_DIR}/.venv/bin/python -m src.main
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
  sudo systemctl daemon-reload
  sudo systemctl enable "${SERVICE_NAME}"
  echo "==> Systemd service '${SERVICE_NAME}' installed."
  echo "==> Configure ${APP_DIR}/.env and run: sudo systemctl restart ${SERVICE_NAME}"
else
  echo "==> Setup complete. Activate ${APP_DIR}/.venv and run: python -m src.main"
fi
