# Fitur Konektivitas.com

> Daftar lengkap fitur per fase implementasi, terstruktur berdasarkan 3 pilar produk: **Learn**, **Manage**, **Discover**.

---

## Pilar 1: Learn — Memahami Internet

> **Implementasi:** Public Tools (gratis). Tujuan: edukasi, traffic, dan SEO.

### Fase 1 — MVP (2026) ✅ SELESAI

#### Core Features

- **25 Tools DNS, Domain, SSL, Website, IP** — Utilitas internet lengkap (+CDN Detection)
- **25+ API Endpoints** — RESTful API gratis dengan rate limit 60 req/min
- **25 Tool Pages** — Halaman frontend dengan form interaktif dan hasil real-time
- **Redis + In-memory Cache** — Performa optimal dengan fallback cache
- **Rate Limiting** — Per-IP rate limiting (60 req/menit)
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, X-XSS-Protection

#### SEO & Performance

- **JSON-LD Structured Data** — FAQPage schema untuk rich snippets
- **Meta Tags** — Title, description, Open Graph, canonical URL
- **robots.txt & sitemap.xml** — SEO crawling optimization
- **Response Time Display** — X-Process-Time header di setiap response
- **Fast Loading** — < 1 detik response time

#### User Experience

- **Dark Mode Toggle** — Light/dark theme dengan localStorage persistence
- **Mobile Responsive** — Hamburger nav, stacked forms, card layout di mobile
- **Tool History** — Riwayat 10 query terakhir per tool (localStorage)
- **URL Query State** — Shareable URLs dengan query parameters
- **Keyboard Shortcuts** — Ctrl+K search, Escape close menus, Ctrl+D toggle dark mode
- **Keyboard Navigation** — Arrow keys navigate between tool cards (WCAG)
- **PWA Support** — Installable sebagai Progressive Web App
- **Breadcrumb Navigation** — Navigasi kategori yang clickable
- **Education Section** — Konten edukasi interaktif di semua tool pages
- **Search/Filter** — Cari dan filter tools di homepage
- **Tool Page Preloading** — Prefetch on hover untuk navigasi cepat
- **Dark Mode System Sync** — Auto-sync dengan system preference (matchMedia listener)

#### 25 Tools (per Kategori)

##### DNS (9 Tools)

| Tool | Endpoint | Page | Description |
|------|----------|------|-------------|
| DNS Lookup | `GET /api/v1/dns/{domain}` | `/dns-lookup` | Cek DNS record (A, AAAA, MX, TXT, dll) |
| Reverse DNS | `GET /api/v1/dns/{domain}/reverse` | `/reverse-dns` | Reverse lookup PTR record |
| DNS Propagation | `GET /api/v1/dns/{domain}/propagation` | `/dns-propagation` | Cek propagasi DNS global |
| MX Lookup | `GET /api/v1/dns/{domain}/mx` | `/mx-lookup` | Cek mail exchange record |
| TXT Lookup | `GET /api/v1/dns/{domain}/txt` | `/txt-lookup` | Cek TXT record |
| CNAME Lookup | `GET /api/v1/dns/{domain}/cname` | `/cname-lookup` | Cek canonical name record |
| SPF Checker | `GET /api/v1/dns/{domain}/spf` | `/spf-checker` | Validasi SPF record |
| DMARC Checker | `GET /api/v1/dns/{domain}/dmarc` | `/dmarc-checker` | Validasi DMARC record |
| NS Lookup | `GET /api/v1/dns/{domain}?record_type=NS` | `/ns-lookup` | Cek name server |

##### Domain (2 Tools)

| Tool | Endpoint | Page | Description |
|------|----------|------|-------------|
| WHOIS Lookup | `GET /api/v1/whois/{domain}` | `/whois-lookup` | Info registrasi domain |
| Domain Expiry | `GET /api/v1/domain/{domain}/expiry` | `/domain-expiry` | Cek masa aktif domain |

##### SSL (2 Tools)

| Tool | Endpoint | Page | Description |
|------|----------|------|-------------|
| SSL Checker | `GET /api/v1/ssl/{domain}` | `/ssl-checker` | Cek SSL certificate |
| SSL Expiry | `GET /api/v1/ssl/{domain}/expiry` | `/ssl-expiry` | Cek expiry SSL certificate |

##### Website (6 Tools)

