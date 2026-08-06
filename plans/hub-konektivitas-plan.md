# Rencana Implementasi - Hub.konektivitas.com

> Tanggal: 2026-08-06
> Status: Menunggu Persetujuan

## Gambaran Umum

Hub.konektivitas.com adalah platform infrastruktur blockchain yang menyediakan akses node (RPC API) untuk developer, startup, perusahaan, dan aplikasi Web3.

## Arsitektur Sistem

```mermaid
flowchart TD
    Client[Client Apps] --> Nginx[Nginx Reverse Proxy]
    Nginx --> FastAPI[FastAPI Backend]
    FastAPI --> Auth[Auth Service]
    FastAPI --> RPC[RPC Proxy Service]
    FastAPI --> API[REST API Service]
    FastAPI --> WS[WebSocket Service]
    RPC --> Node1[Ethereum Node]
    RPC --> Node2[Polygon Node]
    RPC --> Node3[BSC Node]
    RPC --> NodeN[Other Nodes]
    Auth --> PostgreSQL[(PostgreSQL)]
    Auth --> Redis[(Redis Cache)]
    FastAPI --> Monitoring[Prometheus + Grafana]
    
    style Client fill:#4CAF50,color:#fff
    style FastAPI fill:#009688,color:#fff
    style PostgreSQL fill:#336791,color:#fff
    style Redis fill:#DC382D,color:#fff
```

## Struktur Direktori

```
hub-konektivitas/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app utama
│   ├── config.py               # Konfigurasi (Pydantic Settings)
│   ├── dependencies.py         # Dependency injection
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py             # API Key authentication
│   │   ├── rate_limit.py       # Rate limiting middleware
│   │   ├── logging.py          # Request logging middleware
│   │   └── cors.py             # CORS middleware
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── api_key.py          # API Key model
│   │   ├── usage.py            # Usage tracking model
│   │   └── blockchain.py       # Blockchain network model
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Login, Register, API Key management
│   │   ├── dashboard.py        # Dashboard endpoints
│   │   ├── rpc.py              # JSON-RPC proxy endpoints
│   │   ├── blockchain.py       # Blockchain data endpoints
│   │   ├── monitoring.py       # Status & health endpoints
│   │   └── admin.py            # Admin endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── api_key_service.py  # API Key CRUD
│   │   ├── rpc_service.py      # RPC proxy logic
│   │   ├── blockchain_service.py # Blockchain interactions
│   │   ├── usage_service.py    # Usage tracking
│   │   └── notification_service.py # Email/Telegram alerts
│   ├── utils/
│   │   ├── __init__.py
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
│   │   ├── docs.html           # API documentation
│   │   └── status.html         # System status page
│   └── static/
│       ├── css/style.css
│       ├── js/app.js
│       └── favicon.png
├── alembic/                    # Database migrations
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic.ini
└── .env.example
```

## Database Schema (PostgreSQL)

### Tabel Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    company VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    plan VARCHAR(50) DEFAULT 'free',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Tabel API Keys
```sql
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    key_prefix VARCHAR(10) NOT NULL,
    networks TEXT[] DEFAULT '{}',
    rate_limit INTEGER DEFAULT 100,
    is_active BOOLEAN DEFAULT true,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
);
```

### Tabel Usage Logs
```sql
CREATE TABLE usage_logs (
    id BIGSERIAL PRIMARY KEY,
    api_key_id UUID REFERENCES api_keys(id),
    network VARCHAR(50) NOT NULL,
    method VARCHAR(100) NOT NULL,
    request_size INTEGER,
    response_size INTEGER,
    response_time_ms INTEGER,
    status_code INTEGER,
    ip_address INET,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Tabel Blockchain Networks
```sql
CREATE TABLE blockchain_networks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL,
    chain_id INTEGER,
    rpc_endpoint TEXT NOT NULL,
    ws_endpoint TEXT,
    explorer_url TEXT,
    native_currency VARCHAR(10),
    is_active BOOLEAN DEFAULT true,
    node_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## API Endpoints

### Authentication
```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login
POST   /api/v1/auth/refresh           # Refresh token
GET    /api/v1/auth/me                 # Get current user
PUT    /api/v1/auth/me                 # Update profile
```

### API Keys
```
GET    /api/v1/keys                   # List API keys
POST   /api/v1/keys                   # Create API key
DELETE /api/v1/keys/{id}              # Revoke API key
PUT    /api/v1/keys/{id}              # Update API key
```

### RPC Proxy
```
POST   /rpc/{network}                 # JSON-RPC proxy
GET    /rpc/{network}/health          # Node health check
```

### Blockchain Data
```
GET    /api/v1/networks               # List supported networks
GET    /api/v1/networks/{slug}        # Network details
GET    /api/v1/{network}/block/{id}   # Get block
GET    /api/v1/{network}/tx/{hash}    # Get transaction
GET    /api/v1/{network}/address/{addr} # Get address info
GET    /api/v1/{network}/balance/{addr} # Get balance
POST   /api/v1/{network}/broadcast    # Broadcast transaction
```

