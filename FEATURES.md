# Fitur Konektivitas.com

> Daftar lengkap fitur per fase implementasi. Satu platform modular dengan empat pilar: **Learn**, **Manage**, **Discover**, **Connect**.

---

## Pilar 1: Learn — Memahami Internet

> **Implementasi:** Public Tools (gratis). Tujuan: edukasi, traffic, dan SEO.

### Fase 1 — Public Tools MVP (2026) ✅ SELESAI

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

> **Implementasi:** Utility Search Engine + Business Intelligence. Tujuan: menemukan objek berguna di internet dan menghasilkan insight.

### Fase 2 — Core Engine & Jobs Vertical (2027)

#### Core Engine

- **Crawler Infrastructure** — HTTP-first crawler (httpx + selectolax), Playwright fallback
- **Parser Pipeline** — Extraction → Cleaning → Entity Detection → Normalization → Deduplication → Validation
- **Rule-Based Normalization** — Normalisasi title, skill, location, salary tanpa AI
- **robots.txt Compliance** — Respectful crawling dengan rate limit per source
- **PostgreSQL Database** — Schema relasional (companies, jobs, skills, tools, sources, categories)
- **PostgreSQL FTS + pg_trgm** — Full text search + fuzzy matching untuk MVP
- **UtilityRank** — Scoring algorithm (freshness, availability, relevance, reliability, completeness)

#### Jobs Vertical (MVP)

- **Job Discovery** — Crawling dari public career pages
- **Structured Job Data** — Title, company, location, remote, salary, skills, employment type
- **Active Status Detection** — 🟢 ACTIVE / 🟡 CLOSING SOON / ⚪ UNKNOWN / 🔴 EXPIRED
- **Skill Matching** — Pencarian berdasarkan skill requirements
- **Remote Filter** — Filter remote/hybrid/onsite
- **Salary Range Filter** — Filter berdasarkan range gaji

#### Search Experience

- **Homepage** — "What do you want to accomplish?" search interface
- **Natural Language Query** — Pencarian dalam bahasa alami
- **Intent Detection** — Auto-detect intent (work, buy, learn, build) dari query
- **Structured Results** — Hasil terstruktur, bukan sekadar URL
- **Filter & Sort** — By status, location, price, utility score
- **Dark Mode** — Light/dark theme

#### Background Jobs

- **APScheduler** — Crawl schedule (jobs: 6 jam, verification: 6 jam, index rebuild: 24 jam)
- **Active/Expired Detection** — Re-crawl untuk cek status job masih aktif

---

### Fase 3 — Multi-Vertical & B2B (2028)

#### Vertical Baru

| Vertical | Source | Priority |
|----------|--------|----------|
| Tools | Product Hunt, GitHub, direktori tools | Tinggi |
| APIs | RapidAPI, ProgrammableWeb | Tinggi |
| Suppliers | Direktori bisnis, marketplace B2B | Sedang |
| Products | Marketplace, e-commerce directories | Sedang |
| Courses | Coursera, Udemy, edX | Sedang |
| Opportunities | Affiliate directories, freelance platforms | Rendah |

#### Enhancements

- **Multi-Vertical Crawler** — Crawler per vertical dengan parser khusus
- **Category System** — Hierarchical categories dengan auto-classification
- **Advanced UtilityRank** — Lebih banyak faktor scoring
- **Saved Searches** — Simpan pencarian (Pro feature)
- **Alerts** — Notifikasi saat ada hasil baru (Pro feature)
- **Search History** — Riwayat pencarian
- **Advanced Filters** — Filter lanjutan per vertical

#### Intelligence Features

- **Trend Detection** — Deteksi tren skill, tools, salary
- **Recommendation** — Rekomendasi berdasarkan search history
- **Monitoring** — Monitor perubahan data (job posting, tool availability)
- **Historical Data** — Data historis untuk analisis trend

#### B2B Features

- **Market Intelligence** — Berapa banyak perusahaan hiring Python Developer?
- **Supplier Intelligence** — Analisis supplier per kategori/lokasi
- **Labor Intelligence** — Skill demand analysis, salary benchmarking
- **Competitor Intelligence** — Track perubahan di industri
- **Custom Reports** — Laporan kustom untuk enterprise

#### Developer API

- **Utility Search API** — `GET /v1/search` dengan structured query
- **Jobs API** — `GET /v1/jobs` dengan filter
- **Tools API** — `GET /v1/tools` dengan filter
- **APIs API** — `GET /v1/apis` dengan filter
- **Suppliers API** — `GET /v1/suppliers` dengan filter
- **API Key System** — Register & kelola API key
- **Rate Limiting** — Per-API-key rate limiting

