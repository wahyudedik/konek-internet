# Agent Guide - Konektivitas.com

> Panduan untuk AI/agent agar mudah memahami dan mengerjakan proyek Konektivitas.com.

## Overview

Internet menjadi fondasi hampir semua layanan digital. Website, aplikasi mobile, AI, IoT, sistem perusahaan, hingga perangkat pintar bergantung pada infrastruktur internet untuk beroperasi.

Namun, mengelola infrastruktur tersebut masih tersebar di banyak layanan dan sering kali rumit.

**Konektivitas hadir untuk menyederhanakan cara orang memahami, mengelola, dan mengembangkan aset internet mereka.**

> **"Konektivitas.com adalah platform Utility & Digital Infrastructure yang membantu manusia dan aplikasi menemukan, memahami, mengelola, memantau, dan terhubung dengan hal-hal yang berguna di internet."**

**Tagline:** "Memahami. Mengelola. Mengembangkan Internet."

## Visi

> **"Make the useful internet searchable."**

Atau versi yang lebih luas:

> **"Konektivitas.com adalah platform Utility & Digital Infrastructure yang membantu manusia dan aplikasi menemukan, memahami, mengelola, memantau, dan terhubung dengan hal-hal yang berguna di internet."**

### Misi

1. Menyederhanakan pengelolaan infrastruktur internet.
2. Menyediakan monitoring yang mudah dipahami.
3. Memberikan edukasi internet dalam bahasa Indonesia.
4. Membantu pengguna mengambil keputusan berdasarkan data.
5. Menjadi pusat kendali aset internet.
6. Mengindeks hal-hal yang berguna di internet (Utility Index).

### Positioning

**Bukan:**

- Google clone
- Domain Registrar
- Hosting Provider
- Cloud Provider
- Blockchain Provider
- Business Directory

**Tetapi:** Platform Utility & Digital Infrastructure.

### Pertanyaan Penuntun

Setiap fitur baru harus menjawab setidaknya satu dari empat pertanyaan berikut:

1. **"Apakah fitur ini membantu pengguna memahami internet?"** *(Learn)*
2. **"Apakah fitur ini membantu pengguna mengelola aset internetnya?"** *(Manage)*
3. **"Apakah fitur ini membantu pengguna menemukan sesuatu yang berguna?"** *(Discover)*
4. **"Apakah fitur ini membantu menghubungkan aplikasi dan infrastruktur?"** *(Connect)*

Kalau jawabannya "ya", berarti fitur tersebut sejalan dengan visi Konektivitas. Kalau tidak, lebih baik ditunda agar produk tetap fokus.

---

## 4 Pilar Produk

> Konektivitas adalah **satu platform modular**. Tidak ada subdomain terpisah. Setiap fitur adalah modul dalam satu platform.

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

**Implementasi:** Utility Search Engine + Business Intelligence

- Utility Index (Jobs, Tools, APIs, Suppliers, Products, Courses, Opportunities)
- Full-Text Search + UtilityRank
- Crawler Pipeline (Discovery → Crawl → Extract → Normalize → Index → Search)
- Business Intelligence & Market Analysis
- Custom Reports

**Target Pengguna:** Job seeker, Freelancer, Business Owner, Konsultan, Marketing

### 4. Connect — Menghubungkan infrastruktur

**Implementasi:** Developer Platform + Blockchain Infrastructure

- Utility Search API
- Blockchain RPC API (JSON-RPC, WebSocket)
- Multi-chain support (Ethereum, Polygon, BSC, Arbitrum, dll)
- API Key System & Dashboard
- Dynamic DNS API

**Target Pengguna:** Developer blockchain, Startup Web3, AI Agent, IoT

---

## Target Pengguna

### 🌐 Public — Belajar, Mengecek, Mencari referensi

Pelajar, Mahasiswa, Freelancer, Developer pemula, Ide startup, Job seeker

### 💼 Professional — Monitoring, Workspace, Manajemen aset

Developer, DevOps, IT Support, SysAdmin, Network Engineer, Agency, Software House

