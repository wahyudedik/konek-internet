#!/bin/bash
# ============================================
# Konektivitas.com — Initial Deployment Script
# Usage: bash deploy.sh
# Server: Ubuntu 22.04 + AAPanel + Nginx
# Path: /www/wwwroot/konektivitas.com
# ============================================

set -e

# ============ KONFIGURASI ============
APP_DIR="/www/wwwroot/konektivitas.com"
GIT_REPO="https://github.com/USERNAME/konek-internet.git"  # Ganti dengan URL repo
BRANCH="main"
PORT=8002
VENV_DIR="$APP_DIR/.venv"
LOG_DIR="/www/wwwlogs"
SUPERVISOR_CONF="/etc/supervisor/conf.d/konektivitas.conf"

echo "============================================"
echo "  Konektivitas.com — Initial Deployment"
echo "============================================"
echo ""

# ============ STEP 1: CEK ROOT ============
if [ "$EUID" -ne 0 ]; then
    echo "❌ Script ini harus dijalankan sebagai root."
    echo "   Gunakan: sudo bash deploy.sh"
    exit 1
fi

# ============ STEP 2: INSTALL DEPENDENCIES SISTEM ============
echo "📦 [1/10] Installing system dependencies..."

# Update package list
apt-get update -qq

# Install Python 3.10+, pip, venv, build tools
apt-get install -y -qq python3 python3-pip python3-venv python3-dev \
    build-essential libffi-dev libssl-dev git curl socat > /dev/null 2>&1

echo "   ✅ System dependencies installed."

# ============ STEP 3: KONFIGURASI DIRECTORI ============
echo "📁 [2/10] Setting up directories..."

# Buat direktori web root
mkdir -p "$APP_DIR"
mkdir -p "$LOG_DIR"

echo "   ✅ Directories ready."

# ============ STEP 4: KLONE REPOSITORY ============
echo "📥 [3/10] Cloning repository..."

cd /www/wwwroot

if [ -d "$APP_DIR/.git" ]; then
    echo "   ⚠️ Repository sudah ada, pull latest..."
    cd "$APP_DIR"
    git pull origin "$BRANCH"
else
    echo "   Cloning ke $APP_DIR..."
    git clone -b "$BRANCH" "$GIT_REPO" "$APP_DIR"
    cd "$APP_DIR"
fi

echo "   ✅ Repository ready."

# ============ STEP 5: SETUP VIRTUAL ENVIRONMENT ============
echo "🐍 [4/10] Setting up Python virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip -q

echo "   ✅ Virtual environment ready."

# ============ STEP 6: INSTALL DEPENDENCIES ============
echo "📦 [5/10] Installing Python dependencies..."

pip install -q -r requirements.txt

echo "   ✅ Dependencies installed."

# ============ STEP 7: KONFIGURASI .ENV ============
echo "⚙️ [6/10] Setting up environment variables..."

if [ ! -f "$APP_DIR/.env" ]; then
    # Generate random JWT secret
    JWT_SECRET=$(python3 -c "import secrets; print(secrets.token_urlsafe(64))")

    cat > "$APP_DIR/.env" << EOF
# ============================================
# Konektivitas.com — Production Environment
# ============================================

# App
APP_NAME=Konektivitas.com
APP_VERSION=1.0.0
DEBUG=false

# Server
HOST=0.0.0.0
PORT=$PORT

# Redis
REDIS_URL=redis://localhost:6379/0

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60

# CORS
ALLOWED_ORIGINS=https://konektivitas.com,https://www.konektivitas.com

# API
API_V1_PREFIX=/api/v1

# Database (SQLite untuk Fase 1-2, PostgreSQL untuk Fase 3+)
DATABASE_URL=sqlite+aiosqlite:///./konektivitas.db

# JWT Authentication
JWT_SECRET_KEY=$JWT_SECRET
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# SMTP Email (konfigurasi sesuai provider)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_FROM=noreply@konektivitas.com

# Telegram Bot (opsional)
TELEGRAM_BOT_TOKEN=
TELEGRAM_DEFAULT_CHAT_ID=

# Discord Webhook (opsional)
DISCORD_WEBHOOK_URL=
EOF

    chmod 600 "$APP_DIR/.env"
    echo "   ✅ .env created (JWT secret auto-generated)."
    echo "   ⚠️  IMPORTANT: Edit .env untuk mengisi SMTP credentials!"
else
    echo "   ✅ .env sudah ada, skip."
fi

# ============ STEP 8: SETUP LOGS ============
echo "📋 [7/10] Setting up log files..."

touch "$LOG_DIR/konektivitas.com.access.log"
touch "$LOG_DIR/konektivitas.com.error.log"

echo "   ✅ Log files ready."

# ============ STEP 9: KONFIGURASI SUPERVISOR ============
echo "🔧 [8/10] Setting up Supervisor..."

if [ -f "$SUPERVISOR_CONF" ]; then
    echo "   ⚠️ Supervisor config sudah ada, skip."
else
    cat > "$SUPERVISOR_CONF" << EOF
[program:konektivitas]
command=$VENV_DIR/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:$PORT --timeout 120
directory=$APP_DIR
user=root
autostart=true
autorestart=true
startsecs=10
stopwaitsecs=30
redirect_stderr=true
stdout_logfile=$LOG_DIR/konektivitas.com.error.log
stderr_logfile=$LOG_DIR/konektivitas.com.error.log
environment=PATH="$VENV_DIR/bin"
stopsignal=TERM
EOF

    supervisorctl reread
    supervisorctl update
    supervisorctl start konektivitas
    echo "   ✅ Supervisor configured and started."
fi

# ============ STEP 10: HEALTH CHECK ============
echo "🏥 [9/10] Running health check..."

sleep 3

HEALTH=$(curl -s http://localhost:$PORT/health 2>/dev/null || echo "FAILED")
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ Health check passed!"
    echo "   $HEALTH" | python3 -m json.tool 2>/dev/null || echo "   $HEALTH"
else
    echo "   ❌ Health check failed!"
    echo "   Response: $HEALTH"
    echo "   Cek log: tail -50 $LOG_DIR/konektivitas.com.error.log"
fi

# ============ STEP 11: SET PERMISSIONS ============
echo "🔐 [10/10] Setting permissions..."

chmod -R 755 "$APP_DIR"
chmod 600 "$APP_DIR/.env"
chown -R root:root "$APP_DIR"

echo "   ✅ Permissions set."

# ============ SELESAI ============
echo ""
echo "============================================"
echo "  ✅ Deployment Selesai!"
echo "============================================"
echo ""
echo "  Website : https://konektivitas.com"
echo "  API     : https://konektivitas.com/api/v1/"
echo "  Docs    : https://konektivitas.com/docs"
echo "  Health  : https://konektivitas.com/health"
echo ""
echo "  Logs    : $LOG_DIR/konektivitas.com.error.log"
echo "  App     : $APP_DIR"
echo ""
echo "  ⚠️  Selanjutnya:"
echo "  1. Konfigurasi Nginx reverse proxy di AAPanel"
echo "  2. Setup SSL Let's Encrypt di AAPanel"
echo "  3. Edit $APP_DIR/.env untuk SMTP credentials"
echo "  4. Setup domain DNS ke IP server"
echo ""
echo "  Untuk update: bash $APP_DIR/update.sh"
echo "============================================"