#### Search Scale

- **OpenSearch** — Migrasi dari PostgreSQL FTS ke OpenSearch
- **Full-Text Advanced** — Autocomplete, synonym, typo tolerance

---

### Fase 4 — Intelligence & Ecosystem (2029)

#### Advanced Search

- **Semantic Search** — Understanding intent lebih dalam
- **Cross-Vertical Search** — Search lintas vertical
- **Personalized Results** — Results yang dipersonalisasi
- **AI Classification** — AI untuk entity extraction & normalization (jika sudah ada revenue)

#### Ecosystem

- **Developer Marketplace** — Third-party integrations
- **Data Contributors** — Sumbang data ke index
- **Partner Program** — Revenue sharing dengan partner
- **Community** — Forum, documentation, tutorials

#### Business Intelligence

- **GeoIP Indonesia Database** — Data geografis IP Indonesia
- **ASN Database** — Database ASN lengkap
- **IP Reputation** — Reputasi IP berbasis data
- **Market Analysis** — Analisis pasar digital per wilayah
- **CDN Analytics** — Analisis penggunaan CDN
- **Network Intelligence** — Insight jaringan
- **Custom Reports** — Laporan kustom untuk enterprise

---

### Fase 5 — Utility Platform (2030-2031)

#### Platform Features

- **100+ Vertical Categories** — Index terstruktur atas semua kategori utilitas
- **Real-Time Index** — Update data dalam hitungan menit
- **Global Coverage** — Data dari seluruh dunia
- **Multi-Language** — Bahasa Indonesia, English, dan lainnya
- **Mobile App** — Search dari genggaman

#### Advanced Intelligence

- **Real-time Analytics** — Analisis real-time
- **Predictive Analytics** — Analisis prediktif
- **Sentiment Analysis** — Analisis sentimen
- **BI Dashboard** — Dashboard BI lengkap
- **White Label** — BI untuk client

#### Developer Ecosystem

- **Marketplace** — Third-party tools & integrasi
- **Plugin System** — Extend Utility Search
- **Revenue Sharing** — Berbagi pendapatan dengan developer

---

## Pilar 4: Connect — Menghubungkan Infrastruktur

> **Implementasi:** Developer Platform + Blockchain Infrastructure. Tujuan: menghubungkan aplikasi dan infrastruktur.

### Fase 2 — Developer Platform MVP (2027)

#### API Platform

- **API Key System** — Daftar & kelola API key
- **API Dashboard** — Usage stats, rate limit info
- **Dynamic DNS** — Update DNS record via API

#### Authentication

- **User Registration** — Email + password dengan email verification
- **Login System** — JWT token-based authentication
- **Password Hashing** — Bcrypt untuk keamanan
- **Session Management** — Token refresh mechanism

---

### Fase 3 — Blockchain Infrastructure (2028)

#### RPC Node Platform

- **JSON-RPC Proxy** — Proxy untuk Ethereum mainnet + multi-chain
- **Request Validation** — Validasi JSON-RPC request format
- **Response Caching** — Cache response di Redis
- **Rate Limiting** — 100 request per menit per API key
- **Request Logging** — Log semua RPC requests

#### Multi Chain Support

| Network | Chain ID | Status |
|---------|----------|--------|
| Ethereum | 1 | 📋 Planned |
| Polygon | 137 | 📋 Planned |
| BSC | 56 | 📋 Planned |
| Arbitrum | 42161 | 📋 Planned |
| Optimism | 10 | 📋 Planned |
| Avalanche | 43114 | 📋 Planned |

#### Load Balancer

- **Round-Robin Routing** — Distribusi beban merata
- **Health-Based Routing** — Route ke node sehat
- **Failover Handling** — Automatic failover jika node down

#### WebSocket

- **WebSocket Proxy** — Proxy untuk real-time events
- **Subscription Management** — Kelola subscriptions
- **Connection Pooling** — Optimasi koneksi

#### Blockchain Data API

- **Network Discovery** — List supported networks
- **Block API** — Get block data
- **Transaction API** — Get transaction data
- **Address API** — Get address info & balance
- **Broadcast API** — Broadcast transaksi
- **Smart Contract API** — Interaksi smart contract

#### Monitoring

