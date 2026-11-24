#!/usr/bin/env bash
# ==============================================================================
# Fox Next — Automation Control & Smart Support Bot Official Linux Installer
# - Downloads compiled Linux release package from GitHub Releases of
#   Fox-Next/Automation-Control with SHA-256 verification.
# - Configures and starts `foxnext-control-expert.service` (/opt/foxnext-automation).
# - Automatically installs and configures `smart-support-bot.service` (/opt/smart-support)
#   from the same repository.
# - Interactive CLI wizard for Port, Email, and optional Domain/Let's Encrypt SSL
#   (No mandatory license key — 48-hour free trial starts automatically!).
# Usage: curl -fsSL https://raw.githubusercontent.com/Fox-Next/Automation-Control/main/install.sh | sudo bash
# ==============================================================================
set -euo pipefail

PANEL_DIR="${FOXNEXT_PANEL_DIR:-/opt/foxnext-automation}"
BOT_DIR="${FOXNEXT_BOT_DIR:-/opt/smart-support}"
BACKUP_DIR="${FOXNEXT_BACKUP_DIR:-/opt/foxnext-backups}"
PANEL_SERVICE="foxnext-control-expert.service"
BOT_SERVICE="smart-support-bot.service"
DEFAULT_PORT="${PORT:-8787}"
PUBLIC_REPO_URL="https://github.com/Fox-Next/Automation-Control.git"
RELEASE_BASE_URL="https://github.com/Fox-Next/Automation-Control/releases/latest/download"
RELEASE_ARCHIVE="automation-control-linux.tar.gz"

echo "=========================================================================="
echo "   Fox Next — Automation Control & Smart Support Bot Linux Installer"
echo "=========================================================================="

if [ "${EUID:-$(id -u)}" -ne 0 ]; then
  echo "[ERROR] Please run this installer as root (or with sudo)."
  exit 1
fi

# 1. Interactive Wizard (non-blocking in non-interactive shells, 48h Trial auto-enabled)
SELECTED_PORT="$DEFAULT_PORT"
SELECTED_USER_EMAIL="${FOXNEXT_USER_EMAIL:-}"
SELECTED_LICENSE_KEY="${FOXNEXT_LICENSE_KEY:-}"
SELECTED_ADMIN_USER="${ADMIN_USER:-admin}"
SELECTED_ADMIN_PASS="${ADMIN_PASS:-admin12345}"
DOMAIN_NAME="${FOXNEXT_DOMAIN:-}"
SETUP_SSL="n"

if [ -t 0 ]; then
  read -r -p "Control Panel HTTP port [${DEFAULT_PORT}]: " in_port || true
  SELECTED_PORT="${in_port:-$DEFAULT_PORT}"
  read -r -p "Account email (activates 48-hour Free Trial & auto-syncs license): " in_email || true
  SELECTED_USER_EMAIL="$(echo "${in_email:-}" | tr -d '[:space:]')"
  read -r -p "License key (optional — press Enter to start 48-hour Free Trial): " in_lic || true
  SELECTED_LICENSE_KEY="$(echo "${in_lic:-}" | tr -d '[:space:]')"
  read -r -p "Admin username [admin]: " in_user || true
  SELECTED_ADMIN_USER="${in_user:-admin}"
  read -r -s -p "Admin password [admin12345]: " in_pass || true
  echo ""
  SELECTED_ADMIN_PASS="${in_pass:-admin12345}"
  read -r -p "Optional domain for Nginx + Let's Encrypt SSL (press Enter to skip): " in_dom || true
  DOMAIN_NAME="$(echo "${in_dom:-}" | tr -d '[:space:]')"
  if [ -n "$DOMAIN_NAME" ]; then
    SETUP_SSL="y"
  fi
fi

if [ -z "$SELECTED_LICENSE_KEY" ]; then
  echo "[INFO] No license key entered — 48-hour Free Trial will start automatically."
fi

