# Rencana Teknis: Fase 2 — Developer Platform & Workspace MVP

> Arsitektur detail, database schema, API design, dan implementation plan untuk Fase 2.

---

## Daftar Isi

1. [Overview](#overview)
2. [Arsitektur](#arsitektur)
3. [Database Schema](#database-schema)
4. [Autentikasi & API Keys](#autentikasi--api-keys)
5. [API Endpoints](#api-endpoints)
6. [File Structure](#file-structure)
7. [Dependencies Baru](#dependencies-baru)
8. [Implementation Order](#implementation-order)
9. [Configuration](#configuration)

---

## Overview

Fase 2 menambahkan tiga komponen utama ke platform:

1. **User Authentication & API Keys** — Sistem autentikasi JWT + API key management
2. **Workspace MVP** — Domain management, SSL/DNS/Uptime monitoring
3. **Notification System** — Email, Telegram, Discord alerts

### Scope Fase 2 (MVP Only)

| Komponen | Include | Exclude (Fase 3+) |
|----------|---------|-------------------|
| Auth | Register, Login, JWT, Password Reset | Google OAuth, SSO |
| API Keys | Create, List, Delete, Rate Limit | Custom rate limit, Enterprise keys |
| Domain Mgmt | Add, List, Details, Notes, Bulk Import | Team sharing |
| SSL Monitoring | Status check, Expiry alert, History | Certificate Transparency |
| DNS Monitoring | Records check, Change detection, History | DNS Hosting, Zone Editor |
| Uptime Monitoring | HTTP check every 5min, Response time | Multi-URL, Keyword monitoring |
| Notifications | Email, Telegram, Discord | SMS, Custom webhook |
| Dashboard | Overview, Health score, Activity | Custom reports, PDF export |

---

## Arsitektur

### Arsitektur Fase 2

```
Internet
      │
  Cloudflare
      │
   AAPanel / Nginx
      │
  FastAPI (Python)
      │
  ┌───┴───┐
  │       │
 Redis   PostgreSQL
(Cache)  (Auth, Workspace, Monitoring)
  │       │
  └───┬───┘
      │
  APScheduler (Background Jobs)
      │
  ┌───┼───┬───┐
  │   │   │   │
SSL DNS Uptime Notify
Check Check Check
```

### Alur Autentikasi

```
Client
  │
  ├─ Public Tools → No auth needed → Rate limit 60/min per IP
  │
  ├─ Register/Login → FastAPI Auth → JWT Token → Client
  │
  ├─ API Key Request → Validate JWT → Create API Key (kn_xxx) → Client
  │
  └─ Authenticated Request → Validate JWT or API Key → Workspace API → Response
```

### Alur Monitoring

```
APScheduler (cron)
      │
  ┌───┼───┬───┐
  │   │   │   │
SSL DNS Uptime Domain
Check Check Check Check
  │   │   │   │
  │   │   │   └──→ Check domain expiry
  │   │   └──────→ HTTP GET, check status + response time
  │   └──────────→ Compare DNS records with stored snapshot
  └──────────────→ Check SSL certificate expiry
      │
  Store results in PostgreSQL
      │
  Check alert conditions
      │
  ┌───┼───┬───┐
  │   │   │   │
Email TG  DC  Webhook
```

---

## Database Schema

### Entity Relationship Diagram

```mermaid
erDiagram
    users ||--o{ api_keys : has
    users ||--o{ monitored_domains : owns
    monitored_domains ||--o{ domain_ssl_history : has
    monitored_domains ||--o{ domain_dns_history : has
    monitored_domains ||--o{ uptime_checks : has
    uptime_checks ||--o{ uptime_logs : has
    users ||--o{ notification_settings : configures

    users {
        int id PK
        string email UK
        string username UK
        string password_hash
        string display_name
        bool is_verified
        bool is_active
        string plan
        timestamp created_at
        timestamp updated_at
        timestamp last_login
    }

    api_keys {
        int id PK
        int user_id FK
        string key_prefix
        string key_hash
        string name
        string permissions
        int rate_limit
        bool is_active
        timestamp created_at
        timestamp last_used_at
        timestamp expires_at
    }

    monitored_domains {
        int id PK
        int user_id FK
        string domain
        string notes
        string status
        bool monitor_ssl
        bool monitor_dns
        bool monitor_uptime
        int check_interval_minutes
        timestamp created_at
        timestamp updated_at
        timestamp last_checked_at
    }

    domain_ssl_history {
        int id PK
        int domain_id FK
        string issuer
        string subject
        string serial_number
        date valid_from
        date valid_until
        string san_list
        string protocol_version
        string key_type
        int key_size
        string signature_algorithm
        bool is_valid
        int days_remaining
        timestamp checked_at
    }

    domain_dns_history {
        int id PK
        int domain_id FK
        string record_type
        string record_value
        int ttl
        string previous_value
        bool has_changed
        timestamp checked_at
    }

    uptime_checks {
        int id PK
        int domain_id FK
        string url
        string method
        int expected_status
        int timeout_seconds
        bool is_active
        timestamp created_at
    }

    uptime_logs {
        int id PK
        int check_id FK
        bool is_up
        int status_code
        int response_time_ms
        string error_message
        string checked_from
        timestamp checked_at
    }

    notification_settings {
        int id PK
        int user_id FK
        string channel
        bool is_enabled
        string config_json
        timestamp created_at
        timestamp updated_at
    }
```

### Table Definitions

#### 1. users

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    plan VARCHAR(20) DEFAULT 'free',  -- free, pro, team, enterprise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

#### 2. api_keys

```sql
CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    key_prefix VARCHAR(10) NOT NULL,   -- 'kn_' + first 8 chars
    key_hash VARCHAR(255) NOT NULL,     -- bcrypt hash of full key
    name VARCHAR(100) NOT NULL,
    permissions VARCHAR(255) DEFAULT 'read',  -- read, write, admin
    rate_limit INTEGER DEFAULT 120,     -- requests per minute
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    expires_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_api_keys_prefix ON api_keys(key_prefix);
CREATE INDEX idx_api_keys_user ON api_keys(user_id);
```

#### 3. monitored_domains

```sql
CREATE TABLE monitored_domains (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    domain VARCHAR(255) NOT NULL,
    notes TEXT,
    status VARCHAR(20) DEFAULT 'active',  -- active, paused, error
    monitor_ssl BOOLEAN DEFAULT TRUE,
    monitor_dns BOOLEAN DEFAULT TRUE,
    monitor_uptime BOOLEAN DEFAULT TRUE,
    check_interval_minutes INTEGER DEFAULT 60,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_checked_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, domain)
);

CREATE INDEX idx_domains_user ON monitored_domains(user_id);
CREATE INDEX idx_domains_status ON monitored_domains(status);
```

#### 4. domain_ssl_history

```sql
CREATE TABLE domain_ssl_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL,
    issuer VARCHAR(255),
    subject VARCHAR(255),
    serial_number VARCHAR(255),
    valid_from DATE,
    valid_until DATE,
    san_list TEXT,                    -- comma-separated SANs
    protocol_version VARCHAR(20),     -- TLSv1.2, TLSv1.3
    key_type VARCHAR(10),             -- RSA, ECDSA
    key_size INTEGER,
    signature_algorithm VARCHAR(50),
    is_valid BOOLEAN,
    days_remaining INTEGER,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES monitored_domains(id) ON DELETE CASCADE
);

CREATE INDEX idx_ssl_domain ON domain_ssl_history(domain_id);
CREATE INDEX idx_ssl_checked ON domain_ssl_history(checked_at);
```

#### 5. domain_dns_history

```sql
CREATE TABLE domain_dns_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL,
    record_type VARCHAR(10) NOT NULL,  -- A, AAAA, MX, CNAME, TXT, NS
    record_value TEXT NOT NULL,
    ttl INTEGER,
    previous_value TEXT,               -- NULL if first check
    has_changed BOOLEAN DEFAULT FALSE,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES monitored_domains(id) ON DELETE CASCADE
);

CREATE INDEX idx_dns_domain ON domain_dns_history(domain_id);
CREATE INDEX idx_dns_checked ON domain_dns_history(checked_at);
```

#### 6. uptime_checks

```sql
CREATE TABLE uptime_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id INTEGER NOT NULL,
    url VARCHAR(500) NOT NULL,
    method VARCHAR(10) DEFAULT 'GET',
    expected_status INTEGER DEFAULT 200,
    timeout_seconds INTEGER DEFAULT 10,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (domain_id) REFERENCES monitored_domains(id) ON DELETE CASCADE
);

CREATE INDEX idx_uptime_domain ON uptime_checks(domain_id);
```

#### 7. uptime_logs

```sql
CREATE TABLE uptime_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    check_id INTEGER NOT NULL,
    is_up BOOLEAN NOT NULL,
    status_code INTEGER,
    response_time_ms INTEGER,
    error_message TEXT,
    checked_from VARCHAR(50),          -- server location
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (check_id) REFERENCES uptime_checks(id) ON DELETE CASCADE
);

CREATE INDEX idx_uptime_check ON uptime_logs(check_id);
CREATE INDEX idx_uptime_checked ON uptime_logs(checked_at);
```

#### 8. notification_settings

```sql
CREATE TABLE notification_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel VARCHAR(20) NOT NULL,      -- email, telegram, discord
    is_enabled BOOLEAN DEFAULT FALSE,
    config_json TEXT,                   -- channel-specific config
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, channel)
);

CREATE INDEX idx_notif_user ON notification_settings(user_id);
```

---

## Autentikasi & API Keys

### JWT Authentication

#### Token Structure

```json
{
  "sub": "user_id",
  "email": "user@example.com",
  "username": "user123",
  "plan": "free",
  "exp": 1234567890,
  "iat": 1234567890
}
```

#### Configuration

```python
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7
```

#### Auth Flow

```
Register:
  POST /api/v1/auth/register
  → Validate input → Check duplicate → Hash password → Create user → Return tokens

Login:
  POST /api/v1/auth/login
  → Validate input → Find user → Verify password → Update last_login → Return tokens

Refresh:
  POST /api/v1/auth/refresh
  → Validate refresh token → Generate new access token → Return token

Protected Route:
  Authorization: Bearer <access_token>
  → Validate token → Extract user → Attach to request → Process
```

### API Key System

#### Key Format

```
kn_ + 32 random characters (alphanumeric)
Example: kn_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
```

#### Key Generation

```python
import secrets
import hashlib

def generate_api_key():
    """Generate a new API key with kn_ prefix."""
    random_part = secrets.token_urlsafe(24)[:32]
    full_key = f"kn_{random_part}"
    key_hash = hashlib.sha256(full_key.encode()).hexdigest()
    key_prefix = full_key[:12]  # kn_abcdefgh (first 12 chars)
    return full_key, key_hash, key_prefix
```

#### Key Validation

```
X-API-Key: kn_a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
→ Extract prefix → Find key by prefix → Verify hash → Check is_active → Check expires_at → Attach user
```

---

## API Endpoints

### Authentication Endpoints

```
POST   /api/v1/auth/register        — Register new user
POST   /api/v1/auth/login           — Login with email/password
POST   /api/v1/auth/refresh         — Refresh access token
POST   /api/v1/auth/logout          — Invalidate refresh token
GET    /api/v1/auth/me              — Get current user profile
PUT    /api/v1/auth/me              — Update profile
POST   /api/v1/auth/forgot-password — Request password reset
POST   /api/v1/auth/reset-password  — Reset password with token
POST   /api/v1/auth/verify-email    — Verify email address
```

### API Key Endpoints

```
GET    /api/v1/keys                 — List user's API keys
POST   /api/v1/keys                 — Create new API key (returns full key once)
DELETE /api/v1/keys/{key_id}        — Revoke API key
GET    /api/v1/keys/{key_id}/usage  — Get key usage stats
```

### Workspace Endpoints

```
# Domain Management
GET    /api/v1/workspace/domains           — List monitored domains
POST   /api/v1/workspace/domains           — Add domain to monitor
GET    /api/v1/workspace/domains/{id}      — Get domain details
PUT    /api/v1/workspace/domains/{id}      — Update domain settings
DELETE /api/v1/workspace/domains/{id}      — Remove domain
POST   /api/v1/workspace/domains/import    — Bulk import domains

# SSL Monitoring
GET    /api/v1/workspace/domains/{id}/ssl        — Get latest SSL status
GET    /api/v1/workspace/domains/{id}/ssl/history — Get SSL history

# DNS Monitoring
GET    /api/v1/workspace/domains/{id}/dns        — Get latest DNS records
GET    /api/v1/workspace/domains/{id}/dns/history — Get DNS change history

# Uptime Monitoring
GET    /api/v1/workspace/domains/{id}/uptime        — Get uptime status
GET    /api/v1/workspace/domains/{id}/uptime/history — Get uptime logs
POST   /api/v1/workspace/domains/{id}/uptime/check   — Manual uptime check

# Dashboard
GET    /api/v1/workspace/dashboard          — Overview stats
GET    /api/v1/workspace/activity           — Recent activity
```

### Notification Endpoints

```
GET    /api/v1/notifications/settings       — Get notification settings
PUT    /api/v1/notifications/settings       — Update notification settings
POST   /api/v1/notifications/test           — Send test notification
GET    /api/v1/notifications/history        — Notification history
```

---

## File Structure

### New Files (Phase 2)

```
app/
├── __init__.py
├── main.py                    # UPDATED — include new routers
├── config.py                  # UPDATED — add JWT, DB settings
├── database.py                # NEW — SQLAlchemy engine & session
├── dependencies.py            # NEW — FastAPI dependencies (get_db, get_current_user)
├── models/                    # NEW — SQLAlchemy ORM models
│   ├── __init__.py
│   ├── base.py                # Base declarative model
│   ├── user.py                # User model
│   ├── api_key.py             # API Key model
│   ├── monitored_domain.py    # Monitored Domain model
│   ├── ssl_history.py         # SSL History model
│   ├── dns_history.py         # DNS History model
│   ├── uptime_check.py        # Uptime Check model
│   ├── uptime_log.py          # Uptime Log model
│   └── notification.py        # Notification Settings model
├── routers/                   # UPDATED — add new routers
│   ├── __init__.py
│   ├── auth.py                # NEW — Auth endpoints
│   ├── keys.py                # NEW — API Key endpoints
│   ├── workspace.py           # NEW — Domain management endpoints
│   ├── monitoring.py          # NEW — SSL/DNS/Uptime monitoring endpoints
│   ├── notifications.py       # NEW — Notification settings endpoints
│   ├── dns.py                 # EXISTING
│   ├── domain.py              # EXISTING
│   ├── ssl.py                 # EXISTING
│   ├── website.py             # EXISTING
│   ├── ip.py                  # EXISTING
│   ├── cdn.py                 # EXISTING
│   ├── batch.py               # EXISTING
│   └── compare.py             # EXISTING
├── services/                  # UPDATED — add new services
│   ├── __init__.py
│   ├── auth_service.py        # NEW — Auth logic (register, login, JWT)
│   ├── api_key_service.py     # NEW — API key management
│   ├── workspace_service.py   # NEW — Domain management
│   ├── monitoring_service.py  # NEW — SSL/DNS/Uptime monitoring
│   ├── scheduler_service.py   # NEW — APScheduler background jobs
│   ├── notification_service.py # NEW — Email/Telegram/Discord
│   ├── ssl_service.py         # EXISTING (shared with public tools)
│   ├── dns_service.py         # EXISTING (shared with public tools)
│   ├── website_service.py     # EXISTING (shared with public tools)
│   └── ...
├── templates/                 # UPDATED — add dashboard templates
│   ├── base.html              # EXISTING
│   ├── base_dashboard.html    # NEW — Dashboard base layout
│   ├── auth/
│   │   ├── login.html         # NEW
│   │   ├── register.html      # NEW
│   │   ├── forgot_password.html # NEW
│   │   └── reset_password.html  # NEW
│   └── dashboard/
│       ├── overview.html      # NEW — Dashboard home
│       ├── domains.html       # NEW — Domain list
│       ├── domain_detail.html # NEW — Domain detail + monitoring
│       ├── api_keys.html      # NEW — API key management
│       ├── notifications.html # NEW — Notification settings
│       └── profile.html       # NEW — User profile
├── static/
│   └── css/
│       └── dashboard.css     # NEW — Dashboard-specific styles
└── utils/
    ├── __init__.py
    ├── security.py            # NEW — Password hashing, JWT encode/decode
    ├── cache.py               # EXISTING
    ├── rate_limit.py          # EXISTING
    └── validators.py          # EXISTING

alembic/                       # NEW — Database migrations
├── alembic.ini
├── env.py
├── script.py.mako
└── versions/
    └── 001_initial.py         # Initial migration
```

---

## Dependencies Baru

### requirements.txt Updates

```
# Existing (keep)
fastapi==0.104.1
uvicorn[standard]==0.24.0
jinja2==3.1.2
aiofiles==23.2.1
dnspython==2.4.2
python-whois==0.9.4
httpx==0.25.2
redis==5.0.1
pydantic==2.5.3
python-multipart==0.0.6
cryptography>=41.0.0

# NEW for Fase 2
sqlalchemy==2.0.23           # ORM & database
alembic==1.13.0              # Database migrations
python-jose[cryptography]==3.3.0  # JWT encode/decode
passlib[bcrypt]==1.7.4       # Password hashing
bcrypt==4.1.2                # bcrypt backend
aiosqlite==0.19.0            # Async SQLite support
```

### Optional (for notifications)

```
# Email — built-in smtplib (no extra dependency)
# Telegram — httpx (already included)
# Discord — httpx (already included, webhook-based)
```

---

## Implementation Order

### Phase 2.1 — Database Foundation

1. Add new dependencies to requirements.txt
2. Create `app/database.py` — SQLAlchemy async engine + session factory
3. Create `app/models/base.py` — Base declarative model
4. Create all ORM models (user, api_key, monitored_domain, etc.)
5. Create `app/dependencies.py` — get_db dependency
6. Setup Alembic for migrations
7. Create initial migration
8. Run migration to create tables

### Phase 2.2 — Authentication System

1. Create `app/utils/security.py` — Password hashing + JWT utilities
2. Create `app/services/auth_service.py` — Auth business logic
3. Create `app/routers/auth.py` — Auth API endpoints
4. Create auth templates (login, register, forgot/reset password)
5. Create `app/dependencies.py` — get_current_user dependency
6. Update main.py to include auth router

### Phase 2.3 — API Key System

1. Create `app/services/api_key_service.py` — Key management logic
2. Create `app/routers/keys.py` — Key API endpoints
3. Update rate limiting to support API key rate limits
4. Create API key management template

### Phase 2.4 — Workspace & Domain Management

1. Create `app/services/workspace_service.py` — Domain management logic
2. Create `app/routers/workspace.py` — Domain CRUD endpoints
3. Create domain management templates

### Phase 2.5 — Monitoring System

1. Create `app/services/monitoring_service.py` — SSL/DNS/Uptime check logic
2. Create `app/routers/monitoring.py` — Monitoring endpoints
3. Create `app/services/scheduler_service.py` — APScheduler setup
4. Integrate monitoring with existing ssl_service, dns_service, website_service

### Phase 2.6 — Notification System

1. Create `app/services/notification_service.py` — Email/Telegram/Discord
2. Create `app/routers/notifications.py` — Notification settings endpoints
3. Create notification templates

### Phase 2.7 — Dashboard

1. Create `app/templates/base_dashboard.html` — Dashboard layout
2. Create dashboard templates (overview, domains, keys, etc.)
3. Create `app/static/css/dashboard.css` — Dashboard styles
4. Update `app/templates/base.html` — Add login/register links

### Phase 2.8 — Integration & Testing

1. Update main.py with all new routers
2. Update config.py with new settings
3. Test all auth flows
4. Test workspace CRUD
5. Test monitoring checks
6. Test notifications
7. Update AGENT.md with new structure

---

## Configuration

### New Environment Variables

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./konektivitas.db
# DATABASE_URL=postgresql+asyncpg://user:pass@localhost/konektivitas

# JWT
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@konektivitas.com

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_DEFAULT_CHAT_ID=your-chat-id

# Discord Webhook
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx/yyy
```

### Config.py Updates

```python
class Settings(BaseModel):
    # ... existing fields ...

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./konektivitas.db")

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    # SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    SMTP_FROM: str = os.getenv("SMTP_FROM", "noreply@konektivitas.com")

    # Telegram
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_DEFAULT_CHAT_ID: str = os.getenv("TELEGRAM_DEFAULT_CHAT_ID", "")

    # Discord
    DISCORD_WEBHOOK_URL: str = os.getenv("DISCORD_WEBHOOK_URL", "")
```

---

## Key Design Decisions

### 1. SQLite First, PostgreSQL Later

Menggunakan SQLite untuk MVP karena:
- Tidak perlu setup database server
- File-based, mudah di-deploy
- Async support via aiosqlite
- Migration ke PostgreSQL tinggal ganti connection string

### 2. Shared Services

Monitoring services (SSL, DNS, Uptime) akan **reuse** service yang sudah ada:
- `ssl_service.py` — Sudah ada, tinggal tambah logging ke DB
- `dns_service.py` — Sudah ada, tinggal tambah perbandingan
- `website_service.py` — Sudah ada untuk HTTP check

### 3. APScheduler for Background Jobs

Menggunakan APScheduler (lightweight) bukan Celery karena:
- Lebih ringan, tidak perlu broker
- Cukup untuk MVP (< 1000 domains)
- Bisa upgrade ke Celery nanti

### 4. JWT + Refresh Token

Access token singkat (30 min) untuk keamanan:
- Access token: 30 menit
- Refresh token: 7 hari
- Simpan refresh token di httpOnly cookie

### 5. API Key via Header

```
X-API-Key: kn_xxxxxxxxxxxxxxxx
```
Bukan di query parameter karena lebih aman (tidak log di server logs).

---

> "Bangun fondasi yang kuat. Scale nanti."
