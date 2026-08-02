#!/bin/bash
# Quick update script for Konektivitas.com
# Usage: bash update.sh

set -e

echo "🚀 Updating Konektivitas.com..."

# Navigate to app directory (adjust path as needed)
cd /var/www/konektivitas

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Restart service
echo "🔄 Restarting service..."
sudo supervisorctl restart konektivitas

# Health check
echo "🏥 Health check:"
sleep 2
curl -s http://localhost:8000/health | python3 -m json.tool

echo "✅ Deploy selesai!"
