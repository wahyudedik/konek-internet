# Roadmap Konektivitas.com (2026–2031)

> **"Bagaimana Konektivitas menjadi tempat pertama yang dibuka seseorang ketika ingin memahami, mengelola, atau mengembangkan aset digitalnya?"**

---

## 🎯 Tahun 1 — Foundation (2026)

**Target:** Menjadi platform utilitas internet terbesar berbahasa Indonesia.

### ✅ Public Tools — 30 Tools (SELESAI)

- ✅ 30 Tools DNS, Domain, SSL, Website, IP (+5 baru: Traceroute, Tech Detector, Speed Test, DNS History, SSL History)
- ✅ 36+ API Endpoints (RESTful, rate limit 60 req/min)
- ✅ 30 Tool Pages dengan form interaktif
- ✅ Redis + in-memory Cache
- ✅ SEO: JSON-LD, robots.txt, sitemap.xml
- ✅ Dark Mode, PWA, Tool History, URL State
- ✅ Mobile Responsive, Keyboard Shortcuts
- ✅ Section Edukasi interaktif di semua tool pages
- ✅ CDN Detection, API Dashboard

### Target Metrics

| Metric | Target | Status |
|--------|--------|--------|
| Visitor/bulan | 100.000 | 🔄 |
| Tools | 30 | ✅ |
| API request/hari | 10.000 | 🔄 |
| SEO ranking | Top 3 "dns checker indonesia" | 🔄 |

### Pendapatan

- Iklan
- Donasi
- Pro tanpa iklan

---

## 🎯 Tahun 2 — Developer Platform & Workspace MVP (2027)

**Target:** Developer mulai memakai API. Workspace MVP launching. Utility Search Engine dimulai.

### Public Tools (lanjutan) ✅

- ✅ 5 tools tambahan (total 30) — Traceroute, Tech Detector, Speed Test, DNS History, SSL History
- Improved SEO & content
- Multi-language support (ID/EN)

### Workspace MVP ✅

- ✅ **User Authentication** — Login, register (JWT token-based)
- ✅ **Domain Management** — Tambah & monitor domain
- ✅ **SSL Monitoring** — Alert saat SSL expiry < 30 hari
- ✅ **DNS Monitoring** — Deteksi perubahan DNS record
- ✅ **Uptime Monitoring** — Cek uptime setiap 5 menit
- ✅ **Notification Settings** — Email, Telegram, Discord
- ✅ **Dashboard** — Overview semua aset internet (6 pages)

### API Platform ✅

- ✅ **API Key System** — Daftar & kelola API key (kn_ prefix)
- ✅ **API Dashboard** — Usage stats, rate limit info (36 endpoints)
- ✅ **Dynamic DNS** — Update DNS record via API (8 endpoints, token-based)

### Utility Search Engine — Core Engine & Jobs Vertical

**Fokus:** Buktikan bahwa Utility Index punya value dengan satu vertical: **Jobs**.

#### Core Engine

- **Crawler Infrastructure** — HTTP-first crawler (httpx + selectolax), Playwright fallback
- **Parser Pipeline** — Extraction → Cleaning → Entity Detection → Normalization → Deduplication → Validation
- **Rule-Based Normalization** — Normalisasi title, skill, location, salary tanpa AI
- **robots.txt Compliance** — Respectful crawling dengan rate limit per source
- **PostgreSQL Database** — Schema relasional (companies, jobs, skills, tools, sources, categories)
- **PostgreSQL FTS + pg_trgm** — Full text search + fuzzy matching
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

#### Background Jobs

- **APScheduler** — Crawl schedule (jobs: 6 jam, verification: 6 jam, index rebuild: 24 jam)
- **Active/Expired Detection** — Re-crawl untuk cek status job masih aktif

#### Deployment

- **Docker Compose** — FastAPI + PostgreSQL + Redis + APScheduler
- **Nginx** — Reverse proxy
- **Ubuntu VPS** — Shared server dengan Konektivitas.com

### Target Metrics

| Metric | Target |
|--------|--------|
| Visitor/bulan | 500.000 |
| Registered users | 10.000 |
| Developer API key | 1.000 |
| Pro subscribers | 100 |
| Domain monitored | 5.000 |
| Indexed jobs | 10.000+ |
| Active sources | 10+ career pages |
| Search latency | < 500ms |

### Kelayakan Utility Search