| Tool | Endpoint | Page | Description |
|------|----------|------|-------------|
| Ping Checker | `GET /api/v1/ping/{host}` | `/ping-checker` | Cek host aktif |
| HTTP Status | `GET /api/v1/http-status/{url}` | `/http-status` | Cek HTTP response code |
| Redirect Checker | `GET /api/v1/redirect/{url}` | `/redirect-checker` | Trace redirect chain |
| Header Checker | `GET /api/v1/headers/{url}` | `/header-checker` | Cek HTTP headers + version |
| User-Agent Checker | `GET /api/v1/ua` | `/ua-checker` | Deteksi browser & device |
| CDN Detection | `GET /api/v1/cdn/{domain}/detect` | `/cdn-detect` | Deteksi provider CDN |

##### IP (6 Tools)

| Tool | Endpoint | Page | Description |
|------|----------|------|-------------|
| IP Lookup | `GET /api/v1/ip/{ip}` | `/ip-lookup` | Info lengkap IP address |
| ASN Lookup | `GET /api/v1/ip/{ip}/asn` | `/asn-lookup` | Cek ASN & ISP |
| Blacklist Checker | `GET /api/v1/ip/{ip}/blacklist` | `/blacklist-checker` | Cek IP blacklist |
| My IP | `GET /api/v1/ip/me` | `/my-ip` | Deteksi IP Anda |
| Email Validator | `GET /api/v1/email/{email}/validate` | `/email-validator` | Validasi email address |
| Port Scanner | `GET /api/v1/port/{host}` | `/port-scanner` | Scan port terbuka |

##### Additional Pages

| Page | URL | Description |
|------|-----|-------------|
| Homepage | `/` | Grid 25 tools dengan search/filter |
| About | `/about` | Visi, misi, filosofi, tech stack |
| API Docs | `/api-docs` | Dokumentasi API lengkap |
| 404 | `/404` | Custom error page dengan tool suggestions |

#### Security Features

- **Input Validation** — Semua input divalidasi sebelum diproses
- **XSS Protection** — HTML escaping + CSP headers + JavaScript Map
- **Rate Limiting** — 60 requests per minute per IP
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- **Request ID** — X-Request-ID header untuk tracing (uuid, 8 char)
- **HTTPS Only** — HSTS header untuk production
- **No Data Storage** — Tidak menyimpan data pribadi pengguna

#### Accessibility (WCAG 2.1)

- **Touch-Friendly Targets** — Minimum 44px tap targets (WCAG 2.5.5)
- **Focus Visible** — Keyboard focus indicators untuk semua interactive elements
- **ARIA Labels** — Search box dan navigation dengan aria-label
- **Keyboard Navigation** — Arrow keys untuk tool cards, Tab untuk form elements

#### Responsive Design

- **Mobile (< 768px)** — Single column, hamburger nav, stacked forms
- **Tablet (768px - 1024px)** — 2-column grid, optimized layout
- **Desktop (> 1024px)** — Full grid layout, horizontal nav
- **Small Mobile (< 480px)** — Card layout untuk result tables

#### Performance Optimizations

- **HTTP Client Reuse** — Shared httpx.AsyncClient dengan connection pooling
- **Cache TTL Tuning** — Optimized berdasarkan data volatility
  - Blacklist: 10 menit (sering berubah)
  - CDN Detection: 1 jam (jarang berubah)
  - DNS/Website: 1-5 menit (real-time)
- **Tool Page Preloading** — Prefetch on hover

---

### Fase 2 — Public Tools Enhancement (2027)

#### Planned Tools (total 30)

| Tool | Category | Description |
|------|----------|-------------|
| Traceroute | Website | Trace route ke server |
| DNS History | DNS | History DNS record |
| SSL History | SSL | History SSL certificate |
| Technology Detector | Website | Deteksi teknologi website |
| Website Speed Test | Website | Test kecepatan website |

#### Enhancements

- Multi-language support (ID/EN)
- Batch lookup (cek banyak domain sekaligus)
- Tool comparison (bandingkan hasil 2 domain)
- Share results (share via link/social media)
- API v2 dengan fitur baru

---

### Fase 3 — Public Tools Advanced (2028)

#### Planned Tools (total 40+)

| Tool | Category | Description |
|------|----------|-------------|
| DNS Security Analyzer | DNS | Analisis keamanan DNS |
| SSL Grade | SSL | Grading SSL configuration |
| Server Location | IP | Peta lokasi server |
| Email Deliverability | Email | Cek kemampuan kirim email |
| Website Accessibility | Website | Cek aksesibilitas website |
| DNSSEC Checker | DNS | Validasi DNSSEC |
| HTTP/3 Checker | Website | Deteksi HTTP/3 support |
| Security Headers Analyzer | Website | Analisis security headers lengkap |