- **Health Check Endpoints** — `/api/v1/status`
- **Node Health** — Cek kesehatan blockchain node
- **Prometheus Metrics** — Export metrics untuk monitoring
- **Grafana Dashboards** — Dashboard monitoring visual

#### API Documentation

- **Swagger/OpenAPI** — Interactive API documentation
- **Code Examples** — Contoh integrasi Python, JavaScript, Go
- **SDK Information** — Library yang tersedia

---

### Fase 4 — Enterprise Developer (2029)

#### Enterprise Features

- **SSO Integration** — Login perusahaan (SAML, OIDC)
- **Audit Logging** — Jejak aktivitas lengkap
- **SLA Monitoring** — Jaminan uptime
- **Custom Rate Limits** — Rate limit kustom per klien
- **Priority Support** — Support prioritas

#### Analytics & Billing

- **Detailed Usage Analytics** — Analisis penggunaan mendalam
- **Cost Tracking** — Lacak biaya penggunaan
- **Performance Metrics** — Metrik performa API
- **Usage-Based Billing** — Bayar sesuai penggunaan
- **Invoice Generation** — Generate invoice otomatis

#### Marketplace

- **Third-Party Node Providers** — Provider node pihak ketiga
- **Revenue Sharing** — Berbagi pendapatan
- **Quality Monitoring** — Monitor kualitas layanan

---

### Fase 5 — Global Infrastructure (2030-2031)

#### Global Infrastructure

- **Multi-Region Deployment** — Server di beberapa wilayah
- **Auto Scaling** — Otomatis menambah resource
- **CDN Integration** — CDN untuk static assets
- **Load Balancer** — High availability

#### Platform Features

- **Developer Marketplace** — Jual/beli tools & integrasi
- **Plugin System** — Extend Konektivitas
- **Enterprise API v3** — Custom solutions

---

## Database Schema

### Public Tools (Fase 1 — SQLite → PostgreSQL)

> Tidak ada database untuk public tools. Semua data bersifat real-time (DNS, WHOIS, SSL, IP, HTTP).

### Utility Search (PostgreSQL)

#### Companies Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | Company name |
| url | TEXT | Company website |
| logo_url | TEXT | Logo URL |
| location | VARCHAR(255) | Headquarters |
| industry | VARCHAR(100) | Industry category |
| created_at | TIMESTAMP | First seen |

#### Jobs Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| company_id | INTEGER | FK ke companies |
| title | VARCHAR(255) | Normalized title |
| title_raw | TEXT | Original title |
| description | TEXT | Job description |
| location | VARCHAR(255) | Job location |
| remote | BOOLEAN | Remote flag |
| salary_min | INTEGER | Minimum salary |
| salary_max | INTEGER | Maximum salary |
| salary_currency | VARCHAR(3) | Currency code |
| employment_type | VARCHAR(50) | full-time, part-time, etc |
| posted_date | DATE | When posted |
| expiration_date | DATE | When expires |
| source_url | TEXT | Original URL |
| source_id | INTEGER | FK ke sources |
| status | VARCHAR(20) | active, expired, etc |
| utility_score | FLOAT | UtilityRank score |
| created_at | TIMESTAMP | First indexed |
| updated_at | TIMESTAMP | Last updated |

#### Skills Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(100) | Normalized skill name |
| category | VARCHAR(50) | Programming, Design, etc |

#### Job_Skills Table

| Column | Type | Description |
|--------|------|-------------|
| job_id | INTEGER | FK ke jobs |
| skill_id | INTEGER | FK ke skills |

#### Tools Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | Tool name |
| description | TEXT | Tool description |
| url | TEXT | Tool URL |
| category | VARCHAR(100) | Tool category |
| pricing | VARCHAR(20) | free, freemium, paid |
| features | JSONB | Tool features |
| status | VARCHAR(20) | available, unavailable |
| utility_score | FLOAT | UtilityRank score |
| created_at | TIMESTAMP | First indexed |
| updated_at | TIMESTAMP | Last updated |

#### APIs Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | API name |
| description | TEXT | API description |
| url | TEXT | API URL |
| docs_url | TEXT | Documentation URL |
| category | VARCHAR(100) | API category |
| pricing_model | VARCHAR(50) | Pricing model |
| free_tier | BOOLEAN | Has free tier |
| sdks | JSONB | Available SDKs |
| status | VARCHAR(20) | online, offline, etc |
| utility_score | FLOAT | UtilityRank score |
| created_at | TIMESTAMP | First indexed |
| updated_at | TIMESTAMP | Last updated |