MVP harus membuktikan 3 hal:
1. **Discovery** — Bisakah menemukan data publik secara otomatis?
2. **Quality** — Bisakah hasil jauh lebih bersih dari pencarian umum?
3. **Utility** — Apakah orang merasa "ini menghemat waktu saya"?

### Pendapatan

- Iklan
- Pro (Rp 49.000/bulan)
- API access

---

## 🎯 Tahun 3 — Infrastructure, Multi-Vertical & Mobile (2028)

**Target:** Mulai menyediakan layanan internet fundamental. Utility Search berkembang ke multi-vertical. Blockchain RPC diluncurkan.

### Public Tools (lanjutan)

- Total 40+ tools
- Tool comparison & batch lookup
- Advanced analytics per tool

### Workspace (enhanced)

- **Team Workspace** — Kolaborasi tim
- **Shared Monitoring** — Monitor bareng
- **Laporan PDF** — Export laporan bulanan
- **Custom Alerts** — Threshold kustom
- **DNS Hosting** — Kelola DNS dari dashboard

### Infrastructure

- **DNS Hosting** — Hosting DNS gratis & premium
- **DNS Anycast (bertahap)** — Resolusi DNS cepat global
- **Status Page** — Status page publik untuk website
- **SSL Certificate Management** — Auto-renewal integration

### Utility Search — Multi-Vertical & B2B

#### Vertical Baru

| Vertical | Source | Priority |
|----------|--------|----------|
| Tools | Product Hunt, GitHub, direktori tools | Tinggi |
| APIs | RapidAPI, ProgrammableWeb | Tinggi |
| Suppliers | Direktori bisnis, marketplace B2B | Sedang |
| Products | Marketplace, e-commerce directories | Sedang |
| Courses | Coursera, Udemy, edX | Sedang |
| Opportunities | Affiliate directories, freelance platforms | Rendah |

#### Intelligence Features

- **Trend Detection** — Deteksi tren skill, tools, salary
- **Recommendation** — Rekomendasi berdasarkan search history
- **Monitoring** — Monitor perubahan data
- **Historical Data** — Data historis untuk analisis trend

#### B2B Features

- **Market Intelligence** — Analisis pasar digital
- **Supplier Intelligence** — Analisis supplier per kategori/lokasi
- **Labor Intelligence** — Skill demand analysis, salary benchmarking
- **Competitor Intelligence** — Track perubahan di industri
- **Custom Reports** — Laporan kustom untuk enterprise

#### Developer API

- **Full API** — Semua vertical tersedia via API
- **Webhooks** — Real-time notification untuk perubahan data
- **SDK** — Python, JavaScript SDK
- **Developer Dashboard** — Usage stats, documentation

#### Search Scale

- **OpenSearch** — Migrasi dari PostgreSQL FTS ke OpenSearch
- **Full-Text Advanced** — Autocomplete, synonym, typo tolerance

### Blockchain Infrastructure — RPC Node Platform

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

#### Load Balancer & WebSocket

- **Round-Robin + Health-Based Routing** — Distribusi beban merata
- **Failover Handling** — Automatic failover jika node down
- **WebSocket Proxy** — Real-time event subscriptions
- **Connection Pooling** — Optimasi koneksi

#### Blockchain Data API

- **Network Discovery** — List supported networks
- **Block API** — Get block data
- **Transaction API** — Get transaction data
- **Address API** — Get address info & balance
- **Broadcast API** — Broadcast transaksi
- **Smart Contract API** — Interaksi smart contract

#### Monitoring & Documentation

- **Health Check Endpoints** — `/api/v1/status`
- **Node Health** — Cek kesehatan blockchain node
- **Prometheus Metrics** — Export metrics untuk monitoring
- **Grafana Dashboards** — Dashboard monitoring visual
- **Swagger/OpenAPI** — Interactive API documentation
- **Code Examples** — Contoh integrasi Python, JavaScript, Go

### Mobile App

- **Mobile App (Android)** — Dashboard di genggaman
- **Push Notifications** — Alert langsung ke HP
- **Quick Check** — Tools tanpa login

### Target Metrics

| Metric | Target |
|--------|--------|
| Visitor/bulan | 1.000.000 |
| Registered users | 50.000 |
| Developer API key | 5.000 |
| Pro subscribers | 1.000 |
| Domain di DNS hosting | 1.000 |
| Mobile app installs | 10.000 |
| Indexed objects | 100.000+ |
| Active verticals | 4+ (Jobs, Tools, APIs, Suppliers) |
| Search daily visitors | 10.000 |
| Search API users | 100 |
| Blockchain users | 1.000 |
| RPC requests/hari | 100.000 |
| Supported networks | 6 |

