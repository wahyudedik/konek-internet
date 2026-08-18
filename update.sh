#!/bin/bash
# ============================================
# Konektivitas.com — Production Update Script
# Usage: bash update.sh
# Server path: /www/wwwroot/konektivitas.com
# ============================================

set -e

# ============ KONFIGURASI ============
APP_DIR="/www/wwwroot/konektivitas.com"
PORT=8002
VENV_DIR="$APP_DIR/.venv"
LOG_DIR="/www/wwwlogs"

echo "============================================"
echo "  Konektivitas.com — Production Update"
echo "============================================"
echo ""

# ============ STEP 1: CEK ROOT ============
if [ "$EUID" -ne 0 ]; then
    echo "❌ Script ini harus dijalankan sebagai root."
    exit 1
fi

# ============ STEP 2: PULL LATEST CHANGES ============
echo "📥 [1/8] Pulling latest changes..."
cd "$APP_DIR"
git pull origin main
echo "   ✅ Repository updated."

# ============ STEP 3: SETUP VIRTUAL ENVIRONMENT ============
echo "🐍 [2/8] Activating virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    echo "   ⚠️ Virtual environment tidak ditemukan, membuat baru..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "   ✅ Virtual environment ready."

# ============ STEP 4: INSTALL DEPENDENCIES ============
echo "📦 [3/8] Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "   ✅ Dependencies updated."

# ============ STEP 5: DATABASE MIGRATION ============
echo "🗄️ [4/8] Running database migration..."
if [ -f "$APP_DIR/alembic.ini" ]; then
    alembic upgrade head 2>/dev/null && echo "   ✅ Alembic migration complete." || echo "   ⚠️ Alembic migration skipped (no pending migrations)."
else
    echo "   ℹ️ Using SQLAlchemy create_all (no Alembic). Tables auto-synced on startup."
fi

# ============ STEP 6: CLEAR CACHE ============
echo "🧹 [5/8] Clearing application cache..."
# Python bytecode cache
find "$APP_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$APP_DIR" -name "*.pyc" -delete 2>/dev/null || true
echo "   ✅ Python cache cleared."

# ============ STEP 7: RELOAD GUNICORN ============
echo "🔄 [6/8] Reloading gunicorn workers..."
if [ -S /root/.gunicorn/gunicorn.ctl ]; then
    echo "reload" | socat - UNIX-CONNECT:/root/.gunicorn/gunicorn.ctl 2>/dev/null && echo "   ✅ Gunicorn reloaded via control socket." || echo "   ⚠️ Reload via control socket gagal, coba restart..."
else
    echo "   ⚠️ Control socket tidak ditemukan, restart gunicorn..."
    pkill -f "gunicorn app.main:app" 2>/dev/null || true
    sleep 2
    nohup gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker \
        -b 127.0.0.1:$PORT \
        --access-logfile $LOG_DIR/konektivitas.com.access.log \
        --error-logfile $LOG_DIR/konektivitas.com.error.log \
        --timeout 120 \
        > /dev/null 2>&1 &
    echo "   ✅ Gunicorn started."
fi

# ============ STEP 8: LOG ROTATION ============
echo "📋 [7/8] Checking log sizes..."
if [ -f "$LOG_DIR/konektivitas.com.error.log" ]; then
    LOG_SIZE=$(du -h "$LOG_DIR/konektivitas.com.error.log" 2>/dev/null | cut -f1)
    echo "   Error log size: $LOG_SIZE"
    # Auto-truncate if log > 100MB
    LOG_BYTES=$(du -b "$LOG_DIR/konektivitas.com.error.log" 2>/dev/null | cut -f1)
    if [ "$LOG_BYTES" -gt 104857600 ] 2>/dev/null; then
        echo "   ⚠️ Log terlalu besar (>100MB), truncating..."
        truncate -s 10M "$LOG_DIR/konektivitas.com.error.log"
        echo "   ✅ Log truncated."
    fi
fi

# ============ HEALTH CHECK ============
echo "🏥 [8/8] Health check..."
sleep 3
HEALTH=$(curl -s http://localhost:$PORT/health 2>/dev/null || echo "FAILED")
if echo "$HEALTH" | grep -q "healthy"; then
    echo "   ✅ Health check passed!"
    echo ""
    echo "============================================"
    echo "  ✅ Update Selesai!"
    echo "============================================"
    echo "  Website: https://konektivitas.com"
    echo "  Health:  $HEALTH" | head -c 200
    echo ""
else
    echo "   ❌ Health check gagal!"
    echo "   Response: $HEALTH"
    echo "   Cek log: tail -50 $LOG_DIR/konektivitas.com.error.log"
    echo ""
    echo "  ❌ Update selesai dengan error. Cek log untuk detail."
    exit 1
fi