### 🏢 Business — Insight, Peluang, Analisis

UMKM, Startup, Business Owner, Enterprise, Konsultan, Procurement

### 🔗 Technology — Blockchain, AI, IoT

Developer blockchain, Startup Web3, AI Agent, Wallet/Exchange, Game Blockchain

---

## Struktur Proyek

```
konek-internet/
├── BRIEF.md              # Master Brief (visi, misi, filosofi terpadu)
├── BRIEF2.md             # Detail teknis & arsitektur
├── BRIEF3.md             # Brief Utility Search Engine
├── BRIEF4.md             # Tech stack Utility Search Engine
├── ROADMAP.md            # Roadmap terintegrasi 5 tahun (2026-2031)
├── FEATURES.md           # Daftar lengkap fitur per fase (4 pilar)
├── AGENT.md              # Dokumen ini
├── requirements.txt      # Python dependencies
├── .env.example          # Contoh environment variables
├── .venv/                # Virtual environment
├── deploy.sh             # Script deployment awal (setup VPS)
├── update.sh             # Script update produksi (migration, cache clear)
├── konektivitas.db       # SQLite database (development)
├── plans/                # Rencana detail per modul
│   ├── hub-konektivitas-plan.md
│   ├── full-implementation-plan.md
│   └── ...
└── app/
    ├── __init__.py
    ├── main.py           # FastAPI app + middleware
    ├── config.py         # Konfigurasi (Pydantic Settings)
    ├── database.py       # Database session & init (SQLAlchemy async)
    ├── dependencies.py   # Auth dependencies (get_current_user, require_plan)
    ├── routers/          # API endpoints
    │   ├── dns.py        # 8 endpoints: lookup, reverse, mx, txt, cname, spf, dmarc, propagation
    │   ├── domain.py     # 2 endpoints: whois, expiry
    │   ├── ssl.py        # 2 endpoints: ssl check, expiry
    │   ├── website.py    # 5 endpoints: ping, http-status, redirect, headers, ua
    │   ├── ip.py         # 5 endpoints: ip lookup, asn, blacklist, my-ip, port, email
    │   ├── cdn.py        # 1 endpoint: cdn detect
    │   ├── batch.py      # Batch lookup endpoints
    │   ├── compare.py    # Comparison endpoints
    │   ├── auth.py       # 6 endpoints: register, login, refresh, me, update, change-password
    │   ├── workspace.py  # 10 endpoints: domains CRUD, check-*, history, dashboard
    │   ├── ddns.py       # Dynamic DNS endpoints
    │   ├── keys.py       # API Key management endpoints
    │   └── notifications.py # Notification settings endpoints
    ├── services/         # Business logic
    │   ├── dns_service.py
    │   ├── whois_service.py
    │   ├── ip_service.py
    │   ├── ssl_service.py
    │   ├── website_service.py
    │   ├── ua_service.py
    │   ├── email_service.py
    │   ├── port_service.py
    │   ├── cdn_service.py
    │   ├── traceroute_service.py
    │   ├── tech_detector_service.py
    │   ├── speed_test_service.py
    │   ├── dns_history_service.py
    │   ├── ssl_history_service.py
    │   ├── auth_service.py
    │   ├── workspace_service.py
    │   ├── monitoring_service.py
    │   ├── notification_service.py
    │   ├── api_key_service.py
    │   ├── api_dashboard_service.py
    │   └── ddns_service.py
    ├── models/           # SQLAlchemy ORM models
    │   ├── base.py       # Base + TimestampMixin
    │   ├── user.py       # User model (email, username, password_hash, plan)
    │   ├── monitored_domain.py  # MonitoredDomain (user's workspace domains)
    │   ├── ssl_history.py       # DomainSslHistory
    │   ├── dns_history.py       # DomainDnsHistory
    │   ├── uptime_check.py      # UptimeCheck + UptimeLog
    │   ├── notification.py      # NotificationSetting (email, telegram, discord)
    │   ├── api_key.py           # ApiKey (kn_ prefix)
    │   └── ddns.py             # DynamicDns records
    ├── scheduler/        # Background job scheduler
    │   └── jobs.py       # MonitoringScheduler (auto-check SSL, DNS, uptime)
    ├── utils/
    │   ├── cache.py      # Redis + in-memory fallback cache
    │   ├── rate_limit.py # Per-IP rate limiting (60 req/min)
    │   ├── validators.py # Input validation (domain, IP, URL, host)
    │   └── security.py   # JWT tokens, API key hashing (bcrypt)
    ├── templates/        # Jinja2 HTML templates
    │   ├── base.html     # Base layout (navbar, footer, JSON-LD)
    │   ├── index.html    # Homepage (tools grid)
    │   ├── dashboard.html # Dashboard homepage
    │   ├── 404.html      # Custom 404 page
    │   ├── about.html    # About page
    │   ├── api_docs.html # API Documentation page
    │   ├── partials/
    │   │   ├── education.html
    │   │   ├── breadcrumb.html
    │   │   └── dashboard_sidebar.html  # Reusable sidebar partial
    │   ├── dashboard/    # Dashboard pages (auth required)
    │   │   ├── login.html
    │   │   ├── register.html
    │   │   ├── domains.html
    │   │   ├── domain_detail.html
    │   │   ├── api_keys.html
    │   │   ├── notifications.html
    │   │   ├── ddns.html
    │   │   └── profile.html
    │   └── tools/        # Tool pages (dengan section edukasi)
    ├── data/
    │   ├── education.py  # Konten edukasi tools
    │   └── faq_data.py   # FAQ JSON-LD
    └── static/
        ├── favicon.png
        ├── logo.png
        ├── robots.txt
        ├── sitemap.xml
        ├── manifest.json
        ├── sw.js
        ├── css/style.css # Responsive CSS (65+ variables, dark mode, dashboard layout)
        └── js/app.js     # Frontend JavaScript
```

