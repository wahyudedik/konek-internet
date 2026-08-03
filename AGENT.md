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
    ├── routers/          # API endpoints (6 router, 25+ endpoints)
    │   ├── dns.py        # 8 endpoints: lookup, reverse, mx, txt, cname, spf, dmarc, propagation
    │   ├── domain.py     # 2 endpoints: whois, expiry
    │   ├── ssl.py        # 2 endpoints: ssl check, expiry
    │   ├── website.py    # 5 endpoints: ping, http-status, redirect, headers, ua
    │   ├── ip.py         # 5 endpoints: ip lookup, asn, blacklist, my-ip, port, email
    │   └── cdn.py        # 1 endpoint: cdn detect
    ├── services/         # Business logic (9 services)
    │   ├── dns_service.py    # DNS operations + @cached
    │   ├── whois_service.py  # WHOIS lookup + @cached
    │   ├── ip_service.py     # IP lookup via ip-api.com
    │   ├── ssl_service.py    # SSL verification + @cached
    │   ├── website_service.py  # HTTP fallback (HTTPS → HTTP)
    │   ├── ua_service.py       # User-Agent parser
    │   ├── email_service.py    # Email validation + disposable detection
    │   ├── port_service.py     # Port scanner
    │   └── cdn_service.py      # CDN detection (CNAME + Headers)
    ├── utils/            # Helper functions
    │   ├── cache.py      # Redis + in-memory fallback cache
    │   ├── rate_limit.py # Per-IP rate limiting (60 req/min)
    │   └── validators.py # Input validation (domain, IP, URL, host)
    ├── models/           # Data models (Pydantic)
    ├── templates/        # Jinja2 HTML templates
    │   ├── base.html     # Base layout (navbar, footer, JSON-LD)
    │   ├── index.html    # Homepage (25 tools grid)
    │   ├── 404.html      # Custom 404 page
    │   ├── about.html          # NEW - About page
    │   ├── api_docs.html       # NEW - API Documentation page
    │   ├── partials/     # Template partials
    │   │   ├── education.html  # Macro edukasi untuk tool pages
    │   │   └── breadcrumb.html # NEW - Breadcrumb navigation
    │   └── tools/        # 25 tool pages (dengan section edukasi)
    ├── data/             # Data modules
    │   ├── education.py  # Konten edukasi 25 tools
    │   └── faq_data.py   # NEW - FAQ JSON-LD (8 entries)
    └── static/           # Static files
        ├── favicon.svg   # SVG favicon
        ├── robots.txt    # SEO robots
        ├── sitemap.xml   # SEO sitemap
        ├── manifest.json # NEW - PWA manifest
        ├── sw.js         # NEW - Service Worker
        ├── css/style.css # Responsive CSS (65+ variables, dark mode)
        └── js/app.js     # Frontend JavaScript (URL state, keyboard shortcuts)
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
- 25 API endpoints aktif (+ 2 UA endpoints + CDN detect)
- 25 halaman frontend + About page + API Docs page
- 9 service files (dns, whois, ssl, ip, website, ua, email, port, cdn)
- 6 router files (dns, domain, ssl, website, ip, cdn)
- Redis caching + in-memory fallback
- Rate limiting (60 req/min per IP)
- Security headers middleware
- SEO: JSON-LD (FAQPage + BreadcrumbList), robots.txt, sitemap.xml, canonical URL
- Health check endpoint
- Response time display (X-Process-Time header)
- Section edukasi interaktif di semua 25 tool pages
- Navigation dropdown 5 kategori (DNS, Domain, SSL, Website, IP) — 25 tools
- Footer grid dengan semua 25 tools terorganisir + About + API Docs
- Search/filter tools di homepage
- Back-to-top button
- Mobile responsive: hamburger nav, dropdown, stacked forms, card layout
- 404 page dengan tool suggestions
- Input validation di semua endpoints (validate_domain, validate_ip, validate_url, validate_host)
- Async non-blocking di semua services (asyncio.to_thread)
- XSS protection di copyJSON function (JavaScript Map)
- HTTP fallback (HTTPS → HTTP) di website service
- Tool History localStorage (10 query terakhir per tool)
- URL Query State (shareable URLs)
- Dark Mode Toggle (65+ CSS variables, localStorage, system preference)
- Keyboard Shortcuts (Ctrl+K search, Escape close)
- PWA Support (manifest.json + service worker)
- WHOIS extra fields (registrant, admin/tech contact, updated_date)
- SSL chain info (SANs, signature algorithm, chain depth)
- HTTP version detection (HTTP/1.0, 1.1, 2, 3)
- Breadcrumb links ke category
- FAQ JSON-LD Schema (8 FAQ entries)
- CDN Detection (CNAME + Header analysis) — tool ke-25
- XSS protection di history items (event delegation)
- HTTP client reuse di redirect checker
- Email validator: free email provider detection

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
# About: http://localhost:8002/about
# API Docs: http://localhost:8002/api-docs
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
/my-ip
/ua-checker
/email-validator
/ns-lookup
/port-scanner
/cdn-detect
/about
/api-docs
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
GET /api/v1/ip/me
GET /api/v1/ua
GET /api/v1/ua/{encoded_ua:path}
GET /api/v1/email/{email}/validate
GET /api/v1/port/{host}?ports=80,443,22
GET /api/v1/cdn/{domain}/detect
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