#### Enhancements

- Advanced analytics per tool
- Historical data visualization
- Export results (PDF, CSV)
- API v2 dengan advanced features

---

## Pilar 2: Manage — Mengelola Aset Internet

> **Implementasi:** Workspace (Pro & Team). Tujuan: monitoring, kolaborasi, dan produktivitas.

### Fase 2 — Workspace MVP (2027)

#### Authentication

- **User Registration** — Email, Google OAuth
- **Login System** — Email + password
- **Email Verification** — Verifikasi email
- **Password Reset** — Lupa password
- **Profile Management** — Edit profil

#### Domain Management

- **Add Domain** — Tambah domain ke workspace
- **Domain List** — Daftar semua domain
- **Domain Details** — Info detail domain
- **Domain Notes** — Catatan per domain
- **Bulk Import** — Import banyak domain sekaligus

#### SSL Monitoring

- **SSL Status** — Status SSL real-time
- **SSL History** — History perubahan SSL
- **Expiry Alert** — Alert saat SSL < 30 hari
- **SSL Recommendations** — Saran perbaikan SSL

#### DNS Monitoring

- **DNS Records** — Lihat semua DNS record
- **DNS History** — History perubahan DNS
- **Change Alert** — Alert saat DNS berubah
- **DNS Comparison** — Bandingkan DNS 2 domain

#### Uptime Monitoring

- **Uptime Check** — Cek uptime setiap 5 menit
- **Response Time** — Monitor response time
- **Uptime History** — History uptime
- **Downtime Alert** — Alert saat website down

#### Notification System

- **Email Notification** — Notifikasi via email
- **Telegram Bot** — Notifikasi via Telegram
- **Discord Webhook** — Notifikasi via Discord
- **Custom Webhook** — Notifikasi via webhook
- **Notification Settings** — Pengaturan notifikasi

#### Dashboard

- **Overview** — Ringkasan semua aset
- **Health Score** — Skor kesehatan aset
- **Recent Activity** — Aktivitas terbaru
- **Quick Actions** — Aksi cepat

---

### Fase 3 — Workspace Enhanced (2028)

#### Team Features

- **Team Workspace** — Kolaborasi tim
- **Team Members** — Undang anggota tim
- **Roles & Permissions** — Role admin, editor, viewer
- **Shared Monitoring** — Monitor bareng
- **Activity Log** — Jejak aktivitas tim

#### Advanced Monitoring

- **Custom Intervals** — Interval monitoring kustom
- **Multi-URL Check** — Cek banyak URL sekaligus
- **Keyword Monitoring** — Monitor kata kunci di website
- **Certificate Transparency** — Monitor CT logs
- **Custom Alerts** — Threshold alert kustom

#### Reporting

- **Laporan Bulanan** — Laporan otomatis
- **PDF Export** — Export laporan ke PDF
- **CSV Export** — Export data ke CSV
- **Custom Reports** — Laporan kustom
- **Scheduled Reports** — Laporan terjadwal

#### DNS Hosting

- **DNS Zone Editor** — Edit DNS zone
- **DNS Templates** — Template DNS populer
- **DNS History** — History perubahan
- **API Access** — Kelola DNS via API

---

### Fase 4 — Workspace Enterprise (2029)

#### Enterprise Features

- **Multi User (Enterprise)** — Tim besar
- **SSO Integration** — Login perusahaan (SAML, OIDC)
- **Audit Log** — Jejak aktivitas lengkap
- **SLA** — Jaminan uptime
- **Custom Branding** — Dashboard custom
- **Priority Support** — Support prioritas
- **Dedicated Account Manager** — Account manager khusus

#### Advanced Analytics

- **Trend Analysis** — Analisis tren
- **Cost Optimization** — Optimasi biaya
- **Risk Assessment** — Penilaian risiko
- **Compliance Check** — Cek kepatuhan
- **Benchmark** — Perbandingan dengan industri

---

## Pilar 3: Discover — Menemukan Peluang

> **Implementasi:** Business Intelligence (Enterprise). Tujuan: insight berbasis data publik dan pengambilan keputusan.

### Fase 4 — BI MVP (2029)

#### Data Sources

