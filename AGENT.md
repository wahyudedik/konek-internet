# Agent Guide - Konektivitas.com

> Panduan untuk AI/agent agar mudah memahami dan mengerjakan proyek Konektivitas.com.

## Overview

Internet menjadi fondasi hampir semua layanan digital. Website, aplikasi mobile, AI, IoT, sistem perusahaan, hingga perangkat pintar bergantung pada infrastruktur internet untuk beroperasi.

Namun, mengelola infrastruktur tersebut masih tersebar di banyak layanan dan sering kali rumit.

**Konektivitas hadir untuk menyederhanakan cara orang memahami, mengelola, dan mengembangkan aset internet mereka.**

> **"Konektivitas.com adalah platform yang menghubungkan manusia dengan infrastruktur internet—membantu siapa pun memahami, mengelola, dan menemukan peluang dari aset digital mereka dalam satu tempat."**

**Tagline:** "Memahami. Mengelola. Mengembangkan Internet."

## Visi

**Menjadi platform infrastruktur internet terdepan di Indonesia yang membantu individu dan bisnis memahami, mengelola, dan mengembangkan aset digital mereka.**

### Misi

1. Menyederhanakan pengelolaan infrastruktur internet.
2. Menyediakan monitoring yang mudah dipahami.
3. Memberikan edukasi internet dalam bahasa Indonesia.
4. Membantu pengguna mengambil keputusan berdasarkan data.
5. Menjadi pusat kendali aset internet.

### Value Proposition

Daripada membuka banyak layanan berbeda, pengguna cukup membuka Konektivitas untuk mendapatkan gambaran menyeluruh tentang aset internet mereka.

### Filosofi

Kebanyakan orang hanya melihat website. Konektivitas membantu melihat seluruh infrastruktur yang membuat website tersebut dapat berjalan.

### Positioning

**Bukan:**

- Domain Registrar
- Hosting Provider
- Cloud Provider

**Tetapi:** Platform Infrastruktur Internet.

### Pertanyaan Penuntun

Setiap fitur baru harus menjawab setidaknya satu dari tiga pertanyaan berikut:

1. **"Apakah fitur ini membantu pengguna memahami internet?"** *(Learn)*
2. **"Apakah fitur ini membantu pengguna mengelola aset internetnya?"** *(Manage)*
3. **"Apakah fitur ini membantu pengguna menemukan peluang atau mengambil keputusan?"** *(Discover)*

Kalau jawabannya "ya", berarti fitur tersebut sejalan dengan visi Konektivitas. Kalau tidak, lebih baik ditunda agar produk tetap fokus dan identitasnya tidak melebar ke mana-mana.

---

## 3 Pilar Produk

### 1. Learn — Membantu orang memahami internet

**Implementasi:** Public Tools (gratis)

- Edukasi DNS, SSL, Email, Server, HTTP
- Visualisasi cara kerja internet
- Dokumentasi lengkap
- 25+ tools DNS, Domain, SSL, Website, IP (saat ini)
- Target: 100+ tools (2031)
- API gratis dengan rate limit

**Target Pengguna:** Pelajar, Mahasiswa, Guru, Developer pemula

### 2. Manage — Mengelola aset internet

**Implementasi:** Workspace (Pro & Team)

- Domain Management
- SSL, DNS, Server, Email Monitoring
- Team Workspace & Kolaborasi
- Notifikasi (Email, Telegram, Discord)
- Riwayat & Laporan

**Target Pengguna:** Developer, IT Support, SysAdmin, Agency, Startup

### 3. Discover — Menemukan peluang

**Implementasi:** Business Intelligence (Enterprise)

- Business Discovery & Industry Insight
- Technology Insight & Digital Opportunity
- Analisis aset digital berbasis data publik
- Custom Reports

**Target Pengguna:** Business Owner, Konsultan, Freelancer, Marketing

---

## Target Pengguna

### 🌐 Public — Belajar, Mengecek, Mencari referensi

Pelajar, Mahasiswa, Freelancer, Developer pemula, Ide startup

### 💼 Professional — Monitoring, Workspace, Manajemen aset

Developer, DevOps, IT Support, SysAdmin, Agency, Startup

