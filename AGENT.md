# Agent Guide - Konektivitas.com

> Panduan untuk AI/agent agar mudah memahami dan mengerjakan proyek Konektivitas.com.

## Overview

**Konektivitas.com** adalah platform utilitas internet Indonesia yang menyediakan layanan dasar internet gratis, cepat, dan ringan. Bukan website tools, tetapi fondasi internet.

**Tagline:** Infrastruktur Internet Gratis untuk Indonesia

## Struktur Proyek

```
konek-internet/
├── BRIEF.md              # Brief proyek (visi, misi, target)
├── BRIEF2.md             # Detail teknis & arsitektur
├── ROADMAP.md            # Roadmap 5 tahun (2026-2031)
├── FEATURES.md           # Daftar lengkap fitur per fase
├── AGENT.md              # Dokumen ini
├── requirements.txt      # Python dependencies
├── .venv/                # Virtual environment
└── app/
    ├── __init__.py
    ├── main.py           # FastAPI app + middleware
    ├── config.py         # Konfigurasi (Pydantic)
    ├── routers/          # API endpoints (5 router, 19 endpoints)
    │   ├── dns.py        # 8 endpoints: lookup, reverse, mx, txt, cname, spf, dmarc, propagation
    │   ├── domain.py     # 2 endpoints: whois, expiry
    │   ├── ssl.py        # 2 endpoints: ssl check, expiry
    │   ├── website.py    # 4 endpoints: ping, http-status, redirect, headers
    │   └── ip.py         # 3 endpoints: ip lookup, asn, blacklist
    ├── services/         # Business logic (4 services)
    │   ├── dns_service.py    # DNS operations + @cached
    │   ├── whois_service.py  # WHOIS lookup + @cached
    │   ├── ip_service.py     # IP lookup via ip-api.com
    │   └── ssl_service.py    # SSL verification + @cached
    ├── utils/            # Helper functions
    │   ├── cache.py      # Redis + in-memory fallback cache
    │   └── rate_limit.py # Per-IP rate limiting (60 req/min)
    ├── models/           # Data models (Pydantic)
    ├── templates/        # Jinja2 HTML templates
    │   ├── base.html     # Base layout (navbar, footer, JSON-LD)
    │   ├── index.html    # Homepage (19 tools grid)
    │   ├── 404.html      # Custom 404 page
    │   └── tools/        # 19 tool pages
    └── static/           # Static files
        ├── favicon.svg   # SVG favicon
        ├── robots.txt    # SEO robots
        ├── sitemap.xml   # SEO sitemap
        ├── css/style.css # Responsive CSS
        └── js/app.js     # Frontend JavaScript
```

## Arsitektur Teknis

### Stack (2026)
- **Server:** Ubuntu + AAPanel
- **Web Server:** Nginx
- **Backend:** Python FastAPI
- **Cache:** Redis
- **Database:** SQLite → PostgreSQL (2027)

### Alur Request
```
Internet → Cloudflare → AAPanel → Nginx → FastAPI → Redis → Database
```

### Target Server
- 4 Core CPU
- RAM 6 GB
- SSD 100 GB

## Filosofi Pengembangan

### Prinsip Utama
1. **Ringan** - Semua tool harus ringan dan cepat (< 1 detik)
2. **Gratis** - Semua tools gratis digunakan
3. **Bermanfaat** - Berguna untuk banyak orang
4. **Tahan Lama** - Masih relevan 10 tahun ke depan

### Yang TIDAK Perlu
- Docker (di awal)
- Kubernetes
- Microservice
- Elasticsearch
- RabbitMQ

## Status Implementasi

### Fase 1 - MVP (2026) ✅ SELESAI
- 19 API endpoints aktif
- 19 halaman frontend
- Redis caching + in-memory fallback
- Rate limiting (60 req/min per IP)
- Security headers middleware
- SEO: JSON-LD, robots.txt, sitemap.xml, canonical URL
- Health check endpoint
- Response time display

### Cara Menjalankan
```bash
# Install dependencies
e:\PROJEKU\konek-internet\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Start server
e:\PROJEKU\konek-internet\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8002

# Akses
# Web: http://localhost:8002
# API: http://localhost:8002/api/v1/
# Docs: http://localhost:8002/docs
# Health: http://localhost:8002/health
```

## Konvensi Penamaan

### URL Pattern (kebab-case)
```
/dns-lookup          /whois-lookup       /ssl-checker
/reverse-dns         /domain-expiry      /ssl-expiry
/dns-propagation     /ping-checker       /ip-lookup
/mx-lookup           /http-status        /asn-lookup
/txt-lookup          /redirect-checker   /blacklist-checker
/cname-lookup        /header-checker
/spf-checker         /dmarc-checker
```