- **Public DNS Data** — Data DNS publik
- **WHOIS Data** — Data registrasi domain
- **SSL Data** — Data sertifikat SSL
- **Technology Data** — Data teknologi website
- **Geographic Data** — Data geografis

#### Analysis Features

- **Market Analysis** — Analisis pasar digital per wilayah
  - Berapa bisnis yang sudah punya website
  - Berapa yang belum memiliki domain
  - Berapa yang belum memakai SSL
  - Teknologi yang umum dipakai
  - Peluang digital yang masih terbuka
- **Competitor Analysis** — Analisis kompetitor
- **Trend Detection** — Deteksi tren digital
- **Opportunity Finder** — Temukan peluang bisnis

#### Reports

- **Market Report** — Laporan pasar
- **Industry Report** — Laporan industri
- **Regional Report** — Laporan regional
- **Custom Report** — Laporan kustom

---

### Fase 5 — BI Advanced (2030-2031)

#### Advanced Intelligence

- **Real-time Analytics** — Analisis real-time
- **Predictive Analytics** — Analisis prediktif
- **Sentiment Analysis** — Analisis sentimen
- **Network Intelligence** — Insight jaringan

#### Platform Features

- **BI Dashboard** — Dashboard BI lengkap
- **API Access** — Akses data via API
- **White Label** — BI untuk client
- **Integration** — Integrasi dengan tools lain
- **Custom Models** — Model analisis kustom

---

## Technology Stack

### Backend

- **Framework:** FastAPI (Python)
- **Templates:** Jinja2
- **Cache:** Redis + in-memory fallback
- **Rate Limiting:** Per-IP (60 req/min)
- **Validation:** Custom validators (domain, IP, URL, host)

### Frontend

- **CSS:** Custom CSS with variables (65+ variables, light/dark themes)
- **JavaScript:** Vanilla JS (handleToolForm, displayResults, URL state)
- **PWA:** manifest.json + service worker
- **Responsive:** 1024px + 768px + 480px breakpoints (desktop, tablet, mobile, small mobile)

### Infrastructure

| Component | 2026 | 2027 | 2028 | 2029 | 2030-2031 |
|-----------|------|------|------|------|-----------|
| Server | Ubuntu + AAPanel | Upgrade | 2 servers | Load Balancer | Multi Region |
| Web Server | Nginx | Nginx | Nginx | Nginx | Nginx |
| Database | SQLite → PostgreSQL | PostgreSQL | PostgreSQL | PG Primary+Replica | PG Multi Region |
| Cache | Redis | Redis | Redis | Redis Cluster | Redis Cluster |
| DNS | External | External | DNS Hosting | DNS Anycast | Public DNS |

---

## Security Features

### Fase 1 (sudah diimplementasi)

- **Input Validation** — Semua input divalidasi sebelum diproses
- **XSS Protection** — HTML escaping + CSP headers + JavaScript Map
- **Rate Limiting** — 60 requests per minute per IP
- **Security Headers** — X-Content-Type-Options, X-Frame-Options, X-XSS-Protection
- **Request ID** — X-Request-ID header untuk distributed tracing (uuid, 8 char)
- **HTTPS Only** — HSTS header untuk production
- **No Data Storage** — Tidak menyimpan data pribadi pengguna

### Fase 2+

- **User Authentication** — Secure login system
- **API Key System** — API key management
- **CSRF Protection** — Cross-site request forgery protection
- **Data Encryption** — Encrypted at rest & in transit
- **Audit Logging** — Activity tracking
- **GDPR Compliance** — Data privacy compliance

---

## SEO Checklist

- [x] Meta title & description
- [x] Open Graph tags
- [x] Structured data (JSON-LD: BreadcrumbList + FAQPage)
- [x] Fast loading time
- [x] Mobile friendly
- [x] robots.txt
- [x] sitemap.xml
- [x] Canonical URL
- [x] FAQ rich snippets
- [x] Education content (25 tools)
- [x] Breadcrumb navigation

---

## Performance Checklist

- [x] Response time < 1 detik
- [x] Memory usage < 100MB per request
- [x] No heavy dependencies
- [x] Redis cache (+ in-memory fallback)
- [x] Graceful error handling
- [x] X-Process-Time header
- [x] X-Request-ID header (distributed tracing)
- [x] Async non-blocking (asyncio.to_thread)
- [x] HTTP fallback (HTTPS → HTTP)
- [x] HTTP client reuse (shared httpx.AsyncClient + connection pooling)
- [x] Cache TTL tuning (blacklist 10min, CDN 1hr, DNS/Website 1-5min)