# 2. Install OS Packages
if command -v apt-get >/dev/null 2>&1; then
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y -q
  apt-get install -y -q curl git python3 python3-venv python3-pip ffmpeg nginx certbot python3-certbot-nginx sqlite3 tar ca-certificates
elif command -v dnf >/dev/null 2>&1; then
  dnf install -y git python3 python3-pip ffmpeg nginx curl tar
fi

mkdir -p "$PANEL_DIR" "$BOT_DIR" "$BACKUP_DIR" "$PANEL_DIR/data/control" "$PANEL_DIR/logs"

TMP_WORK="$(mktemp -d)"
trap 'rm -rf "${TMP_WORK}"' EXIT

# 3. Download Compiled Linux Release from GitHub Releases with SHA-256 verification
ARCHIVE_PATH="${TMP_WORK}/${RELEASE_ARCHIVE}"
SHA_PATH="${TMP_WORK}/SHA256SUMS.txt"

if curl -fsSL "${RELEASE_BASE_URL}/${RELEASE_ARCHIVE}" -o "$ARCHIVE_PATH" 2>/dev/null; then
  echo "[INFO] Downloaded ${RELEASE_ARCHIVE} from GitHub Releases."
  EXPECTED_SHA=""
  if curl -fsSL "${RELEASE_BASE_URL}/SHA256SUMS.txt" -o "$SHA_PATH" 2>/dev/null; then
    EXPECTED_SHA="$(awk -v tgt="${RELEASE_ARCHIVE}" '$2==tgt || $2=="*"tgt {print $1}' "$SHA_PATH" | head -n1 | tr '[:upper:]' '[:lower:]')"
  elif curl -fsSL "${RELEASE_BASE_URL}/${RELEASE_ARCHIVE}.sha256" -o "$SHA_PATH" 2>/dev/null; then
    EXPECTED_SHA="$(awk '{print $1}' "$SHA_PATH" | head -n1 | tr '[:upper:]' '[:lower:]')"
  fi
  if [ -n "$EXPECTED_SHA" ]; then
    ACTUAL_SHA="$(sha256sum "$ARCHIVE_PATH" | awk '{print $1}' | tr '[:upper:]' '[:lower:]')"
    if [ "$EXPECTED_SHA" != "$ACTUAL_SHA" ]; then
      echo "[ERROR] SHA-256 verification failed! Expected ${EXPECTED_SHA}, got ${ACTUAL_SHA}"
      exit 1
    fi
    echo "[OK] SHA-256 checksum verified: ${ACTUAL_SHA}"
  fi
  tar --no-same-owner -xzf "$ARCHIVE_PATH" -C "$PANEL_DIR"
fi

# 4. Clone Public Repo for Smart Support Bot
git clone --depth 1 "$PUBLIC_REPO_URL" "${TMP_WORK}/pub_repo"
cp -r "${TMP_WORK}/pub_repo/smart-support-bot/src" "${BOT_DIR}/src"
cp "${TMP_WORK}/pub_repo/smart-support-bot/requirements.txt" "${BOT_DIR}/requirements.txt"
if [ ! -f "${BOT_DIR}/.env" ]; then
  cp "${TMP_WORK}/pub_repo/.env.example" "${BOT_DIR}/.env"
  sed -i "s|^CONTROL_PANEL_URL=.*|CONTROL_PANEL_URL=http://127.0.0.1:${SELECTED_PORT}|" "${BOT_DIR}/.env" || true
fi

if [ ! -d "${BOT_DIR}/.venv" ]; then
  python3 -m venv "${BOT_DIR}/.venv"
fi
"${BOT_DIR}/.venv/bin/pip" install --upgrade pip wheel -q
"${BOT_DIR}/.venv/bin/pip" install -r "${BOT_DIR}/requirements.txt" -q

