# Agent Guide - Konektivitas.com

> Panduan untuk AI/agent agar mudah memahami dan mengerjakan proyek Konektivitas.com.

## Overview

**Konektivitas.com** adalah platform utilitas internet Indonesia yang menyediakan layanan dasar internet gratis, cepat, dan ringan. Bukan website tools, tetapi fondasi internet.

**Tagline:** Infrastruktur Internet Gratis untuk Indonesia

## Struktur Proyek

```
konek-internet/
├── BRIEF.md           # Brief proyek (visi, misi, target)
├── BRIEF2.md          # Detail teknis & arsitektur
├── ROADMAP.md         # Roadmap 5 tahun (2026-2031)
├── FEATURES.md        # Daftar lengkap fitur per fase
├── AGENT.md           # Dokumen ini
└── [Source Code]      # Akan ditambahkan saat implementasi
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

## Konvensi Penamaan

### URL Pattern
```
/dns-lookup
/whois-lookup
/ip-lookup
/ssl-checker
/ping-checker
```

### API Pattern
```
/api/dns/{domain}
/api/ip/{ip_address}
/api/whois/{domain}
/api/ssl/{domain}
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
├── main.py           # FastAPI app
├── routers/          # API endpoints
│   ├── dns.py
│   ├── domain.py
│   ├── ssl.py
│   ├── website.py
│   └── ip.py
├── services/         # Business logic
│   ├── dns_service.py
│   ├── whois_service.py
│   └── ssl_service.py
├── models/           # Data models
├── utils/            # Helper functions
└── config.py         # Configuration
```

### Naming Convention
- **File:** snake_case.py
- **Function:** snake_case()
- **Class:** PascalCase
- **Variable:** snake_case
- **Constant:** UPPER_SNAKE_CASE
- **API Endpoint:** kebab-case (/dns-lookup)

### Performance Checklist
- [ ] Response time < 1 detik
- [ ] Memory usage < 100MB per request
- [ ] No heavy dependencies
- [ ] Redis cache untuk data yang sering diakses
- [ ] Graceful error handling

### SEO Checklist
- [ ] Meta title & description
- [ ] Open Graph tags
- [ ] Structured data (JSON-LD)
- [ ] Fast loading time
- [ ] Mobile friendly

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