---

## Feature Checklist

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

---

# Fitur Hub.konektivitas.com — Blockchain Infrastructure

> Platform infrastruktur blockchain yang menyediakan akses node RPC API untuk developer, startup, perusahaan, dan aplikasi Web3.

---

## Visi

Menjadi penyedia infrastruktur konektivitas blockchain yang sederhana, cepat, dan andal untuk developer di Indonesia maupun global.

## Misi

1. Menyediakan RPC Node berkinerja tinggi.
2. Mempermudah integrasi blockchain melalui REST API dan JSON-RPC.
3. Menyediakan endpoint yang stabil dengan uptime tinggi.
4. Mendukung berbagai jaringan blockchain populer.
5. Menjadi fondasi berbagai aplikasi Web3.

---

## Fase 1 — MVP (2026)

### Authentication System

- **User Registration** — Email + password dengan email verification
- **Login System** — JWT token-based authentication
- **Password Hashing** — Bcrypt untuk keamanan
- **Session Management** — Token refresh mechanism
- **Profile Management** — Edit profil pengguna

### API Key Management

- **Generate API Keys** — Prefix `hk_` untuk identifikasi
- **Hash API Keys** — SHA-256 hash sebelum storage
- **CRUD Operations** — Create, list, update, delete API keys
- **Network Permissions** — Batasi akses per blockchain network
- **Key Expiration** — Set masa berlaku API key
- **Rate Limit Per Key** — Batasi request per API key

### RPC Proxy

- **JSON-RPC Proxy** — Proxy untuk Ethereum mainnet
- **Request Validation** — Validasi JSON-RPC request format
- **Response Caching** — Cache response di Redis
- **Rate Limiting** — 100 request per menit per API key
- **Request Logging** — Log semua RPC requests

### Dashboard

- **Landing Page** — Hero section, features, pricing
- **User Dashboard** — Overview usage statistics
- **API Key Management UI** — Kelola API keys dari UI
- **Network Status** — Status kesehatan node
- **Usage Statistics** — Grafik penggunaan API

### API Documentation

- **Swagger/OpenAPI** — Interactive API documentation
- **Code Examples** — Contoh integrasi Python, JavaScript, Go
- **SDK Information** — Library yang tersedia

### Monitoring

- **Health Check Endpoints** — `/api/v1/status`
- **Node Health** — Cek kesehatan blockchain node
- **Prometheus Metrics** — Export metrics untuk monitoring
- **Grafana Dashboards** — Dashboard monitoring visual

### Security

- **API Key Authentication** — Wajib API key untuk akses
- **JWT Validation** — Validasi token di setiap request
- **CORS Configuration** — Cross-origin resource sharing
- **Rate Limiting** — Per-API-key rate limiting
- **Request Logging** — Audit trail untuk semua request

---

## Fase 2 — Multi Blockchain (2027)

### Multi Chain Support

| Network | Chain ID | Status |
|---------|----------|--------|
| Ethereum | 1 | ✅ MVP |
| Polygon | 137 | 📋 Planned |
| BSC | 56 | 📋 Planned |
| Arbitrum | 42161 | 📋 Planned |
| Optimism | 10 | 📋 Planned |
| Avalanche | 43114 | 📋 Planned |

### Load Balancer

- **Round-Robin Routing** — Distribusi beban merata
- **Health-Based Routing** — Route ke node sehat
- **Failover Handling** — Automatic failover jika node down

### WebSocket

- **WebSocket Proxy** — Proxy untuk real-time events
- **Subscription Management** — Kelola subscriptions
- **Connection Pooling** — Optimasi koneksi

### Analytics

- **Detailed Usage Analytics** — Analisis penggunaan mendalam
- **Cost Tracking** — Lacak biaya penggunaan
- **Performance Metrics** — Metrik performa API

### Billing

- **Usage-Based Billing** — Bayar sesuai penggunaan
- **Plan Management** — Kelola paket berlangganan
- **Invoice Generation** — Generate invoice otomatis

### Team Management

- **Team Workspace** — Kolaborasi tim
- **Team Members** — Undang anggota tim
- **Roles & Permissions** — Role admin, developer, viewer
- **Shared API Keys** — API keys yang dibagikan tim

---

## Fase 3 — Enterprise (2028-2029)

### Global Infrastructure

- **Multi-Region Deployment** — Server di beberapa wilayah
- **Auto Scaling** — Otomatis menambah resource
- **CDN Integration** — CDN untuk static assets