### 🏢 Business — Insight, Peluang, Analisis

UMKM, Perusahaan, Konsultan, Marketing, Investor, Business Owner

---

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
    │   ├── about.html    # About page
    │   ├── api_docs.html # API Documentation page
    │   ├── partials/     # Template partials
    │   │   ├── education.html  # Macro edukasi untuk tool pages
    │   │   └── breadcrumb.html # Breadcrumb navigation
    │   └── tools/        # 25 tool pages (dengan section edukasi)
    ├── data/             # Data modules
    │   ├── education.py  # Konten edukasi 25 tools
    │   └── faq_data.py   # FAQ JSON-LD (8 entries)
    └── static/           # Static files
        ├── favicon.png   # PNG favicon
        ├── robots.txt    # SEO robots
        ├── sitemap.xml   # SEO sitemap
        ├── manifest.json # PWA manifest
        ├── sw.js         # Service Worker
        ├── css/style.css # Responsive CSS (65+ variables, dark mode)
        └── js/app.js     # Frontend JavaScript (URL state, keyboard shortcuts)
```

---

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

---

## Filosofi Pengembangan

### Prinsip Utama
1. **Ringan** — Semua tool harus ringan dan cepat (< 1 detik)
2. **Gratis** — Public tools gratis digunakan
3. **Bermanfaat** — Berguna untuk banyak orang
4. **Tahan Lama** — Masih relevan 10 tahun ke depan

### Framework Keputusan Fitur

Gunakan **dua framework** saat memutuskan fitur baru:

**Framework 1 — Arah Produk (3 Pertanyaan Pilar):**

Apakah fitur ini membantu pengguna memahami internet *(Learn)*, mengelola aset internetnya *(Manage)*, atau menemukan peluang *(Discover)*? Kalau tidak menjawab salah satunya, tolak.

**Framework 2 — Kelayakan Teknis (3 Syarat):**

1. Ringan dijalankan (sesuai spesifikasi server)
2. Berguna untuk banyak orang
3. Masih relevan 10 tahun ke depan

> Fitur harus lolos **kedua** framework sebelum diimplementasikan.

### Yang TIDAK Perlu
- Docker (di awal)
- Kubernetes
- Microservice
- Elasticsearch
- RabbitMQ

---

## Status Implementasi

### Fase 1 — Public Tools MVP (2026) ✅ SELESAI

#### Public Tools
- 25 API endpoints aktif (+ 2 UA endpoints + CDN detect)
- 25 halaman frontend + About page + API Docs page
- 9 service files (dns, whois, ssl, ip, website, ua, email, port, cdn)
- 6 router files (dns, domain, ssl, website, ip, cdn)

#### Core Infrastructure
- Redis caching + in-memory fallback
- Rate limiting (60 req/min per IP)
- Security headers middleware
- Input validation di semua endpoints (validate_domain, validate_ip, validate_url, validate_host)
- Async non-blocking di semua services (asyncio.to_thread)

#### SEO
- JSON-LD (FAQPage + BreadcrumbList)
- robots.txt, sitemap.xml, canonical URL
- FAQ rich snippets

#### User Experience
- Dark Mode Toggle (65+ CSS variables, localStorage, system preference)
- Dark Mode System Sync (matchMedia listener, real-time preference update)
- Mobile responsive: hamburger nav, dropdown, stacked forms, card layout
- Tablet responsive (768px-1024px breakpoint, 2-column grid)
- Tool History localStorage (10 query terakhir per tool)
- URL Query State (shareable URLs)
- Keyboard Shortcuts (Ctrl+K search, Escape close, Ctrl+D dark mode)
- Keyboard Navigation (arrow keys untuk tool cards, WCAG compliant)
- PWA Support (manifest.json + service worker)
- Tool Page Preloading (prefetch on hover untuk navigasi cepat)
- Section edukasi interaktif di semua 25 tool pages
- Navigation dropdown 5 kategori (DNS, Domain, SSL, Website, IP)
- Footer grid dengan semua 25 tools terorganisir + About + API Docs
- Search/filter tools di homepage
- Back-to-top button
- 404 page dengan tool suggestions

#### Advanced Features
- WHOIS extra fields (registrant, admin/tech contact, updated_date)
- SSL chain info (SANs, signature algorithm, chain depth)
- HTTP version detection (HTTP/1.0, 1.1, 2, 3)
- CDN Detection (CNAME + Header analysis) — tool ke-25
- Email validator: free email provider detection
- HTTP fallback (HTTPS → HTTP) di website service
- HTTP client reuse (shared httpx.AsyncClient + connection pooling)
- Cache TTL tuning (blacklist 10min, CDN 1hr, DNS/Website 1-5min)
- XSS protection di copyJSON function (JavaScript Map)
- XSS protection di history items (event delegation)
- Breadcrumb links ke category
- Health check endpoint
- Response time display (X-Process-Time header)
- Request ID (X-Request-ID header untuk distributed tracing)
- Touch-friendly tap targets (WCAG 2.5.5, minimum 44px)

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

---

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
X-Request-ID: {uuid-8char}
Strict-Transport-Security: max-age=31536000 (HTTPS only)
```