### Pendapatan

- Iklan
- Pro (Rp 49.000/bulan)
- Team (Rp 99.000-199.000/bulan)
- API access
- DNS hosting
- Blockchain API access

---

## 🎯 Tahun 4 — Business Intelligence & Enterprise (2029)

**Target:** Masuk ke layanan enterprise, data intelligence, dan ekosistem developer.

### Public Tools (lanjutan)

- Total 50+ tools
- API v3 dengan fitur baru
- White-label widget

### Workspace (enterprise)

- **Multi User** — Tim besar
- **Audit Log** — Jejak aktivitas
- **SLA** — Jaminan uptime
- **SSO Integration** — Login perusahaan
- **Custom Branding** — Dashboard custom

### Utility Search — Intelligence & Ecosystem

#### Advanced Search

- **Semantic Search** — Understanding intent lebih dalam
- **Cross-Vertical Search** — Search lintas vertical
- **Personalized Results** — Results yang dipersonalisasi
- **AI Classification** — AI untuk entity extraction & normalization

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

### Blockchain Infrastructure — Enterprise

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

### Target Metrics

| Metric | Target |
|--------|--------|
| Visitor/bulan | 3.000.000 |
| Registered users | 100.000 |
| Developer API key | 20.000 |
| Pro subscribers | 5.000 |
| Enterprise clients | 50 |
| API request/hari | 1.000.000 |
| Indexed objects | 1.000.000+ |
| Search daily visitors | 50.000 |
| Search API users | 1.000 |
| B2B clients | 20 |
| Blockchain users | 5.000 |
| RPC requests/hari | 500.000 |
| Supported networks | 10+ |

### Pendapatan

- Iklan
- Pro (Rp 49.000/bulan)
- Team (Rp 99.000-199.000/bulan)
- Enterprise (Rp 500.000-5.000.000/bulan)
- API access
- DNS hosting
- BI reports
- Blockchain API access

---

## 🎯 Tahun 5 — Internet Platform (2030-2031)

**Target:** Menjadi **pusat data infrastruktur internet Indonesia** dan platform utility index terdepan.

### Public DNS

- **Public DNS Service** — DNS 1.1.1.1-style untuk Indonesia
  - `dns.konektivitas.com` — DNS resolver publik
  - Cepat, aman, privat
  - DNS-over-HTTPS & DNS-over-TLS

### Internet Intelligence

- **Internet Health Dashboard** — Kondisi internet Indonesia real-time
- **BGP Monitoring** — Monitoring routing internet
- **IXP Data** — Data Internet Exchange Point
- **Latency Map** — Peta latensi antar kota
- **Bandwidth Analytics** — Analisis bandwidth nasional

### Utility Search — Full Platform

- **100+ Vertical Categories** — Index terstruktur atas semua kategori utilitas
- **Real-Time Index** — Update data dalam hitungan menit
- **Global Coverage** — Data dari seluruh dunia
- **Multi-Language** — Bahasa Indonesia, English, dan lainnya
- **Advanced Analytics** — Predictive analytics, trend forecasting
- **Custom Dashboards** — Dashboard BI kustom
- **Data Feeds** — Real-time data feeds untuk enterprise
- **White Label** — Utility search untuk client

### Platform

- **Developer Marketplace** — Jual/beli tools & integrasi
- **Plugin System** — Extend Konektivitas
- **Enterprise API v3** — Custom solutions
- **Multi Region** — Server di beberapa wilayah
- **Load Balancer** — High availability

### Mobile App (enhanced)

- **iOS App** — iPhone & iPad
- **Offline Mode** — Tools tanpa internet
- **Widget** — Quick check dari home screen

### Target Metrics

| Metric | Target |
|--------|--------|
| Visitor/bulan | 5.000.000 |
| Registered users | 500.000 |
| Developer API key | 100.000 |
| Pro subscribers | 20.000 |
| Enterprise clients | 500 |
| Public DNS users | 1.000.000 |
| API request/hari | 10.000.000 |
| Indexed objects | 100.000.000+ |
| Search daily visitors | 500.000 |
| Search API users | 20.000 |
| B2B clients | 500 |
| Blockchain users | 20.000 |
| RPC requests/hari | 5.000.000 |

### Pendapatan

- Iklan
- Pro
- Team
- Enterprise
- API access
- DNS hosting
- BI reports
- Marketplace commissions
- Public DNS sponsorships
- Utility Search Pro
- Utility Search B2B
- Utility Search API
- Blockchain API access