### Struktur Future (Utility Search Engine + Blockchain)

```
konek-internet/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── crawler/              # Utility Search Crawler
│   │   ├── base.py
│   │   ├── discovery.py
│   │   ├── jobs.py
│   │   ├── tools.py
│   │   ├── apis.py
│   │   └── robots.py
│   ├── parser/
│   │   ├── html_parser.py
│   │   ├── content_extractor.py
│   │   └── dynamic_parser.py
│   ├── processor/
│   │   ├── normalizer.py
│   │   ├── deduplicator.py
│   │   ├── validator.py
│   │   └── entity_detector.py
│   ├── search/
│   │   ├── engine.py        # PostgreSQL FTS + pg_trgm
│   │   ├── ranking.py       # UtilityRank
│   │   └── query_parser.py
│   ├── scheduler/
│   │   └── jobs.py          # APScheduler / Celery tasks
│   ├── blockchain/          # Blockchain Infrastructure
│   │   ├── rpc_proxy.py
│   │   ├── websocket_proxy.py
│   │   ├── data_api.py
│   │   └── monitoring.py
│   ├── middleware/
│   │   ├── auth.py          # API Key + JWT auth
│   │   ├── rate_limit.py    # Per-IP + Per-API-Key
│   │   └── logging.py
│   ├── routers/
│   ├── services/
│   ├── models/
│   ├── utils/
│   ├── templates/
│   └── static/
├── alembic/                  # Database migrations
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Arsitektur Teknis

### Stack (2026)
- **Server:** Ubuntu + AAPanel
- **Web Server:** Nginx
- **Backend:** Python FastAPI
- **Cache:** Redis
- **Database:** SQLite → PostgreSQL (2027)

### Alur Request — Public Tools
```
Internet → Cloudflare → AAPanel → Nginx → FastAPI → Redis → External APIs
```

### Alur Request — Utility Search
```
Internet → Nginx → FastAPI → PostgreSQL (FTS+pg_trgm) → Response
                                    ↑
                            Crawler → Parser → Processor → Index
