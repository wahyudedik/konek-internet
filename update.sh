#!/bin/bash
# Quick update script for Konektivitas.com
# Usage: bash update.sh
# Server path: /www/wwwroot/konektivitas.com

set -e

APP_DIR="/www/wwwroot/konektivitas.com"
PORT=8002

echo "🚀 Updating Konektivitas.com..."

# Navigate to app directory
cd "$APP_DIR"

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Reload gunicorn workers (tanpa downtime)
echo "🔄 Reloading gunicorn workers..."
if [ -S /root/.gunicorn/gunicorn.ctl ]; then
    echo "reload" | socat - UNIX-CONNECT:/root/.gunicorn/gunicorn.ctl 2>/dev/null && echo "✅ Gunicorn reloaded" || echo "⚠️ Reload via control socket gagal, coba restart..."
else
    echo "⚠️ Control socket tidak ditemukan, restart gunicorn..."
    # Kill existing gunicorn
    pkill -f "gunicorn app.main:app" 2>/dev/null || true
    sleep 1
    # Start gunicorn in background
    nohup gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker \
        -b 127.0.0.1:$PORT \
        --access-logfile /www/wwwlogs/konektivitas.com.access.log \
        --error-logfile /www/wwwlogs/konektivitas.com.error.log \
        --timeout 120 \
        > /dev/null 2>&1 &
    echo "✅ Gunicorn started"
fi

# Health check
echo "🏥 Health check:"
sleep 3
HEALTH=$(curl -s http://localhost:$PORT/health)
if echo "$HEALTH" | python3 -m json.tool 2>/dev/null; then
    echo ""
    echo "✅ Deploy selesai! Website: https://konektivitas.com"
else
    echo "⚠️ Health check gagal. Cek log: /www/wwwlogs/konektivitas.com.error.log"
    exit 1
fi
