Kalau melihat **visi produk kita** dan kondisi kamu yang solo + ingin hemat + awalnya cukup VPS, aku justru **tidak akan memakai stack yang terlalu berat**.

## 🧱 Stack yang aku pilih

```text
                    INTERNET
                       │
                       ▼
              ┌─────────────────┐
              │ Crawler Workers  │
              │ Python           │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Parser / Extract │
              │ Python           │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ PostgreSQL      │
              │ Structured Data │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Search Engine   │
              │ PostgreSQL FTS  │
              │ + pg_trgm       │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Python API      │
              │ FastAPI         │
              └────────┬────────┘
                       ▼
              ┌─────────────────┐
              │ Web Application │
              │ HTML + Tailwind │
              └─────────────────┘
```

### Backend: **Python + FastAPI**

Ini pilihan utama.

Kenapa?

Kita akan banyak bermain dengan:

* crawling
* parsing
* text processing
* data normalization
* scheduled jobs
* API
* data processing

Python sangat cocok.

Dan kamu sendiri sekarang memang lebih nyaman dengan Python dibanding Laravel.

---

# 🕷️ Crawler

### Python

Library yang bisa digunakan:

* `httpx` → HTTP requests
* `BeautifulSoup` / `selectolax` → parsing HTML
* `Playwright` → halaman yang membutuhkan browser
* `trafilatura` → extraction konten
* `urllib.robotparser` → robots.txt

Tapi **jangan langsung Playwright untuk semuanya**.

Urutannya:

```text
HTTP request
   ↓
HTML parsing
   ↓
Kalau gagal
   ↓
Browser rendering
```

Karena browser crawler jauh lebih berat.

---

# 🧠 Data Processing

Python worker:

```text
Raw HTML
 ↓
Extraction
 ↓
Cleaning
 ↓
Entity detection
 ↓
Normalization
 ↓
Deduplication
 ↓
Validation
 ↓
PostgreSQL
```

Contohnya:

```text
"Software Engineer"
"Backend Developer"
"Python Developer"
```

bisa dinormalisasi menjadi:

```text
occupation = software_engineering
specialization = backend
skill = python
```

Untuk awal **rule-based dulu**.

Jangan buru-buru AI.

---

# 🗄️ Database: PostgreSQL

Aku pilih **PostgreSQL**, bukan MongoDB.

Karena data kita akan sangat relational.

Misalnya:

```text
companies
jobs
skills
products
suppliers
tools
apis
sources
locations
categories
```

Relasinya penting.

Dan PostgreSQL sudah punya:

### Full Text Search

dan

### pg_trgm

untuk fuzzy matching.

Jadi MVP **belum perlu Elasticsearch/OpenSearch**.

---

# 🔎 Search

### Phase 1

**PostgreSQL**

```text
PostgreSQL
├── Full Text Search
├── pg_trgm
├── indexes
└── ranking
```

Sudah cukup.

Misalnya:

```text
search("python backend remote")
```

kita gabungkan:

```text
text relevance
+
freshness
+
availability
+
utility score
```

---

### Phase 2

Kalau datanya sudah jutaan/belasan juta objek:

**OpenSearch**

baru masuk.

```text
PostgreSQL
      │
      ├── Source of Truth
      │
      └── OpenSearch
              ↓
          Search
```

Jangan pasang OpenSearch dari hari pertama kalau belum perlu.

---

# ⚙️ Background Jobs

Ini penting karena crawler tidak boleh berjalan di request web.

Untuk awal:

### Celery + Redis

atau bahkan lebih sederhana:

### **APScheduler**

Misalnya:

```text
01:00 → crawl source A
02:00 → crawl source B
03:00 → verify expired jobs
04:00 → rebuild indexes
```

Kalau workload sudah besar:

```text
Celery
+
Redis
```

---

# 🌐 Frontend

Aku **tidak akan membuat React/Next.js dulu.**

Untuk MVP:

### FastAPI + Jinja2

atau bahkan:

### HTML + Tailwind + Alpine.js

Ini jauh lebih ringan.

Kita membuat pengalaman seperti search engine:

```text
Search
 ↓
Results
 ↓
Filter
 ↓
Detail
```

Tidak perlu SPA berat.

---

# 🎨 UI

### Tailwind CSS

*