```

### Alur Request — Blockchain RPC
```
Client → Nginx → FastAPI → Auth → Rate Limit → Cache (Redis) → Blockchain Node
                                              → Log (PostgreSQL)
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

**Framework 1 — Arah Produk (4 Pertanyaan Pilar):**

Apakah fitur ini membantu pengguna memahami internet *(Learn)*, mengelola aset internetnya *(Manage)*, menemukan sesuatu yang berguna *(Discover)*, atau menghubungkan infrastruktur *(Connect)*? Kalau tidak menjawab salah satunya, tolak.

**Framework 2 — Kelayakan Teknis (3 Syarat):**

1. Ringan dijalankan (sesuai spesifikasi server)
2. Berguna untuk banyak orang
3. Masih relevan 10 tahun ke depan

> Fitur harus lolos **kedua** framework sebelum diimplementasikan.

### Yang TIDAK Perlu
- Docker (di awal, untuk public tools)
- Kubernetes
- Microservice (di awal)
- Elasticsearch (gunakan PostgreSQL FTS dulu)
- RabbitMQ
- AI API (untuk MVP — rule-based dulu)
- OpenSearch (ketika data belum jutaan)

---

## Status Implementasi

### Fase 1 — Public Tools MVP (2026) ✅ SELESAI

#### Public Tools
- 30 tools aktif (DNS, Domain, SSL, Website, IP + 5 baru: Traceroute, Tech Detector, Speed Test, DNS History, SSL History)
- 36+ API endpoints aktif (+ DDNS, API Dashboard)
- 30 halaman frontend + About page + API Docs page
- 14 service files (dns, whois, ssl, ip, website, ua, email, port, cdn, traceroute, tech_detector, speed_test, dns_history, ssl_history)
- 13 router files (dns, domain, ssl, website, ip, cdn, tools_v2, ddns, auth, workspace, keys, notifications)

#### Core Infrastructure
- Redis caching + in-memory fallback
- Rate limiting (60 req/min per IP)
- Security headers middleware
- Input validation di semua endpoints
- Async non-blocking di semua services (asyncio.to_thread)

#### Database & Auth
- SQLAlchemy 2.0 async ORM (mapped_column / Mapped type annotations)
- JWT Authentication (python-jose) + bcrypt password hashing
- User model (email, username, password_hash, plan)
- 8 ORM models (User, MonitoredDomain, DomainSslHistory, DomainDnsHistory, UptimeCheck, UptimeLog, NotificationSetting, ApiKey, DynamicDns)
- API Key system (kn_ prefix, bcrypt hashing)
- Auth dependencies (get_current_user, require_plan, get_optional_user)
- Dashboard auth redirect (unauthenticated → /login)
- Header auth link (Login/Dashboard dynamic berdasarkan auth state)

#### Dashboard & Workspace
- Dashboard sidebar partial (DRY, reusable across 7 pages via {% include %})
- Dashboard mobile responsive (slide-in sidebar + overlay backdrop)
- Workspace domain management (CRUD)
- Monitoring scheduler (auto-check SSL, DNS, uptime)
- Notification system (Email, Telegram, Discord)

#### Deployment Infrastructure
- Deploy script (deploy.sh — initial VPS setup: Python, Nginx, Supervisor, Gunicorn)
- Update script (update.sh — migration, cache clear, log rotation, graceful reload)

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
- Footer grid dengan semua 30 tools terorganisir + About + API Docs
- Search/filter tools di homepage
- Back-to-top button
- 404 page dengan tool suggestions
- CSS consolidation (350+ lines removed dari dashboard pages ke global style.css)

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

# Deployment (VPS)
# bash deploy.sh    # Initial setup: Python, Nginx, Supervisor, Gunicorn
# bash update.sh    # Update produksi: migration, cache clear, log rotation
```

### Cara Menjalankan (Future — Utility Search + Blockchain)
```bash
# Setup database
alembic upgrade head

# Start crawler scheduler
python -m app.scheduler.jobs