# 5. Setup Panel Virtualenv & Environment if panel requirements exist
PANEL_ENV="${PANEL_DIR}/apps/control_expert/.env"
mkdir -p "${PANEL_DIR}/apps/control_expert"
cat > "$PANEL_ENV" <<EOF
AUTOMATION_EDITION=self_hosted
AUTOMATION_ROOT=${PANEL_DIR}
PORT=${SELECTED_PORT}
FOXNEXT_USER_EMAIL=${SELECTED_USER_EMAIL}
FOXNEXT_LICENSE_KEY=${SELECTED_LICENSE_KEY}
AUTOMATION_SUPERUSER_USERNAME=${SELECTED_ADMIN_USER}
AUTOMATION_SUPERUSER_PASSWORD=${SELECTED_ADMIN_PASS}
EOF
chmod 600 "$PANEL_ENV"

if [ -f "${PANEL_DIR}/requirements.txt" ]; then
  if [ ! -d "${PANEL_DIR}/apps/control_expert/.venv" ]; then
    python3 -m venv "${PANEL_DIR}/apps/control_expert/.venv"
  fi
  "${PANEL_DIR}/apps/control_expert/.venv/bin/pip" install --upgrade pip wheel -q
  "${PANEL_DIR}/apps/control_expert/.venv/bin/pip" install -r "${PANEL_DIR}/requirements.txt" -q
fi

# 6. Register systemd services: foxnext-control-expert.service & smart-support-bot.service
if command -v systemctl >/dev/null 2>&1; then
  cat > "/etc/systemd/system/${PANEL_SERVICE}" <<EOF
[Unit]
Description=Fox Next Automation Control Expert
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${PANEL_DIR}/apps/control_expert
Environment=AUTOMATION_ROOT=${PANEL_DIR}
Environment=PYTHONPATH=${PANEL_DIR}
EnvironmentFile=-${PANEL_DIR}/apps/control_expert/.env
ExecStart=${PANEL_DIR}/apps/control_expert/.venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port ${SELECTED_PORT}
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

  cat > "/etc/systemd/system/${BOT_SERVICE}" <<EOF
[Unit]
Description=Fox Next Smart Support Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=${BOT_DIR}
Environment=PYTHONPATH=${BOT_DIR}
EnvironmentFile=-${BOT_DIR}/.env
ExecStart=${BOT_DIR}/.venv/bin/python -m src.main
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

  systemctl daemon-reload
  systemctl enable "${BOT_SERVICE}" >/dev/null 2>&1 || true
  if [ -f "${PANEL_DIR}/apps/control_expert/main.py" ]; then
    systemctl enable "${PANEL_SERVICE}" >/dev/null 2>&1 || true
    systemctl restart "${PANEL_SERVICE}" || true
  fi
fi

# 7. Optional Nginx + Let's Encrypt SSL
if [ -n "$DOMAIN_NAME" ] && command -v nginx >/dev/null 2>&1; then
  cat > "/etc/nginx/sites-available/${DOMAIN_NAME}" <<EOF
server {
    listen 80;
    server_name ${DOMAIN_NAME};
    client_max_body_size 50M;
    location / {
        proxy_pass http://127.0.0.1:${SELECTED_PORT};
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
  ln -sf "/etc/nginx/sites-available/${DOMAIN_NAME}" "/etc/nginx/sites-enabled/${DOMAIN_NAME}"
  nginx -t && systemctl reload nginx
  if [ "$SETUP_SSL" = "y" ] && command -v certbot >/dev/null 2>&1; then
    certbot --nginx -d "$DOMAIN_NAME" --non-interactive --agree-tos --register-unsafely-without-email --redirect || true
  fi
fi

echo "=========================================================================="
echo "[SUCCESS] Fox Next Automation Control & Smart Support Bot setup complete!"
echo "  - Panel Dir:   ${PANEL_DIR} (${PANEL_SERVICE})"
echo "  - Bot Dir:     ${BOT_DIR} (${BOT_SERVICE})"
echo "  - Trial Mode:  48-Hour Free Trial enabled automatically"
echo "=========================================================================="