### Alpine.js

Karena kebutuhan awal kita hanya:

* search
* filter
* sort
* pagination
* modal
* dropdown
* bookmark
* saved search

Alpine sudah cukup.

---

# 🔐 Authentication

Awal:

### Simple session / JWT

Kalau sudah subscription:

```text
User
 ├── Free
 ├── Pro
 ├── Business
 └── Developer
```

---

# 💳 Subscription

Ini **nanti**.

Karena kamu belum ingin mengeluarkan banyak biaya.

Untuk Indonesia bisa integrasi payment gateway ketika sudah siap secara legal/bisnis.

Untuk global nanti bisa pertimbangkan Stripe atau provider lain sesuai ketersediaan akun dan kebutuhan.

---

# 🚀 Deployment

Karena kamu sudah menggunakan **AAPanel**, bisa seperti:

```text
Ubuntu VPS
│
├── Nginx
│
├── FastAPI
│
├── PostgreSQL
│
├── Redis
│
├── Crawler workers
│
└── Cron
```

Gunakan:

### Docker Compose

supaya semua service mudah dikelola.

---

# ☁️ Storage

Raw HTML jangan semuanya disimpan selamanya.

Misalnya:

```text
Crawler
 ↓
HTML
 ↓
Extract
 ↓
Normalize
 ↓
PostgreSQL
```

Kalau perlu menyimpan raw snapshot:

**Object Storage**.

Tapi jangan membengkakkan storage VPS.

---

# 📊 Monitoring

Awal:

* application logs
* crawler logs
* PostgreSQL metrics
* disk monitoring

Nanti:

* Prometheus
* Grafana
* Sentry

Tidak perlu sekarang.

---

# 🧠 AI?

### **Tidak wajib.**

Ini justru salah satu bagian favoritku dari konsep ini.

MVP:

```text
Crawler
+
Rules
+
Parser
+
Database
+
Search
```

Sudah bisa berjalan.

AI baru digunakan ketika kita menemukan bagian yang memang sulit:

```text
HTML
 ↓
"Apakah ini lowongan?"
 ↓
AI classification
```

atau:

```text
"Software Engineer II"
"Backend Engineer"
"Python Developer"
        ↓
Entity normalization
```

Kalau nanti sudah ada revenue, baru kita pertimbangkan API AI atau model lokal.

---

# ⭐ Stack final yang menurutku paling cocok

| Komponen       | Teknologi                                |
| -------------- | ---------------------------------------- |
| Backend        | **Python**                               |
| API            | **FastAPI**                              |
| Web            | **Jinja2 + Tailwind + Alpine.js**        |
| Crawler        | **httpx + Selectolax/BeautifulSoup**     |
| Dynamic page   | **Playwright**                           |
| Parser         | **Trafilatura / custom parser**          |
| Database       | **PostgreSQL**                           |
| Search MVP     | **PostgreSQL FTS + pg_trgm**             |
| Queue awal     | **APScheduler**                          |
| Queue scale    | **Celery + Redis**                       |
| Reverse Proxy  | **Nginx**                                |
| Deployment     | **Docker Compose**                       |
| OS             | **Ubuntu**                               |
| Server panel   | **AAPanel**                              |
| Object Storage | **Wasabi/S3-compatible** jika diperlukan |
| AI             | **Tidak diperlukan untuk MVP**           |
| Search scale   | **OpenSearch nanti**                     |

---

## Dan yang paling penting:

**Jangan membangun crawler + search engine + 10 vertical sekaligus.**

Kita bikin **Core Engine**:

```text
                 CORE
                  │
       ┌──────────┼──────────┐
       ↓          ↓          ↓
    Crawler    Entity     Ranking
       │          │          │
       └──────────┼──────────┘
                  ↓
                INDEX
                  │
          ┌───────┼───────┐
          ↓       ↓       ↓
         JOB     TOOL    PRODUCT
```

Kemudian **vertical hanyalah modul**.

Jadi kalau kita mulai dari `jobs`, nanti tidak perlu rewrite sistem ketika ingin menambahkan `tools` atau `products`.

Dan untuk kondisi **solo developer + hanya sanggup membayar VPS**, stack ini menurutku sudah lebih dari cukup untuk membuktikan apakah **Utility Index** benar-benar punya value.