#### Suppliers Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | Supplier name |
| description | TEXT | Supplier description |
| url | TEXT | Supplier website |
| category | VARCHAR(100) | Supplier category |
| location | VARCHAR(255) | Supplier location |
| products | JSONB | Product list |
| contact_email | VARCHAR(255) | Contact email |
| contact_phone | VARCHAR(50) | Contact phone |
| utility_score | FLOAT | UtilityRank score |
| created_at | TIMESTAMP | First indexed |
| updated_at | TIMESTAMP | Last updated |

#### Sources Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(100) | Source name |
| url | TEXT | Source URL |
| type | VARCHAR(50) | career_page, job_board, directory, etc |
| crawl_interval | INTEGER | Crawl interval in seconds |
| last_crawled_at | TIMESTAMP | Last crawl time |
| is_active | BOOLEAN | Active status |
| robots_allowed | BOOLEAN | robots.txt allows crawling |

#### Categories Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(100) | Category name |
| slug | VARCHAR(100) | URL-friendly name |
| parent_id | INTEGER | Parent category (self-ref) |
| object_type | VARCHAR(50) | job, tool, api, supplier, product, course |

### Blockchain Infrastructure (PostgreSQL)

#### Users Table

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

#### API Keys Table

| Column | Type | Description |
|--------|------|-------------|
| id | UUID | Primary key |
| user_id | UUID | Foreign key ke users |
| name | VARCHAR(100) | Nama key |
| key_hash | VARCHAR(255) | SHA-256 hash |
| key_prefix | VARCHAR(10) | Prefix untuk display (`kn_`) |
| networks | TEXT[] | Blockchain networks |
| rate_limit | INTEGER | Request per menit |
| is_active | BOOLEAN | Status aktif |
| expires_at | TIMESTAMP | Masa berlaku |

#### Usage Logs Table

| Column | Type | Description |
|--------|------|-------------|
| id | BIGSERIAL | Primary key |
| api_key_id | UUID | Foreign key ke api_keys |
| network | VARCHAR(50) | Blockchain network |
| method | VARCHAR(100) | RPC method |
| response_time_ms | INTEGER | Response time |
| status_code | INTEGER | HTTP status |
| created_at | TIMESTAMP | Timestamp |

#### Blockchain Networks Table

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

## Search Implementation

### Phase 1 — PostgreSQL FTS + pg_trgm

```text
PostgreSQL
├── Full Text Search (tsvector, tsquery)
├── pg_trgm (fuzzy matching, similarity)
├── GIN indexes (fast text search)
├── Custom ranking (utility_score + freshness + relevance)
```

### Phase 2 — OpenSearch (ketika data sudah jutaan)

```text
PostgreSQL
      │
      ├── Source of Truth
      │
      └── OpenSearch
              ↓
          Search
```

---

## Background Jobs

### MVP — APScheduler

```text
01:00 → crawl source A (jobs)
02:00 → crawl source B (tools)
03:00 → crawl source C (APIs)
04:00 → verify expired jobs
05:00 → rebuild search indexes
06:00 → check API status
```

### Scale — Celery + Redis

```text
Celery Workers
├── Crawler Tasks (per source)
├── Verification Tasks (active/expired check)
├── Index Tasks (rebuild FTS indexes)
└── Notification Tasks (alert delivery)
```

### Schedule

| Job | Interval | Description |
|-----|----------|-------------|
| Job crawl | 6 jam | Crawl career pages & job boards |
| Tool crawl | 24 jam | Crawl tool directories |
| API crawl | 12 jam | Crawl API directories |
| Supplier crawl | 7 hari | Crawl supplier directories |
| Job verification | 6 jam | Check if jobs are still active |
| API health check | 1 jam | Check if APIs are online |
| Tool availability | 12 jam | Check if tools are accessible |
| Index rebuild | 24 jam | Rebuild search indexes |
| Score recalculation | 24 jam | Recalculate utility scores |

---

## UtilityRank

### Scoring Factors

```text
Utility Score = weighted_average(
    Freshness      (0.20)  — Seberapa baru data ini
    Availability   (0.20)  — Apakah masih bisa digunakan
    Relevance      (0.25)  — Seberapa relevan dengan query
    Reliability    (0.10)  — Seberapa reliable sumbernya
    Completeness   (0.15)  — Seberapa lengkap data field-nya
    Popularity     (0.05)  — Seberapa banyak orang mengakses
    Accessibility  (0.05)  — Seberapa mudah diakses/digunakan
)
```