### Monitoring
```
GET    /api/v1/status                 # System status
GET    /api/v1/status/{network}       # Network status
GET    /api/v1/usage                  # Usage statistics
GET    /api/v1/usage/daily            # Daily usage stats
```

## Fase 1 - MVP

### 1.1 Setup Infrastructure
- [ ] Setup PostgreSQL database
- [ ] Setup Redis
- [ ] Setup Docker environment
- [ ] Setup Alembic migrations

### 1.2 Authentication System
- [ ] User registration with email verification
- [ ] Login with JWT tokens
- [ ] Password hashing with bcrypt
- [ ] Session management

### 1.3 API Key Management
- [ ] Generate API keys with prefix
- [ ] Hash API keys for storage
- [ ] Rate limit per API key
- [ ] Network-specific permissions
- [ ] Key expiration

### 1.4 RPC Proxy
- [ ] JSON-RPC proxy for Ethereum
- [ ] Request validation
- [ ] Response caching (Redis)
- [ ] Rate limiting
- [ ] Request logging

### 1.5 Dashboard
- [ ] Usage statistics
- [ ] API key management UI
- [ ] Network status overview
- [ ] Billing information

### 1.6 Monitoring
- [ ] Health check endpoints
- [ ] Prometheus metrics
- [ ] Grafana dashboards
- [ ] Alerting rules

## Fase 2 - Multi Blockchain

### 2.1 Multi Chain Support
- [ ] Polygon (MATIC)
- [ ] Binance Smart Chain (BSC)
- [ ] Arbitrum
- [ ] Optimism
- [ ] Avalanche
- [ ] Solana (via RPC adapter)

### 2.2 Load Balancer
- [ ] Round-robin across nodes
- [ ] Health-based routing
- [ ] Failover handling

### 2.3 WebSocket
- [ ] WebSocket proxy for real-time events
- [ ] Subscription management
- [ ] Connection pooling

### 2.4 Analytics
- [ ] Detailed usage analytics
- [ ] Cost tracking
- [ ] Performance metrics

### 2.5 Billing
- [ ] Usage-based billing
- [ ] Plan management
- [ ] Invoice generation

## Fase 3 - Enterprise

### 3.1 Global Infrastructure
- [ ] Multi-region deployment
- [ ] Auto-scaling
- [ ] CDN for static assets

### 3.2 Enterprise Features
- [ ] SSO integration
- [ ] Audit logging
- [ ] SLA monitoring
- [ ] Custom rate limits

### 3.3 Marketplace
- [ ] Third-party node providers
- [ ] Revenue sharing
- [ ] Quality monitoring

## Teknologi Stack

| Komponen | Teknologi |
|----------|-----------|
| Backend | Python FastAPI |
| Database | PostgreSQL 15+ |
| Cache | Redis 7+ |
| Auth | JWT + API Keys |
| Proxy | Nginx |
| Container | Docker + Docker Compose |
| Orchestration | Traefik (optional) |
| Monitoring | Prometheus + Grafana |
| Migration | Alembic |
| Testing | Pytest |

## Konfigurasi Environment

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/hub_konektivitas

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
API_KEY_PREFIX=hk_
RATE_LIMIT_PER_MINUTE=100

# Blockchain Nodes
ETHEREUM_RPC_URL=https://eth.llamarpc.com
POLYGON_RPC_URL=https://polygon-rpc.com
BSC_RPC_URL=https://bsc-dataseed.binance.org

# Monitoring
PROMETHEUS_ENABLED=true
GRAFANA_ENABLED=true
```

## Integrasi dengan Konektivitas.com

Hub.konektivitas.com dapat diintegrasikan dengan Konektivitas.com melalui:

1. **Shared Authentication** - SSO antara kedua platform
2. **Cross-linking** - Link dari Konektivitas tools ke Hub
3. **Status Page** - Monitoring endpoint di Konektivitas
4. **DNS/SSL Tools** - Gunakan tools Konektivitas untuk manage DNS Hub

## Diagram Alur Request

```mermaid
sequenceDiagram
    participant C as Client
    participant N as Nginx
    participant A as FastAPI
    participant R as Redis
    participant P as PostgreSQL
    participant B as Blockchain Node
    
    C->>N: POST /rpc/ethereum
    N->>A: Forward request
    A->>A: Validate API Key
    A->>R: Check rate limit
    R-->>A: OK
    A->>R: Check cache
    alt Cache hit
        R-->>A: Cached response
    else Cache miss
        A->>B: JSON-RPC call
        B-->>A: Response
        A->>R: Store in cache
    end
    A->>P: Log usage
    A-->>N: Response
    N-->>C: JSON-RPC response
```

## Catatan Penting

1. **Database Migration**: Menggunakan PostgreSQL, bukan SQLite. Perlu setup migration dengan Alembic.
2. **Security**: API keys harus di-hash sebelum disimpan. Gunakan bcrypt atau SHA-256.
3. **Rate Limiting**: Per-API-key, bukan per-IP (berbeda dengan Konektivitas.com).
4. **Caching**: Cache RPC responses untuk mengurangi beban node.
5. **Monitoring**: Penting untuk memantau kesehatan node dan performa API.