# Start server (integrated)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8002

# Akses
# Web: http://localhost:8002
# Tools: http://localhost:8002/dns-lookup
# Search: http://localhost:8002/search
# Blockchain: http://localhost:8002/rpc/{network}
# API: http://localhost:8002/api/v1/
# Docs: http://localhost:8002/docs
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
/search              # Utility Search (future)
/rpc/{network}       # Blockchain RPC (future)
/about
/api-docs
```

### API Pattern
```
# Public Tools (Fase 1 — aktif)
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

# Utility Search (Future)
GET /api/v1/search?intent=work&category=jobs&skill=python
GET /api/v1/jobs?skill=python&remote=true&status=active
GET /api/v1/tools?category=calculator&pricing=free
GET /api/v1/apis?category=payment&status=online
GET /api/v1/suppliers?category=network_equipment&location=indonesia

# Blockchain RPC (Future)
POST   /rpc/{network}             # JSON-RPC proxy
GET    /rpc/{network}/health      # Node health check
GET    /api/v1/networks           # List supported networks
GET    /api/v1/{network}/block/{id}
GET    /api/v1/{network}/tx/{hash}
GET    /api/v1/{network}/address/{addr}
GET    /api/v1/{network}/balance/{addr}
POST   /api/v1/{network}/broadcast

# Authentication (Future)
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me

# API Keys (Future)
GET    /api/v1/keys
POST   /api/v1/keys
DELETE /api/v1/keys/{id}
PUT    /api/v1/keys/{id}
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

### API Key Prefix
- `kn_` — Konektivitas.com unified API keys (tools, search, blockchain)

---

## Roadmap (Ringkasan)

### Fase 1 — Foundation (2026) ✅ SELESAI
- 30 Public Tools (DNS, Domain, SSL, Website, IP + Traceroute, Tech Detector, Speed Test, DNS History, SSL History)
- 36+ API endpoints (RESTful, rate limit 60 req/min)
- User Authentication & Workspace (JWT)
- API Key System (kn_ prefix) & Dashboard
- Dynamic DNS (token-based)
- Notification System (Email, Telegram, Discord)
- 30 tool pages + 6 dashboard pages
- Target: 100.000 visitor/bulan

### Fase 2 — Developer Platform, Workspace & Utility Search MVP (2027)
- Utility Search Engine: Core Engine + Jobs Vertical
- PostgreSQL FTS + pg_trgm
- Crawler Pipeline (Discovery → Crawl → Extract → Normalize → Index → Search)
- Target: 500.000 visitor/bulan, 100 premium subscribers
- Utility Search Engine: Core Engine + Jobs Vertical
- Target: 500.000 visitor/bulan, 100 premium subscribers

### Fase 3 — Infrastructure, Multi-Vertical, Blockchain & Mobile (2028)
- Total 40+ tools
- Team Workspace & Shared Monitoring
- DNS Hosting & DNS Anycast (bertahap)
- Status Page
- Utility Search: Multi-Vertical (Tools, APIs, Suppliers, Products)
- Utility Search: B2B Intelligence
- Blockchain RPC: Ethereum + 5 chains, Load Balancer, WebSocket
- Mobile App (Android)
- Target: 1 juta visitor/bulan, 1.000 premium subscribers

### Fase 4 — Business Intelligence, Enterprise & Ecosystem (2029)
- Total 50+ tools
- Enterprise features (SSO, Audit Log, SLA)
- BI: Market Analysis, Technology Detection, Opportunity Finder
- GeoIP & ASN Database
- Utility Search: Semantic Search, AI Classification, Developer Marketplace
- Blockchain: Enterprise features, Analytics, Billing
- Target: 3 juta visitor/bulan, 50 enterprise clients