### Fase 1 - MVP (2026) ✅ SELESAI
- 25 tools DNS, Domain, SSL, Website, IP (+CDN Detection)
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
├── routers/          # API endpoints (6 router, 25+ endpoints)
│   ├── dns.py        # DNS: lookup, reverse, mx, txt, cname, spf, dmarc, propagation
│   ├── domain.py     # Domain: whois, expiry
│   ├── ssl.py        # SSL: check, expiry
│   ├── website.py    # Website: ping, http-status, redirect, headers, ua
│   ├── ip.py         # IP: lookup, asn, blacklist, my-ip, port, email
│   └── cdn.py        # CDN: detect
├── services/         # Business logic (dengan @cached decorator)
│   ├── dns_service.py
│   ├── whois_service.py
│   ├── ip_service.py
│   ├── ssl_service.py
│   ├── website_service.py  # HTTP fallback
│   ├── ua_service.py       # User-Agent parser
│   ├── email_service.py    # Email validation + disposable detection
│   ├── port_service.py     # Port scanner
│   └── cdn_service.py      # CDN detection (CNAME + Headers)
├── utils/
│   ├── cache.py      # Redis + in-memory cache
│   ├── rate_limit.py # Per-IP rate limiting
│   └── validators.py # Input validation (domain, IP, URL, host)
├── templates/        # Jinja2 HTML (25 tool pages + about + api_docs)
│   ├── base.html     # Base layout + JSON-LD
│   ├── index.html    # Homepage
│   ├── 404.html      # Error page
│   ├── about.html    # About page
│   ├── api_docs.html # API Documentation
│   ├── partials/
│   │   ├── education.html
│   │   └── breadcrumb.html
│   └── tools/        # 25 tool pages
├── data/
│   ├── education.py  # Konten edukasi 25 tools
│   └── faq_data.py   # FAQ JSON-LD (8 entries)
├── static/
│   ├── css/style.css
│   ├── js/app.js     # handleToolForm(), displayResults(), copyJSON()
│   ├── favicon.svg
│   ├── manifest.json # PWA
│   └── sw.js         # Service Worker
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
- [x] Async non-blocking (asyncio.to_thread untuk semua blocking operations)
- [x] HTTP fallback (HTTPS → HTTP)

### SEO Checklist
- [x] Meta title & description
- [x] Open Graph tags
- [x] Structured data (JSON-LD: BreadcrumbList + FAQPage)
- [x] Fast loading time
- [x] Mobile friendly
- [x] robots.txt
- [x] sitemap.xml
- [x] Canonical URL
- [x] FAQ rich snippets

### Feature Checklist
- [x] Dark mode toggle (65+ CSS variables)
- [x] Tool history (localStorage, 10 per tool)
- [x] URL query state (shareable URLs)
- [x] Keyboard shortcuts (Ctrl+K, Escape)
- [x] PWA support (manifest.json + service worker)
- [x] Mobile card layout (result tables)
- [x] Breadcrumb navigation (clickable categories)
- [x] Input validation (all endpoints)
- [x] WHOIS extra fields (registrant, contacts)
- [x] SSL chain info (SANs, signature)
- [x] HTTP version detection (1.0, 1.1, 2, 3)
- [x] CDN Detection (CNAME + Header analysis)
- [x] XSS protection in history items
- [x] Email validator: free email detection

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
