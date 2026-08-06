# 🚀 Deployment Guide - Konektivitas.com (AAPanel)

Panduan deployment ke production server menggunakan **AAPanel**.

---

## Server Requirements

- **OS:** Ubuntu 22.04 LTS
- **CPU:** 4 Core
- **RAM:** 6 GB
- **Storage:** 100 GB SSD
- **Panel:** AAPanel (https://aa-panel.com)

---

## 1. Install AAPanel

```bash
# Install AAPanel (Ubuntu/Debian)
wget -O install.sh http://www.aapanel.com/script/install-ubuntu_6.0_en.sh && sudo bash install.sh aapanel
```

Setelah install, akses panel di:
```
http://YOUR_SERVER_IP:8888
```

**Catatan penting:** Simpan URL login, username, dan password yang muncul di terminal setelah install.

### Install App via AAPanel

Buka **App Store** di AAPanel dan install:
- **Nginx** (versi terbaru)
- **Redis** (versi terbaru)
- **Python Manager** (Project Manager untuk Python)
- **Let's Encrypt** (untuk SSL, bisa juga dari panel)

---

## 2. Upload Project ke Server

### Via Git (Recommended)
```bash
# SSH ke server
ssh root@YOUR_SERVER_IP

# Masuk ke directory web
cd /www/wwwroot/

# Clone repository
git clone https://github.com/your-username/konek-internet.git konektivitas

# Masuk ke project
cd konektivitas
```

### Via Upload (Alternative)
1. Buka **Files** di AAPanel
2. Navigasi ke `/www/wwwroot/`
3. Buat folder `konektivitas`
4. Upload semua file project (zip, lalu extract)

---

## 3. Setup Python Project di AAPanel

### Buka Python Manager
1. Login AAPanel → **App Store** → **Python Manager** (Project Manager)
2. Klik **Add Project**

### Konfigurasi Project
| Field | Value |
|-------|-------|
| **Project Name** | `konektivitas` |
| **Project Path** | `/www/wwwroot/konektivitas` |
| **Python Version** | Python 3.11 (pilih yang tersedia) |
| **Run Command** | `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8000` |
| **Run Directory** | `/www/wwwroot/konektivitas` |
| **Startup File** | (kosongkan) |

> **Catatan:** Jika Python 3.11 belum tersedia di Python Manager, install dulu via **App Store** → cari "Python 3.11" atau gunakan versi Python yang tersedia.

### Install Dependencies
Buka **Terminal** di AAPanel atau SSH:
```bash
cd /www/wwwroot/konektivitas

# Buat virtual environment
python3.11 -m venv .venv

# Activate venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### Start Project
Di Python Manager, klik **Start** pada project `konektivitas`.

Status harusnya berubah menjadi **Running** (hijau).

---

## 4. Environment Configuration

### Setup .env
```bash
cd /www/wwwroot/konektivitas
cp .env.example .env
nano .env
```

Isi `.env` dengan values production:
```env
APP_NAME=Konektivitas.com
APP_VERSION=1.0.0
DEBUG=false
HOST=127.0.0.1
PORT=8000
REDIS_URL=redis://localhost:6379/0
RATE_LIMIT_PER_MINUTE=60
ALLOWED_ORIGINS=https://konektivitas.com,https://www.konektivitas.com
API_V1_PREFIX=/api/v1
```

**PENTING:** 
- `HOST=127.0.0.1` (bukan 0.0.0.0) karena Nginx akan jadi reverse proxy
- `ALLOWED_ORIGINS` isi dengan domain production kamu
- Jangan commit `.env` ke git repository

---

## 5. Setup Website di AAPanel

### Tambah Website
1. Login AAPanel → **Website** → **Add Site**
2. Isi konfigurasi:

| Field | Value |
|-------|-------|
| **Domain** | `konektivitas.com` |
| **Secondary Domain** | `www.konektivitas.com` |
| **Root Directory** | `/www/wwwroot/konektivitas` |
| **PHP Version** | `Pure Static` atau `Do Not Create` |
| **Database** | Tidak perlu (None) |

### Konfigurasi Nginx (Reverse Proxy)
1. Klik **Settings** pada website `konektivitas.com`
2. Buka tab **Configuration File** (Nginx config)
3. **Hapus semua** isi yang ada
4. **Paste** konfigurasi berikut:

```nginx
# HTTP -> HTTPS Redirect
server {
    listen 80;
    server_name konektivitas.com www.konektivitas.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS Server
server {
    listen 443 ssl http2;
    server_name konektivitas.com www.konektivitas.com;
    
    # Root directory
    root /www/wwwroot/konektivitas;
    index index.html;

    # SSL (Let's Encrypt via AAPanel)
    ssl_certificate /www/server/panel/vhost/cert/konektivitas.com/fullchain.pem;
    ssl_certificate_key /www/server/panel/vhost/cert/konektivitas.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip Compression
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml;
    gzip_min_length 1000;

    # Static Files (direct from Nginx - faster)
    location /static/ {
        alias /www/wwwroot/konektivitas/app/static/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Favicon
    location /favicon.ico {
        alias /www/wwwroot/konektivitas/app/static/favicon.png;
    }

    # API and Pages (proxy to FastAPI)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 30s;
        proxy_connect_timeout 5s;
    }
}
```

5. Klik **Save** (Simpan)
6. Nginx akan otomatis restart

---

## 6. Setup SSL via AAPanel

### Method 1: Let's Encrypt (Recommended)
1. AAPanel → **Website** → Klik **Settings** pada `konektivitas.com`
2. Buka tab **SSL**
3. Pilih **Let's Encrypt**
4. Centang domain `konektivitas.com` dan `www.konektivitas.com`
5. Klik **Apply** (Apply/Issue)
6. Aktifkan **Force HTTPS**

### Method 2: Cloudflare
Jika menggunakan Cloudflare:
1. Aktifkan **SSL/TLS** di Cloudflare dashboard → **Full (Strict)**
2. Di AAPanel, SSL tidak perlu diaktifkan (atau gunakan self-signed cert)
3. Pastikan proxy (orange cloud) aktif di Cloudflare

---

## 7. First Deploy & Test

```bash
# SSH ke server
ssh root@YOUR_SERVER_IP

# Masuk ke project
cd /www/wwwroot/konektivitas

# Setup .env
cp .env.example .env
nano .env  # edit values production

# Setup venv & install
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Restart project via AAPanel
# Atau via terminal:
# Kill existing process lalu start ulang dari Python Manager
```

### Test
```bash
# Test langsung ke port
curl http://127.0.0.1:8000/health

# Test via Nginx (HTTPS)
curl https://konektivitas.com/health

# Test website
curl -I https://konektivitas.com/
```

---

## 8. Update Deployment

### Via AAPanel Terminal (Recommended)
1. Login AAPanel → **Terminal**
2. Jalankan:
```bash
cd /www/wwwroot/konektivitas
git pull origin main
source .venv/bin/activate
pip install -q -r requirements.txt
```
3. Restart project dari **Python Manager** → klik **Restart**

### Via SSH
```bash
ssh root@YOUR_SERVER_IP
cd /www/wwwroot/konektivitas
git pull origin main
source .venv/bin/activate
pip install -q -r requirements.txt
```

Lalu restart dari AAPanel → **Python Manager** → **Restart**.

### Quick Update Script
```bash
#!/bin/bash
# update.sh - Quick update Konektivitas.com
cd /www/wwwroot/konektivitas
git pull origin main
source .venv/bin/activate
pip install -q -r requirements.txt
echo "✅ Code updated! Restart project dari AAPanel Python Manager."
echo "🏥 Health check:"
curl -s http://127.0.0.1:8000/health | python3 -m json.tool
```

---

## 9. Monitoring & Logs

### Via AAPanel
- **Python Manager** → Lihat status project (Running/Stopped)
- **Logs** → Lihat log error project
- **Website** → Settings → **Logs** (Nginx access/error logs)

### Via Terminal
```bash
# Cek status Python process
ps aux | grep gunicorn

# Cek port 8000
netstat -tlnp | grep 8000

# Health check
curl http://127.0.0.1:8000/health

# Cek Redis
redis-cli ping
```

---

## 10. Troubleshooting

| Masalah | Solusi |
|---------|--------|
| **Project not starting** | Cek log di Python Manager. Pastikan venv dan dependencies terinstall |
| **502 Bad Gateway** | Project belum running. Start dari Python Manager |
| **Static files 404** | Cek path `alias` di Nginx config: `/www/wwwroot/konektivitas/app/static/` |
| **SSL error** | Pastikan SSL sudah apply di AAPanel. Cek path cert di Nginx config |
| **Redis error** | Pastikan Redis install dan running di AAPanel App Store |
| **Rate limit tidak jalan** | Pastikan Redis running: `redis-cli ping` harus return `PONG` |
| **CORS error** | Cek `ALLOWED_ORIGINS` di `.env` sudah sesuai dengan domain |
| **Port conflict** | Pastikan port 8000 tidak dipakai app lain: `netstat -tlnp | grep 8000` |

---

## 11. Rollback

```bash
cd /www/wwwroot/konektivitas

# Lihat history
git log --oneline -10

# Rollback ke commit tertentu
git checkout <commit-hash>

# Restart dari AAPanel Python Manager
```

---

## Quick Reference

### AAPanel Navigation
| Menu | Fungsi |
|------|--------|
| **Website** | Manage website, SSL, Nginx config |
| **App Store** | Install Redis, Python Manager |
| **Python Manager** | Start/Stop/Restart Python project |
| **Files** | Browse/edit files di server |
| **Terminal** | SSH terminal langsung dari panel |
| **Logs** | View Nginx dan project logs |

### Commands
| Command | Description |
|---------|-------------|
| Python Manager → Start | Start project |
| Python Manager → Restart | Restart project |
| Python Manager → Stop | Stop project |
| `curl http://127.0.0.1:8000/health` | Health check |
| `redis-cli ping` | Check Redis |
| `git pull origin main` | Update code |

---

> **Tip:** Untuk production, gunakan **Cloudflare** sebagai DNS + CDN + DDoS protection. AAPanel hanya handle Nginx + Python. Cloudflare handle sisanya.