### Score Display

```text
Utility Score: 94/100
```

### Ranking Philosophy

> **Hasil terbaik bukan yang paling banyak backlink-nya, tetapi yang paling berguna bagi intent user.**

---

## Freshness & Availability

### Status System

| Object | Status Options | Detection Method |
|--------|---------------|-----------------|
| Jobs | 🟢 ACTIVE, 🟡 CLOSING SOON, ⚪ UNKNOWN, 🔴 EXPIRED | Re-crawl & check apply link |
| APIs | 🟢 ONLINE, 🟡 DEGRADED, 🔴 OFFLINE | Health check endpoint |
| Tools | 🟢 AVAILABLE, 🔴 UNAVAILABLE | HTTP status check |
| Products | 🟢 IN STOCK, 🟡 LOW STOCK, 🔴 OUT OF STOCK | Price/availability check |

### Freshness Scoring

- **Re-crawl Interval** — Jobs: 6 jam, Tools: 24 jam, APIs: 1 jam, Suppliers: 7 hari
- **Staleness Penalty** — Data yang sudah lama tidak di-crawl mendapat penalty score
- **Active Priority** — Data dengan status aktif selalu diprioritaskan

---

## Data Normalization Schema

### Job Schema

```text
JOB
├── title (normalized)
├── company
├── location (city, country, remote_flag)
├── remote (boolean)
├── salary_min / salary_max / salary_currency
├── skills[] (normalized)
├── employment_type (full-time, part-time, contract, internship)
├── posted_date
├── expiration_date
├── source_url
├── source_name
├── status (active, closing_soon, expired, unknown)
├── utility_score
└── created_at / updated_at
```

### Tool Schema

```text
TOOL
├── name
├── description
├── url
├── category (calculator, converter, generator, etc.)
├── pricing (free, freemium, paid, enterprise)
├── features[]
├── status (available, unavailable)
├── source_name
├── utility_score
└── created_at / updated_at
```

### API Schema

```text
API
├── name
├── description
├── url
├── docs_url
├── category
├── pricing_model
├── free_tier (boolean)
├── sdks[] (python, javascript, go, etc.)
├── status (online, degraded, offline)
├── source_name
├── utility_score
└── created_at / updated_at
```

### Supplier Schema

```text
SUPPLIER
├── name
├── description
├── url
├── category
├── location (city, country)
├── products[]
├── contact_email
├── contact_phone
├── source_name
├── utility_score
└── created_at / updated_at
```

---

## Technology Stack

### Backend

- **Framework:** FastAPI (Python)
- **Templates:** Jinja2
- **Cache:** Redis + in-memory fallback
- **Rate Limiting:** Per-IP (60 req/min) untuk tools; Per-API-key untuk developer platform
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
| Search | — | PostgreSQL FTS | OpenSearch | OpenSearch Cluster | OpenSearch Multi Region |
| Queue | — | APScheduler | Celery + Redis | Celery + Redis Cluster | Celery + Redis Cluster |
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
- [x] Cache TTL tuning (optimized per data volatility)

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

## Filosofi Produk

> **Intent → Discovery → Action → Outcome**

Bukan: Attention → scrolling → ads.

Outcome yang dibantu:
- Mendapat pekerjaan
- Mendapat pelanggan
- Mendapat supplier
- Mendapat produk
- Menemukan software
- Membangun sesuatu
- Menjalankan bisnis
- Menghasilkan uang

### Prinsip

1. **MVP tidak bergantung pada paid AI API** — Rule-based dulu, AI hanya ketika diperlukan
2. **Mulai dari satu vertical** — Buktikan value, baru perluas
3. **Core Engine → Vertical sebagai modul** — Tidak perlu rewrite saat menambah vertical
4. **Solo developer friendly** — Stack yang bisa dijalankan dengan 1 VPS

---

## Referensi

- [BRIEF.md](BRIEF.md) — Visi, misi, dan filosofi
- [BRIEF2.md](BRIEF2.md) — Detail teknis dan arsitektur
- [BRIEF3.md](BRIEF3.md) — Brief Utility Search Engine
- [BRIEF4.md](BRIEF4.md) — Tech stack Utility Search Engine
- [ROADMAP.md](ROADMAP.md) — Roadmap pengembangan 5 tahun
- [AGENT.md](AGENT.md) — Panduan untuk AI/agent
- [plans/hub-konektivitas-plan.md](plans/hub-konektivitas-plan.md) — Rencana detail blockchain infrastructure