---

## Roadmap (Ringkasan)

### Fase 1 — Foundation (2026) ✅ SELESAI
- 25 Public Tools (DNS, Domain, SSL, Website, IP)
- API gratis dengan rate limit
- Target: 100.000 visitor/bulan

### Fase 2 — Developer Platform & Workspace MVP (2027)
- 5 tools tambahan (total 30)
- User Authentication & Workspace
- Domain, SSL, DNS, Uptime Monitoring
- API Key System & Dashboard
- Dynamic DNS
- Target: 500.000 visitor/bulan, 100 premium subscribers

### Fase 3 — Infrastructure & Mobile (2028)
- Total 40+ tools
- Team Workspace & Shared Monitoring
- DNS Hosting & DNS Anycast (bertahap)
- Status Page
- Mobile App (Android)
- Target: 1 juta visitor/bulan, 1.000 premium subscribers

### Fase 4 — Business Intelligence (2029)
- Total 50+ tools
- Enterprise features (SSO, Audit Log, SLA)
- BI: Market Analysis, Technology Detection, Opportunity Finder
- GeoIP & ASN Database
- Load Balancer
- Target: 3 juta visitor/bulan, 50 enterprise clients

### Fase 5 — Internet Platform (2030-2031)
- 100+ tools
- Public DNS (dns.konektivitas.com)
- Internet Intelligence (BGP, IXP, Latency Map)
- Developer Marketplace
- Mobile App (Android + iOS)
- Multi Region
- Target: 5 juta visitor/bulan, 500 enterprise, 10 juta API request/hari

Detail lengkap di [ROADMAP.md](ROADMAP.md).

---

## Panduan untuk AI/Agent

### Saat Mengerjakan Fitur
1. Baca [FEATURES.md](FEATURES.md) untuk memahami konteks fitur
2. Gunakan **Framework Keputusan Fitur** (lihat section Filosofi Pengembangan)
3. Tanyakan: "Apakah fitur ini membantu pengguna **memahami** *(Learn)*, **mengelola** *(Manage)*, atau **menemukan peluang** *(Discover)*?"
4. Pastikan fitur memenuhi 3 syarat: **ringan**, **bermanfaat**, **tahan lama**
5. Ikuti konvensi penamaan yang sudah ada
6. Pastikan response time < 1 detik
7. Test dengan data sampel sebelum commit

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
│   ├── favicon.png
│   ├── logo.png
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
- [x] X-Request-ID header (distributed tracing)
- [x] Async non-blocking (asyncio.to_thread untuk semua blocking operations)
- [x] HTTP fallback (HTTPS → HTTP)
- [x] HTTP client reuse (shared httpx.AsyncClient + connection pooling)
- [x] Cache TTL tuning (optimized per data volatility)

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
- [x] Dark mode toggle (65+ CSS variables, localStorage, system preference sync)
- [x] Dark mode system sync (matchMedia listener, real-time preference)
- [x] Tool history (localStorage, 10 per tool)
- [x] URL query state (shareable URLs)
- [x] Keyboard shortcuts (Ctrl+K, Escape, Ctrl+D)
- [x] Keyboard navigation (arrow keys untuk tool cards, WCAG)
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
- [x] Tool page preloading (prefetch on hover)
- [x] Touch-friendly tap targets (WCAG 2.5.5, minimum 44px)
- [x] Tablet responsive (768px-1024px breakpoint)