---

## Evolusi Teknologi

| Tahun | Server | Database | Cache | Search | Queue | DNS | Blockchain | Infrastruktur |
|-------|--------|----------|-------|--------|-------|-----|------------|---------------|
| 2026 | 1 (4C/6GB) | SQLite → PG | Redis | — | — | External | — | AAPanel + Nginx |
| 2027 | 1 (upgrade) | PostgreSQL | Redis | PG FTS | APScheduler | External | — | + Auth + Crawler |
| 2028 | 2 servers | PostgreSQL | Redis | OpenSearch | Celery + Redis | DNS Hosting | Ethereum + 5 chains | + Docker Compose |
| 2029 | LB + 2 servers | PG Primary+Replica | Redis Cluster | OpenSearch Cluster | Celery + Redis Cluster | DNS Anycast | +10 chains | + Auto Scaling |
| 2030-31 | Multi Region | PG Multi Region | Redis Cluster | OpenSearch Multi Region | Celery + Redis Cluster | Public DNS | Full platform | Multi Region |

---

## Target Akhir Tahun ke-5 (2031)

### Produk

✅ 100+ Public Tools (Learn)
✅ Workspace — Domain, SSL, DNS, Server, Email Monitoring (Manage)
✅ Utility Search Engine — 100+ indexed vertical categories (Discover)
✅ Business Intelligence — Market Analysis, Technology Detection, Opportunity Finder (Discover)
✅ Blockchain Infrastructure — RPC, WebSocket, Multi-chain (Connect)
✅ Developer Platform — Utility API, Blockchain API (Connect)
✅ Public DNS (dns.konektivitas.com)
✅ Mobile App (Android + iOS)
✅ Enterprise features (SSO, Audit Log, SLA)
✅ Developer Marketplace

### Pengguna

| Segment | Target |
|---------|--------|
| Visitor/bulan | 5.000.000 |
| Registered users | 500.000 |
| Developer API key | 100.000 |
| Pro subscribers | 20.000 |
| Team subscribers | 5.000 |
| Enterprise clients | 500 |
| Public DNS users | 1.000.000 |
| Search daily visitors | 500.000 |
| Search API users | 20.000 |
| Indexed objects | 100.000.000+ |
| Blockchain users | 20.000 |

### Pendapatan

| Sumber | Status |
|--------|--------|
| Iklan | ✅ |
| Pro | ✅ |
| Team | ✅ |
| Enterprise | ✅ |
| API | ✅ |
| DNS Hosting | ✅ |
| Monitoring | ✅ |
| BI Reports | ✅ |
| Marketplace | ✅ |
| Utility Search Pro | ✅ |
| Utility Search B2B | ✅ |
| Utility Search API | ✅ |
| Blockchain API | ✅ |

---

## Filosofi Pengembangan

> "Kami tidak membuat aplikasi yang viral. Kami membangun utilitas yang akan tetap dibutuhkan selama internet masih ada."

### Framework Keputusan Fitur

Gunakan **dua framework** saat memutuskan fitur baru:

**Framework 1 — Arah Produk (4 Pertanyaan Pilar):**

Apakah fitur ini membantu pengguna memahami internet *(Learn)*, mengelola aset internetnya *(Manage)*, menemukan peluang *(Discover)*, atau menghubungkan infrastruktur *(Connect)*? Kalau tidak menjawab salah satunya, tolak.

**Framework 2 — Kelayakan Teknis (3 Syarat):**

1. **Ringan** dijalankan (sesuai spesifikasi server)
2. **Berguna** untuk banyak orang
3. **Masih relevan** 10 tahun ke depan

> Fitur harus lolos **kedua** framework sebelum diimplementasikan. Kalau lolos, produk akan tumbuh lebih lambat tetapi fondasinya jauh lebih kuat.

---

## Referensi

- [BRIEF.md](BRIEF.md) — Visi, misi, dan filosofi (Master Brief)
- [BRIEF2.md](BRIEF2.md) — Detail teknis dan arsitektur
- [BRIEF3.md](BRIEF3.md) — Brief Utility Search Engine
- [BRIEF4.md](BRIEF4.md) — Tech stack Utility Search Engine
- [FEATURES.md](FEATURES.md) — Daftar lengkap fitur per fase
- [AGENT.md](AGENT.md) — Panduan untuk AI/agent
- [plans/hub-konektivitas-plan.md](plans/hub-konektivitas-plan.md) — Rencana detail blockchain infrastructure