### Enterprise Features

- **SSO Integration** — Login perusahaan (SAML, OIDC)
- **Audit Logging** — Jejak aktivitas lengkap
- **SLA Monitoring** — Jaminan uptime
- **Custom Rate Limits** — Rate limit kustom per klien
- **Priority Support** — Support prioritas

### Marketplace

- **Third-Party Node Providers** — Provider node pihak ketiga
- **Revenue Sharing** — Berbagi pendapatan
- **Quality Monitoring** — Monitor kualitas layanan

---

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register pengguna baru |
| `/api/v1/auth/login` | POST | Login |
| `/api/v1/auth/refresh` | POST | Refresh token |
| `/api/v1/auth/me` | GET | Ambil data pengguna |
| `/api/v1/auth/me` | PUT | Update profil |

### API Keys

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/keys` | GET | List API keys |
| `/api/v1/keys` | POST | Buat API key baru |
| `/api/v1/keys/{id}` | PUT | Update API key |
| `/api/v1/keys/{id}` | DELETE | Hapus API key |

### RPC Proxy

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/rpc/{network}` | POST | JSON-RPC proxy |
| `/rpc/{network}/health` | GET | Node health check |

### Blockchain Data

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/networks` | GET | List supported networks |
| `/api/v1/networks/{slug}` | GET | Network details |
| `/api/v1/{network}/block/{id}` | GET | Get block |
| `/api/v1/{network}/tx/{hash}` | GET | Get transaction |
| `/api/v1/{network}/address/{addr}` | GET | Get address info |
| `/api/v1/{network}/balance/{addr}` | GET | Get balance |
| `/api/v1/{network}/broadcast` | POST | Broadcast transaction |

### Monitoring

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/status` | GET | System status |
| `/api/v1/status/{network}` | GET | Network status |
| `/api/v1/usage` | GET | Usage statistics |
| `/api/v1/usage/daily` | GET | Daily usage stats |

---

## Technology Stack

### Backend

- **Framework:** FastAPI (Python)
- **Database:** PostgreSQL 15+
- **Cache:** Redis 7+
- **Auth:** JWT + API Keys (bcrypt + SHA-256)
- **Migration:** Alembic

### Infrastructure

- **Container:** Docker + Docker Compose
- **Reverse Proxy:** Nginx
- **Orchestration:** Traefik (optional)
- **Monitoring:** Prometheus + Grafana
- **Database:** PostgreSQL (relational, berbeda dengan SQLite Konektivitas.com)

### Architecture

```
Client Apps → Nginx → FastAPI → PostgreSQL
                            → Redis Cache
                            → Blockchain Nodes
                            → Prometheus → Grafana
```

---

## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| email | VARCHAR(255) | Unique email |
| password_hash | VARCHAR(255) | Bcrypt hash |
| full_name | VARCHAR(255) | Nama lengkap |
| company | VARCHAR(255) | Perusahaan |
| is_active | BOOLEAN | Status aktif |
| plan | VARCHAR(50) | Paket: free/pro/team |
| created_at | TIMESTAMP | Tanggal daftar |

### API Keys Table

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
| expires_at | TIMESTAMP | Masa berlaku |

### Usage Logs Table

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| api_key_id | UUID | Foreign key ke api_keys |
| network | VARCHAR(50) | Blockchain network |
| method | VARCHAR(100) | RPC method |
| response_time_ms | INTEGER | Response time |
| status_code | INTEGER | HTTP status |
| created_at | TIMESTAMP | Timestamp |

### Blockchain Networks Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(100) | Network name |
| slug | VARCHAR(50) | URL-friendly name |
| chain_id | INTEGER | Chain ID |
| rpc_endpoint | TEXT | RPC URL |
| ws_endpoint | TEXT | WebSocket URL |
| explorer_url | TEXT | Block explorer URL |
| is_active | BOOLEAN | Status aktif |

---

## Referensi

- [BRIEF.md](BRIEF.md) — Visi, misi, dan filosofi
- [BRIEF2.md](BRIEF2.md) — Detail teknis dan arsitektur
- [ROADMAP.md](ROADMAP.md) — Roadmap pengembangan 5 tahun
- [AGENT.md](AGENT.md) — Panduan untuk AI/agent
- [plans/hub-konektivitas-plan.md](plans/hub-konektivitas-plan.md) — Rencana detail Hub.konektivitas.com