### API Pattern
```
GET /api/v1/dns/{domain}
GET /api/v1/dns/{domain}/reverse
GET /api/v1/dns/{domain}/mx
GET /api/v1/dns/{domain}/txt
GET /api/v1/dns/{domain}/cname
GET /api/v1/dns/{domain}/spf
GET /api/v1/dns/{domain}/dmarc
GET /api/v1/dns/{domain}/propagation
GET /api/v1/whois/{domain}
GET /api/v1/domain/{domain}/expiry
GET /api/v1/ssl/{domain}
GET /api/v1/ssl/{domain}/expiry
GET /api/v1/ping/{host}
GET /api/v1/http-status/{url}
GET /api/v1/redirect/{url}
GET /api/v1/headers/{url}
GET /api/v1/ip/{ip}
GET /api/v1/ip/{ip}/asn
GET /api/v1/ip/{ip}/blacklist
```

### Security Headers (otomatis ditambahkan)
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=(), geolocation=()
X-Process-Time: {ms}
Strict-Transport-Security: max-age=31536000 (HTTPS only)
```

## Fase Pengembangan

### Fase 1 - MVP (2026)
- 20+ tools DNS, Domain, SSL, Website, IP
- Target: 100.000 visitor/bulan
- API gratis dengan rate limit

### Fase 2 - Developer Platform (2027)
- Monitoring services
- API Key & Dashboard
- Dynamic DNS
- DNS Hosting

### Fase 3 - Infrastructure (2028)
- DNS Anycast
- Status Page
- Team Dashboard

### Fase 4 - Cloud Platform (2029)
- GeoIP Database
- ASN Database
- Enterprise features

### Fase 5 - Internet Platform (2030-2031)
- Public DNS
- Internet Intelligence
- Mobile App
- Enterprise API

## Panduan untuk AI/Agent

### Saat Mengerjakan Fitur
1. Baca FEATURES.md untuk memahami konteks fitur
2. Pastikan fitur memenuhi 3 syarat: ringan, bermanfaat, tahan lama
3. Ikuti konvensi penamaan yang sudah ada
4. Pastikan response time < 1 detik
5. Test dengan data sampel sebelum commit

### Struktur Code yang Diharapkan
```
app/
├── main.py           # FastAPI app + middleware (Security, RateLimit)
├── config.py         # Pydantic settings
├── routers/          # API endpoints (5 router, 19 endpoints)
│   ├── dns.py        # DNS: lookup, reverse, mx, txt, cname, spf, dmarc, propagation
│   ├── domain.py     # Domain: whois, expiry
│   ├── ssl.py        # SSL: check, expiry
│   ├── website.py    # Website: ping, http-status, redirect, headers
│   └── ip.py         # IP: lookup, asn, blacklist
├── services/         # Business logic (dengan @cached decorator)
│   ├── dns_service.py
│   ├── whois_service.py
│   ├── ip_service.py
│   └── ssl_service.py
├── utils/
│   ├── cache.py      # Redis + in-memory cache
│   └── rate_limit.py # Per-IP rate limiting
├── templates/        # Jinja2 HTML (19 pages)
│   ├── base.html     # Base layout + JSON-LD
│   ├── index.html    # Homepage
│   ├── 404.html      # Error page
│   └── tools/        # 19 tool pages
├── static/
│   ├── css/style.css
│   ├── js/app.js     # handleToolForm(), displayResults(), copyJSON()
│   └── favicon.svg
└── models/           # Data models
```

### Naming Convention
- **File:** snake_case.py
- **Function:** snake_case()
- **Class:** PascalCase
- **Variable:** snake_case
- **Constant:** UPPER_SNAKE_CASE
- **API Endpoint:** kebab-case (/dns-lookup)

### Performance Checklist
- [x] Response time < 1 detik
- [x] Memory usage < 100MB per request
- [x] No heavy dependencies
- [x] Redis cache untuk data yang sering diakses (+ in-memory fallback)
- [x] Graceful error handling
- [x] X-Process-Time header

### SEO Checklist
- [x] Meta title & description
- [x] Open Graph tags
- [x] Structured data (JSON-LD)
- [x] Fast loading time
- [x] Mobile friendly
- [x] robots.txt
- [x] sitemap.xml
- [x] Canonical URL

## Target Metrics

### Year 1 (2026)
- 100.000 visitor/bulan
- 2.000 user
- 30 tools
- 10.000 API request/hari

### Year 5 (2031)
- 5 juta visitor/bulan
- 100.000 developer
- 500 enterprise
- 10 juta API request/hari

## Monetisasi

### Gratis
- Semua tools
- Ada iklan

### Premium
- API access
- Monitoring services
- Dynamic DNS
- DNS Hosting
- Tanpa iklan

## Referensi Penting

- [BRIEF.md](BRIEF.md) - Visi, misi, dan target proyek
- [BRIEF2.md](BRIEF2.md) - Detail teknis dan arsitektur
- [ROADMAP.md](ROADMAP.md) - Roadmap pengembangan 5 tahun
- [FEATURES.md](FEATURES.md) - Daftar lengkap fitur per fase

---

> "Kami tidak membuat aplikasi yang viral. Kami membangun utilitas yang akan tetap dibutuhkan selama internet masih ada."