### Fase 5 — Internet Platform (2030-2031)
- 100+ tools
- Public DNS (dns.konektivitas.com)
- Internet Intelligence (BGP, IXP, Latency Map)
- Utility Search: 100+ vertical categories, Global coverage
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
3. Tanyakan: "Apakah fitur ini membantu pengguna **memahami** *(Learn)*, **mengelola** *(Manage)*, **menemukan** *(Discover)*, atau **menghubungkan** *(Connect)*?"
4. Pastikan fitur memenuhi 3 syarat: **ringan**, **bermanfaat**, **tahan lama**
5. Ikuti konvensi penamaan yang sudah ada
6. Pastikan response time < 1 detik
7. Test dengan data sampel sebelum commit

### Struktur Code yang Diharapkan
```
app/
├── main.py           # FastAPI app + middleware (Security, RateLimit)
├── config.py         # Pydantic settings
├── routers/          # API endpoints
│   ├── dns.py        # DNS: lookup, reverse, mx, txt, cname, spf, dmarc, propagation
│   ├── domain.py     # Domain: whois, expiry
│   ├── ssl.py        # SSL: check, expiry
│   ├── website.py    # Website: ping, http-status, redirect, headers, ua
│   ├── ip.py         # IP: lookup, asn, blacklist, my-ip, port, email
│   ├── cdn.py        # CDN: detect
│   ├── search.py     # Search: universal search (future)
│   ├── jobs.py       # Jobs API (future)
│   ├── rpc.py        # Blockchain RPC proxy (future)
│   ├── auth.py       # Authentication (future)
│   └── keys.py       # API Key management (future)
├── services/         # Business logic (dengan @cached decorator)
│   ├── dns_service.py
│   ├── whois_service.py
│   ├── ip_service.py
│   ├── ssl_service.py
│   ├── website_service.py
│   ├── ua_service.py
│   ├── email_service.py
│   ├── port_service.py
│   ├── cdn_service.py
│   ├── search_service.py    # (future)
│   ├── crawl_service.py     # (future)
│   ├── rpc_service.py       # (future)
│   ├── auth_service.py      # (future)
│   └── api_key_service.py   # (future)
├── crawler/          # Utility Search Crawler (future)
│   ├── base.py
│   ├── discovery.py
│   ├── jobs.py
│   └── robots.py
├── search/           # Search Engine (future)
│   ├── engine.py     # PostgreSQL FTS + pg_trgm
│   ├── ranking.py    # UtilityRank
│   └── query_parser.py
├── processor/        # Data Processing (future)
│   ├── normalizer.py
│   ├── deduplicator.py
│   ├── validator.py
│   └── entity_detector.py
├── scheduler/        # Background Jobs (future)
│   └── jobs.py       # APScheduler / Celery
├── middleware/        # (future)
│   ├── auth.py       # API Key + JWT
│   ├── rate_limit.py
│   └── logging.py
├── utils/
│   ├── cache.py      # Redis + in-memory cache
│   ├── rate_limit.py # Per-IP rate limiting
│   ├── validators.py # Input validation (domain, IP, URL, host)
│   └── crypto.py     # API key hashing, JWT (future)
├── templates/        # Jinja2 HTML
│   ├── base.html     # Base layout + JSON-LD
│   ├── index.html    # Homepage
│   ├── 404.html      # Error page
│   ├── about.html    # About page
│   ├── api_docs.html # API Documentation
│   ├── search.html   # Search homepage (future)
│   ├── results.html  # Search results (future)
│   ├── partials/
│   │   ├── education.html
│   │   └── breadcrumb.html
│   └── tools/        # Tool pages
├── data/
│   ├── education.py  # Konten edukasi tools
│   └── faq_data.py   # FAQ JSON-LD
├── static/
│   ├── css/style.css
│   ├── js/app.js
│   ├── favicon.png
│   ├── logo.png
│   ├── manifest.json # PWA
│   └── sw.js         # Service Worker
└── models/           # Data models (Pydantic + SQLAlchemy future)
```