---

## Target Metrics

### Year 1 (2026) — Foundation ✅ SELESAI

| Metric | Target | Status |
|--------|--------|--------|
| Visitor/bulan | 100.000 | 🔄 |
| Tools | 25 | ✅ |
| API request/hari | 10.000 | 🔄 |

### Year 2 (2027) — Developer Platform & Workspace

| Metric | Target |
|--------|--------|
| Visitor/bulan | 500.000 |
| Registered users | 10.000 |
| Pro subscribers | 100 |
| Domain monitored | 5.000 |

### Year 3 (2028) — Infrastructure & Mobile

| Metric | Target |
|--------|--------|
| Visitor/bulan | 1.000.000 |
| Registered users | 50.000 |
| Pro subscribers | 1.000 |
| Mobile app installs | 10.000 |

### Year 4 (2029) — Business Intelligence

| Metric | Target |
|--------|--------|
| Visitor/bulan | 3.000.000 |
| Registered users | 100.000 |
| Enterprise clients | 50 |
| API request/hari | 1.000.000 |

### Year 5 (2030-2031) — Internet Platform

| Metric | Target |
|--------|--------|
| Visitor/bulan | 5.000.000 |
| Registered users | 500.000 |
| Pro subscribers | 20.000 |
| Enterprise clients | 500 |
| Public DNS users | 1.000.000 |
| API request/hari | 10.000.000 |

---

## Monetisasi

### Free
- Public tools (25+ → 100+ tools)
- Edukasi internet
- API dengan rate limit

### Pro (Rp 49.000/bulan)
- Workspace (Domain, SSL, DNS, Server, Email Monitoring)
- Notification (Email, Telegram, Discord)
- Laporan & Export
- Tanpa iklan

### Team (Rp 99.000-199.000/bulan)
- Semua fitur Pro
- Team Workspace & Kolaborasi
- Shared Monitoring
- DNS Hosting
- Multi-user access
- Role & Permission

### Enterprise (Rp 500.000-5.000.000/bulan)
- Business Intelligence
- Dashboard perusahaan
- Integrasi & Analitik
- SSO, Audit Log, SLA
- Custom Reports
- Priority Support

---

## Nilai yang Dijual

Bukan domain. Bukan hosting. Bukan server.

Yang dijual adalah:

- **Kejelasan** — Memahami infrastruktur internet
- **Monitoring** — Peringatan dini sebelum masalah terjadi
- **Edukasi** — Belajar internet dalam bahasa Indonesia
- **Insight** — Data untuk pengambilan keputusan
- **Efisiensi** — Satu tempat untuk semua aset internet
- **Produktivitas** — Mengelola aset internet lebih cepat
- **Kepercayaan** — Platform yang bisa diandalkan

---

# Hub.konektivitas.com — Blockchain Infrastructure

> Panduan untuk AI/agent agar mudah memahami dan mengerjakan proyek Hub.konektivitas.com.

**Detail:** [`plans/hub-konektivitas-plan.md`](plans/hub-konektivitas-plan.md)

## Overview

Hub.konektivitas.com adalah platform infrastruktur blockchain yang menyediakan akses node RPC API untuk developer, startup, perusahaan, dan aplikasi Web3 tanpa harus menjalankan node sendiri.

Fokus utama proyek ini adalah menyediakan layanan yang cepat, stabil, aman, dan mudah diintegrasikan melalui API.

## Visi

Menjadi penyedia infrastruktur konektivitas blockchain yang sederhana, cepat, dan andal untuk developer di Indonesia maupun global.

## Misi

1. Menyediakan RPC Node berkinerja tinggi.
2. Mempermudah integrasi blockchain melalui REST API dan JSON-RPC.
3. Menyediakan endpoint yang stabil dengan uptime tinggi.
4. Mendukung berbagai jaringan blockchain populer.
5. Menjadi fondasi berbagai aplikasi Web3.

## Layanan

