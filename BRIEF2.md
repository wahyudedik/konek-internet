# Brief Teknis: Konektivitas.com

> Detail teknis, arsitektur, dan infrastruktur untuk mendukung visi platform infrastruktur internet Indonesia.

---

## Arsitektur Teknis

### Arsitektur Fase 1 (2026) — Public Tools

```
Internet
      │
  Cloudflare (Proxy + Cache + WAF)
      │
   AAPanel
      │
    Nginx
      │
  FastAPI (Python)
      │
    Redis (Cache)
      │
  SQLite → PostgreSQL (2027)
```

### Arsitektur Fase 3-5 (2028-2031) — Platform

```
Internet
      │
  Cloudflare (Proxy + Cache + WAF)
      │
   Load Balancer (2029)
      │
  ┌───┴───┐
  │       │
Server  Server  (Multi Region 2030)
  │       │
  Nginx   Nginx
  │       │
FastAPI  FastAPI
  │       │
  Redis Cluster
  │       │
PostgreSQL (Primary + Replica)
  │
Scheduler (Cron) — Monitoring, Notifikasi
```

### Stack Teknologi

| Komponen | 2026 | 2027 | 2028 | 2029 | 2030-2031 |
|----------|------|------|------|------|-----------|
| **Web Server** | Nginx (AAPanel) | Nginx | Nginx | Nginx | Nginx |
| **Backend** | FastAPI | FastAPI | FastAPI | FastAPI | FastAPI |
| **Cache** | Redis | Redis | Redis | Redis Cluster | Redis Cluster |
| **Database** | SQLite | PostgreSQL | PostgreSQL | PostgreSQL | PostgreSQL |
| **Server** | 1 server | 1 server | 2 server | Load Balancer | Multi Region |
| **DNS** | External | External | DNS Anycast | DNS Anycast | DNS Anycast |

### Target Server (Fase 1)

- 4 Core CPU
- RAM 6 GB
- SSD 100 GB
- Ubuntu + AAPanel

---

## Yang Dijalankan di Server

### Fase 1 (2026)

- Nginx (via AAPanel)
- FastAPI (Python)
- Redis (Cache)
- SQLite → PostgreSQL
- Scheduler (cron) untuk monitoring

### Yang TIDAK Perlu

- ❌ Docker (di awal)
- ❌ Kubernetes
- ❌ Elasticsearch
- ❌ RabbitMQ
- ❌ Microservice

> Semakin sederhana, semakin mudah dirawat.

---

## Target Performa

| Metric | Target |
|--------|--------|
| Response time | < 1 detik |
| Memory per request | < 100MB |
| Uptime | 99.9% |
| Cache hit rate | > 80% |
| Rate limit | 60 req/menit per IP |

---

## Alur Request

```
User → Cloudflare → Nginx → FastAPI → Redis (cache check)
                                            │
                                      Cache HIT → Response
                                      Cache MISS → Service → External API → Cache → Response
```

---

## Data Flow per Produk

### Public Tools (Gratis)

```
User → Tool Page → API Endpoint → Service → External DNS/WHOIS/SSL/IP API
                                                    │
                                              Response → Cache → User
```

Tidak ada penyimpanan data. Semua transient.

### Workspace (Premium)

```
User → Dashboard → API Endpoint → Service → Database (PostgreSQL)
                                                    │
                                          Monitoring → Scheduler → Notifikasi
```

Penyimpanan:
- Domain yang dimonitor
- Status SSL/history
- DNS records
- Uptime logs
- Notifikasi settings
- Team members

### Business Intelligence (Enterprise)

```
User → BI Dashboard → Query Engine → Aggregated Data
                                            │
                                      Public Data Analysis → Insight Reports
```

Penyimpanan:
- Aggregated statistics
- Market analysis data
- Trend reports
- Custom reports

---

## Monitoring Architecture

### Fase 2 (2027) — Monitoring Services

```
Scheduler (Cron)
      │
  ┌───┼───┬───┬───┐
  │   │   │   │   │
SSL DNS Uptime Email Domain
Check Check Check Check Check
  │   │   │   │   │
  └───┼───┴───┴───┘
      │
  Notification Service
      │
  ┌───┼───┬───┐
  │   │   │   │
Email Telegram Discord Webhook
```

### Monitoring Intervals

| Check Type | Free | Premium | Enterprise |
|------------|------|---------|------------|
| SSL Expiry | Weekly | Daily | Real-time |
| DNS Change | - | Daily | Hourly |
| Uptime | - | 5 min | 1 min |
| Domain Expiry | - | Weekly | Daily |

---

## Notification System

### Channels

- Email
- Telegram Bot
- Discord Webhook
- Custom Webhook
- SMS (Enterprise)

### Alert Types

- SSL certificate expiring (< 30 days)
- DNS record changed
- Website down
- Domain expiring
- Blacklist detection
- Custom thresholds

---

## Database Schema (Fase 2+)

### Core Tables

```sql
-- Users & Auth
users
user_sessions
teams
team_members

-- Workspace
monitored_domains
domain_ssl_history
domain_dns_history
uptime_checks
uptime_logs
notification_settings

-- BI (Fase 4)
market_statistics
trend_reports
regional_data
```

---

## API Evolution

### Fase 1 — Public API (2026)

```
GET /api/v1/dns/{domain}
GET /api/v1/whois/{domain}
GET /api/v1/ssl/{domain}
GET /api/v1/ip/{ip}
... (25+ endpoints)
```

Gratis dengan rate limit 60 req/menit.

### Fase 2 — API Key (2027)

```
X-API-Key: xxxxx
GET /api/v2/dns/{domain}
GET /api/v2/monitoring/status
GET /api/v2/workspace/domains
```

Rate limit naik untuk API key holders.

### Fase 3 — Enterprise API (2029)

```
X-API-Key: enterprise_xxxxx
GET /api/v3/dns/{domain}
GET /api/v3/analytics/overview
GET /api/v3/intelligence/market
```

Custom rate limit, SLA, dedicated support.

---

## Security Architecture

### Layer 1 — Edge

- Cloudflare WAF
- DDoS protection
- Bot management

### Layer 2 — Application

- Security headers (X-Content-Type-Options, X-Frame-Options, X-XSS-Protection)
- Rate limiting (60 req/min per IP)
- Input validation
- CSRF protection

### Layer 3 — Data

- Encrypted at rest (PostgreSQL)
- Encrypted in transit (HTTPS/HSTS)
- No sensitive data in public tools
- GDPR-ready data handling

---

## Scalability Plan

| Year | Users | Servers | Database | Cache |
|------|-------|---------|----------|-------|
| 2026 | 100K visitors/mo | 1 (4C/6GB) | SQLite → PG | Redis |
| 2027 | 500K visitors/mo | 1 (upgrade) | PostgreSQL | Redis |
| 2028 | 1M visitors/mo | 2 servers | PostgreSQL | Redis |
| 2029 | 3M visitors/mo | LB + 2 servers | PG Primary+Replica | Redis Cluster |
| 2030-31 | 5M visitors/mo | Multi Region | PG Multi Region | Redis Cluster |

---

## Referensi

- [BRIEF.md](BRIEF.md) — Visi, misi, dan filosofi
- [ROADMAP.md](ROADMAP.md) — Roadmap pengembangan 5 tahun
- [FEATURES.md](FEATURES.md) — Daftar lengkap fitur per fase
- [AGENT.md](AGENT.md) — Panduan untuk AI/agent

---

> "Semakin sederhana, semakin mudah dirawat. Semakin kuat fondasinya, semakin lama produknya bertahan."