### Naming Convention
- **File:** snake_case.py
- **Function:** snake_case()
- **Class:** PascalCase
- **Variable:** snake_case
- **Constant:** UPPER_SNAKE_CASE
- **API Endpoint:** kebab-case (/dns-lookup)
- **API Key Prefix:** `kn_` (unified)

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
- [x] Dashboard sidebar partial (DRY, reusable across 7 pages)
- [x] Dashboard mobile responsive (slide-in sidebar + overlay)
- [x] Dashboard auth redirect (unauthenticated → /login)
- [x] Header auth link (Login/Dashboard dynamic)
- [x] CSS consolidation (350+ lines removed from dashboard pages)
- [x] Deploy script (deploy.sh — initial server setup)
- [x] Update script (update.sh — migration, cache clear, log rotation)

---

## Target Metrics

### Year 1 (2026) — Foundation ✅ SELESAI

| Metric | Target | Status |
|--------|--------|--------|
| Visitor/bulan | 100.000 | 🔄 |
| Tools | 30 | ✅ |
| API request/hari | 10.000 | 🔄 |

### Year 2 (2027) — Developer Platform, Workspace & Search MVP

| Metric | Target |
|--------|--------|
| Visitor/bulan | 500.000 |
| Registered users | 10.000 |
| Pro subscribers | 100 |
| Domain monitored | 5.000 |
| Indexed jobs | 10.000+ |

### Year 3 (2028) — Infrastructure, Multi-Vertical, Blockchain & Mobile

| Metric | Target |
|--------|--------|
| Visitor/bulan | 1.000.000 |
| Registered users | 50.000 |
| Pro subscribers | 1.000 |
| Mobile app installs | 10.000 |
| Indexed objects | 100.000+ |
| Active verticals | 4+ |
| Blockchain users | 1.000 |

### Year 4 (2029) — Business Intelligence, Enterprise & Ecosystem

| Metric | Target |
|--------|--------|
| Visitor/bulan | 3.000.000 |
| Registered users | 100.000 |
| Enterprise clients | 50 |
| API request/hari | 1.000.000 |
| Indexed objects | 1.000.000+ |
| B2B clients | 20 |

### Year 5 (2030-2031) — Internet Platform

| Metric | Target |
|--------|--------|
| Visitor/bulan | 5.000.000 |
| Registered users | 500.000 |
| Pro subscribers | 20.000 |
| Enterprise clients | 500 |
| Public DNS users | 1.000.000 |
| API request/hari | 10.000.000 |
| Indexed objects | 100.000.000+ |
| Search daily visitors | 500.000 |
| Blockchain users | 20.000 |

---

## Monetisasi

### Free
- Public tools (25+ → 100+ tools)
- Edukasi internet
- Public search & discovery
- API dengan rate limit

### Pro (Rp 49.000/bulan)
- Workspace (Domain, SSL, DNS, Server, Email Monitoring)
- Notification (Email, Telegram, Discord)
- Laporan & Export
- Saved searches & alerts
- Advanced filtering
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
- **Discovery** — Menemukan hal-hal berguna di internet
- **Insight** — Data untuk pengambilan keputusan
- **Efisiensi** — Satu tempat untuk semua aset internet
- **Produktivitas** — Mengelola aset internet lebih cepat
- **Konektivitas** — Menghubungkan aplikasi dengan infrastruktur
- **Kepercayaan** — Platform yang bisa diandalkan

---

## Referensi

- [BRIEF.md](BRIEF.md) — Master Brief (visi, misi, filosofi terpadu)
- [BRIEF2.md](BRIEF2.md) — Detail teknis dan arsitektur
- [BRIEF3.md](BRIEF3.md) — Brief Utility Search Engine
- [BRIEF4.md](BRIEF4.md) — Tech stack Utility Search Engine
- [ROADMAP.md](ROADMAP.md) — Roadmap terintegrasi 5 tahun
- [FEATURES.md](FEATURES.md) — Daftar lengkap fitur per fase (4 pilar)
- [plans/hub-konektivitas-plan.md](plans/hub-konektivitas-plan.md) — Rencana detail blockchain infrastructure

---

> "Kami tidak membuat aplikasi yang viral. Kami membangun utilitas yang akan tetap dibutuhkan selama internet masih ada."