- **Public RPC Endpoint** — Akses publik tanpa registrasi
- **Private RPC Endpoint** — Akses privat dengan API key
- **JSON-RPC API** — Standar JSON-RPC 2.0
- **WebSocket Endpoint** — Real-time event subscriptions
- **Blockchain Data API** — Block, transaction, address data
- **Transaction Broadcast API** — Broadcast transaksi
- **Block Explorer API** — Data explorasi block
- **Address Balance API** — Cek saldo alamat
- **Smart Contract API** — Interaksi smart contract
- **Monitoring and Status API** — Status kesehatan node

## Target Pengguna

- Developer blockchain
- Startup Web3
- Perusahaan / Fintech
- Wallet / Exchange
- Game Blockchain / NFT Platform
- AI Agent / IoT

## Arsitektur

```
Client Apps → Nginx → FastAPI → PostgreSQL
                            → Redis Cache
                            → Blockchain Nodes
                            → Prometheus → Grafana
```

### Alur Request

1. Client mengirim JSON-RPC request
2. Nginx menerima dan forward ke FastAPI
3. FastAPI memvalidasi API key
4. FastAPI memeriksa rate limit
5. FastAPI memeriksa cache (Redis)
6. Jika cache miss, forward ke blockchain node
7. Response disimpan di cache
8. Request dilog ke PostgreSQL
9. Response dikembalikan ke client

## Struktur Direktori

```
hub-konektivitas/
├── app/
│   ├── main.py                 # FastAPI app utama
│   ├── config.py               # Konfigurasi Pydantic
│   ├── dependencies.py         # Dependency injection
│   ├── middleware/
│   │   ├── auth.py             # API Key authentication
│   │   ├── rate_limit.py       # Rate limiting
│   │   └── logging.py          # Request logging
│   ├── models/
│   │   ├── user.py             # User model
│   │   ├── api_key.py          # API Key model
│   │   ├── usage.py            # Usage tracking
│   │   └── blockchain.py       # Network model
│   ├── routers/
│   │   ├── auth.py             # Login, Register
│   │   ├── dashboard.py        # Dashboard endpoints
│   │   ├── rpc.py              # JSON-RPC proxy
│   │   ├── blockchain.py       # Blockchain data
│   │   ├── monitoring.py       # Status and health
│   │   └── admin.py            # Admin endpoints
│   ├── services/
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── api_key_service.py  # API Key CRUD
│   │   ├── rpc_service.py      # RPC proxy logic
│   │   ├── blockchain_service.py # Blockchain interactions
│   │   └── usage_service.py    # Usage tracking
│   ├── utils/
│   │   ├── cache.py            # Redis + in-memory cache
│   │   ├── crypto.py           # API key hashing, JWT
│   │   └── validators.py       # Input validation
│   ├── templates/
│   │   ├── base.html           # Base layout
│   │   ├── index.html          # Landing page
│   │   ├── dashboard.html      # User dashboard
│   │   ├── login.html          # Login page
│   │   ├── register.html       # Register page
│   │   ├── api_keys.html       # API Key management
│   │   └── docs.html           # API documentation
│   └── static/
│       ├── css/style.css
│       ├── js/app.js
│       └── favicon.png
├── alembic/                    # Database migrations
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

## API Endpoints

### Authentication

```
POST   /api/v1/auth/register       # Register new user
POST   /api/v1/auth/login          # Login
POST   /api/v1/auth/refresh        # Refresh token
GET    /api/v1/auth/me             # Get current user
PUT    /api/v1/auth/me             # Update profile
```

### API Keys

```
GET    /api/v1/keys               # List API keys
POST   /api/v1/keys               # Create API key
DELETE /api/v1/keys/{id}          # Revoke API key
PUT    /api/v1/keys/{id}          # Update API key
```

### RPC Proxy

```
POST   /rpc/{network}             # JSON-RPC proxy
GET    /rpc/{network}/health      # Node health check
```

### Blockchain Data

```
GET    /api/v1/networks           # List supported networks
GET    /api/v1/networks/{slug}    # Network details
GET    /api/v1/{network}/block/{id}  # Get block
GET    /api/v1/{network}/tx/{hash}   # Get transaction
GET    /api/v1/{network}/address/{addr} # Get address info
GET    /api/v1/{network}/balance/{addr} # Get balance
POST   /api/v1/{network}/broadcast    # Broadcast transaction
```

### Monitoring

```
GET    /api/v1/status             # System status
GET    /api/v1/status/{network}   # Network status
GET    /api/v1/usage              # Usage statistics
```

## Database Schema

### Users

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | Unique email |
| password_hash | VARCHAR(255) | Bcrypt hash |
| full_name | VARCHAR(255) | Nama lengkap |
| plan | VARCHAR(50) | free/pro/team |
| created_at | TIMESTAMP | Tanggal daftar |

### API Keys

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key ke users |
| name | VARCHAR(100) | Nama key |
| key_hash | VARCHAR(255) | SHA-256 hash |
| key_prefix | VARCHAR(10) | Prefix untuk display |
| networks | TEXT[] | Blockchain networks |
| rate_limit | INTEGER | Request per menit |
| is_active | BOOLEAN | Status aktif |

### Usage Logs

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| api_key_id | UUID | Foreign key |
| network | VARCHAR(50) | Blockchain network |
| method | VARCHAR(100) | RPC method |
| response_time_ms | INTEGER | Response time |
| status_code | INTEGER | HTTP status |

### Blockchain Networks

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(100) | Network name |
| slug | VARCHAR(50) | URL-friendly name |
| chain_id | INTEGER | Chain ID |
| rpc_endpoint | TEXT | RPC URL |
| is_active | BOOLEAN | Status aktif |

## Konvensi Penamaan

### File
- snake_case.py untuk semua file Python

### Function
- snake_case() untuk semua function

### Class
- PascalCase untuk semua class

### Variable
- snake_case untuk semua variable

### API Endpoint
- kebab-case untuk URL
- `/api/v1/{resource}` untuk REST
- `/rpc/{network}` untuk RPC proxy

### API Key Prefix
- `hk_` untuk Hub.konektivitas.com

## Security

### API Key Security
- API key di-hash dengan SHA-256 sebelum disimpan
- Hanya prefix yang ditampilkan ke user (contoh: `hk_abc123...`)
- Full key hanya ditampilkan sekali saat pembuatan
- Support key expiration dan revocation

### Authentication
- JWT tokens untuk web session
- API key untuk programmatic access
- Bcrypt untuk password hashing
- Rate limiting per API key

### Rate Limiting
- Default: 100 requests per menit per API key
- Configurable per plan
- Custom limits untuk enterprise

## Monitoring

### Prometheus Metrics
- Request count per network
- Response time histogram
- Error rate counter
- Cache hit/miss ratio
- Active connections

### Grafana Dashboards
- System overview
- API performance
- Node health
- Usage analytics

## Cara Menjalankan

```bash
# Install dependencies
pip install -r requirements.txt

# Setup database
alembic upgrade head

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8003

# Akses
# Web: http://localhost:8003
# API: http://localhost:8003/api/v1/
# Docs: http://localhost:8003/docs
# Health: http://localhost:8003/api/v1/status
```

## Perbedaan dengan Konektivitas.com

| Aspek | Konektivitas.com | Hub.konektivitas.com |
|-------|------------------|---------------------|
| Database | SQLite → PostgreSQL | PostgreSQL |
| Auth | Tidak ada | JWT + API Keys |
| Rate Limit | Per-IP | Per-API-Key |
| Container | Tidak ada | Docker |
| Monitoring | Prometheus headers | Prometheus + Grafana |
| Purpose | Internet tools | Blockchain RPC |
| Port | 8002 | 8003 |

---

## Referensi Penting

- [BRIEF.md](BRIEF.md) — Visi, misi, dan filosofi Konektivitas.com
- [BRIEF2.md](BRIEF2.md) — Detail teknis dan arsitektur Konektivitas.com
- [ROADMAP.md](ROADMAP.md) — Roadmap pengembangan 5 tahun
- [FEATURES.md](FEATURES.md) — Daftar lengkap fitur per fase
- [plans/hub-konektivitas-plan.md](plans/hub-konektivitas-plan.md) — Rencana detail Hub.konektivitas.com

---

> "Kami tidak membuat aplikasi yang viral. Kami membangun utilitas yang akan tetap dibutuhkan selama internet masih ada."
