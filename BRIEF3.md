# Brief Produk — **Utility Search Engine**

### *Search the internet for what you can actually use.*

## 1. Visi

Membangun mesin pencarian vertikal yang tidak berusaha mengindeks seluruh internet seperti Google, tetapi **mengindeks hal-hal yang benar-benar berguna untuk melakukan pekerjaan, menjalankan bisnis, mencari peluang, mendapatkan sesuatu, membangun sesuatu, dan menghasilkan uang.**

Prinsip utama:

> **Google membantu menemukan informasi.
> Utility Search membantu menemukan sesuatu yang bisa dilakukan atau digunakan.**

Tujuan akhirnya adalah menjadi **lapisan utility di atas internet** yang dapat digunakan oleh manusia, bisnis, dan developer.

---

# 2. Masalah

Internet memiliki jumlah informasi yang sangat besar, tetapi informasi tersebut tersebar di berbagai:

* website
* marketplace
* career page
* halaman perusahaan
* dokumentasi
* direktori
* tools
* API
* katalog
* supplier
* platform freelance
* program affiliate
* event
* dan sumber publik lainnya.

Masalahnya bukan lagi:

> "Apakah informasinya ada?"

Tetapi:

> **"Di mana saya menemukan sesuatu yang benar-benar bisa membantu saya melakukan pekerjaan ini?"**

Search engine umum menghasilkan banyak halaman.

Utility Search harus menghasilkan **pilihan yang dapat ditindaklanjuti.**

---

# 3. Konsep Utama

Platform melakukan:

```text
PUBLIC INTERNET
       ↓
   DISCOVERY
       ↓
     CRAWL
       ↓
 DATA EXTRACTION
       ↓
   NORMALIZATION
       ↓
  VALIDATION
       ↓
   UTILITY INDEX
       ↓
 FILTER + RANKING
       ↓
    SEARCH
```

Platform tidak mengharuskan pemilik website:

* memasang script
* memasang SDK
* mendaftarkan website
* melakukan submission manual

**Discovery harus sebisa mungkin berjalan otomatis dari sumber publik yang dapat diindeks secara sah.**

Submission/claim dapat disediakan kemudian sebagai fitur tambahan.

---

# 4. Apa yang Diindeks?

Bukan semua konten internet.

Hanya **objek yang memiliki utility**.

### 💼 Work

* lowongan aktif
* freelance project
* remote work
* internship
* project-based work
* skill requirements

### 💰 Money

* peluang bisnis
* affiliate program
* reseller program
* freelance opportunity
* procurement/tender
* business opportunity

### 🏢 Business

* supplier
* vendor
* software
* services
* API
* tools
* infrastructure
* business resources

### 🛠️ Tools

* calculators
* converters
* generators
* validators
* simulators
* productivity tools
* developer tools

### 🧩 Build

* APIs
* libraries
* SDK
* datasets
* templates
* components
* infrastructure

### 🛒 Buy / Acquire

* products
* equipment
* property
* services
* suppliers
* software

### 📚 Learn

* courses
* documentation
* tutorials
* certifications
* learning resources

---

# 5. Contoh Perbedaan dengan Google

### Google

User:

> `Python developer remote Indonesia`

Google memberikan:

```text
10.000+ halaman
```

### Utility Search

Platform memberikan:

```text
1,842 active jobs

Python Backend Developer
PT ABC
Remote
Rp10–15 juta
Python • Django • PostgreSQL
Active 3 hours ago

[View Job]
```

Kemudian:

> **More useful results**

Bukan sekadar menampilkan URL.

---

# 6. Data Normalization

Sumber berbeda menggunakan format berbeda.

Contoh:

```text
"Software Engineer"
"Backend Developer"
"Python Developer"
"Python Programmer"
```

Platform melakukan normalisasi sehingga data dapat dibandingkan.

Contoh:

```text
JOB
├── Title
├── Company
├── Location
├── Remote
├── Salary
├── Skills
├── Employment Type
├── Posted Date
├── Expiration
├── Source
└── Status
```

Hal yang sama berlaku untuk:

* products
* APIs
* suppliers
* services
* tools
* courses
* opportunities

---

# 7. Freshness & Availability

Salah satu nilai utama platform adalah **mengetahui apakah sesuatu masih bisa digunakan.**

Contoh job:

```text
🟢 ACTIVE
🟡 CLOSING SOON
⚪ UNKNOWN
🔴 EXPIRED
```

Contoh API:

```text
🟢 ONLINE
🟡 DEGRADED
🔴 OFFLINE
```

Contoh tool:

```text
🟢 AVAILABLE
🔴 UNAVAILABLE
```

Data yang sudah tidak relevan tidak ditampilkan sebagai hasil utama.

---

# 8. UtilityRank

Platform tidak hanya melakukan keyword ranking.

Setiap objek dapat memiliki **Utility Score** berdasarkan beberapa faktor:

```text
Freshness
Availability
Relevance
Reliability
Completeness
Popularity
Accessibility
```

Contoh:

```text
Utility Score: 94/100
```

Tujuannya:

> **Hasil terbaik bukan yang paling banyak backlink-nya, tetapi yang paling berguna bagi intent user.**

Ini menjadi salah satu bagian teknologi inti platform.

---

# 9. User Experience

Homepage sangat sederhana.

```text
┌──────────────────────────────────────────┐
│                                          │
│       What do you want to accomplish?    │
│                                          │
│  [ Find a remote Python job........ ]    │
│                                          │
└──────────────────────────────────────────┘
```

User tidak harus memilih kategori terlebih dahulu.

Platform memahami intent secara bertahap.

Contoh:

> `Saya ingin mencari supplier kabel LAN murah`

Sistem memahami:

```text
Intent: BUY
Object: Supplier
Category: Network Equipment
Location: Indonesia
Priority: Price
```

Kemudian menampilkan hasil terstruktur.

---

# 10. Public Layer

Public menggunakan platform secara gratis.

Contoh pencarian:

```text
Cari pekerjaan
Cari supplier
Cari produk
Cari software
Cari API
Cari tools
Cari jasa
Cari peluang bisnis
Cari kursus
Cari resources
```

Target utamanya:

> **Membantu seseorang menemukan sesuatu yang berguna secepat mungkin.**

---

# 11. B2B Layer

Setelah index cukup besar, data yang sama memiliki nilai bagi bisnis.

Contoh:

### Market Intelligence

> Berapa banyak perusahaan yang sedang hiring Python Developer?

### Supplier Intelligence

> Supplier apa yang tersedia untuk produk tertentu?

### Competitor Intelligence

> Produk apa yang baru muncul?

### Opportunity Intelligence

> Program affiliate apa yang sedang aktif?

### Labor Intelligence

> Skill apa yang paling banyak dicari?

B2B mendapatkan:

* dashboard
* monitoring
* alerts
* analytics
* historical data
* exports
* advanced filters

Model:

**Subscription.**

---

# 12. Developer Layer

Tahap selanjutnya adalah menyediakan **Utility API**.

Developer tidak perlu crawl ribuan website sendiri.

Contoh:

```http
GET /v1/search
```

Query:

```text
intent=work
category=jobs
skill=python
location=indonesia
status=active
```

Atau:

```http
GET /v1/tools
GET /v1/apis
GET /v1/products
GET /v1/jobs
GET /v1/suppliers
GET /v1/opportunities
```

Developer kemudian dapat membangun aplikasi di atas index kita.

---

# 13. Ecosystem

Dalam jangka panjang:

```text
PUBLIC
   ↓
UTILITY SEARCH
   ↓
BUSINESS
   ↓
UTILITY DATA
   ↓
API
   ↓
DEVELOPERS
   ↓
NEW APPLICATIONS
   ↓
MORE DATA
   ↓
MORE UTILITY
```

Developer, creator, researcher, recruiter, agency, data provider, dan business partner dapat membangun layanan di atas ecosystem tersebut.

---

# 14. Model Bisnis

### Public

**Free**

Search dasar dan discovery.

### Pro User

Subscription untuk:

* saved searches
* alerts
* advanced filtering
* history
* exports
* personalized results

### Business

Subscription:

* market intelligence
* monitoring
* analytics
* competitor tracking
* supplier intelligence
* recruitment intelligence

### Developer

**API subscription / usage**

* Utility Search API
* Jobs API
* Product API
* Supplier API
* Tools API
* Opportunity API

### Enterprise

Custom:

* API quota
* dedicated data
* custom indexes
* SLA
* advanced intelligence

---

# 15. Prinsip Biaya Awal

**MVP tidak bergantung pada paid AI API.**

Stack awal:

```text
VPS
├── Crawler
├── Parser
├── Database
├── Search Engine
├── Scheduler
├── Web Application
└── API
```

AI **bukan core requirement**.

Jika suatu saat diperlukan, AI dapat ditambahkan untuk:

* classification
* entity extraction
* normalization
* duplicate detection
* intent understanding

Tetapi hanya setelah produk memiliki revenue atau menggunakan model lokal/open-source yang sesuai.

---

# 16. MVP Pertama

Jangan langsung meng-index seluruh internet.

Mulai dari **satu vertical**.

Contoh kandidat awal:

> **Jobs**

Crawler:

```text
Public career pages
       ↓
Job discovery
       ↓
Extract
       ↓
Normalize
       ↓
Check active status
       ↓
Index
       ↓
Search
```

User dapat mencari:

```text
Python Developer
Remote
Indonesia
Active
Salary available
```

MVP harus membuktikan tiga hal:

### 1. Discovery

Bisakah kita menemukan data publik secara otomatis?

### 2. Quality

Bisakah kita membuat hasil jauh lebih bersih daripada pencarian umum?

### 3. Utility

Apakah orang benar-benar merasa:

> **"Ini menghemat waktu saya."**

Kalau tiga hal tersebut terbukti, engine dapat diperluas ke vertical lain.

---

# 17. Roadmap

### Phase 1 — Index

```text
Crawler
Parser
Database
Search
Active/expired detection
```

### Phase 2 — Vertical Search

```text
Jobs
Products
Tools
APIs
Suppliers
Opportunities
```

diperluas **satu per satu**, berdasarkan validasi.

### Phase 3 — Intelligence

```text
Ranking
Recommendations
Monitoring
Alerts
Historical data
```

### Phase 4 — B2B

```text
Analytics
Market intelligence
Data export
Monitoring
Subscriptions
```

### Phase 5 — Developer Platform

```text
API
SDK
Webhooks
Developer dashboard
Usage billing
```

### Phase 6 — Ecosystem

```text
Developers
Partners
Data contributors
Business integrations
Third-party applications
```

---

# 18. Filosofi Produk

Produk ini **bukan dibuat untuk membuat orang menghabiskan waktu di dalam platform.**

Filosofinya:

> **Intent → Discovery → Action → Outcome**

Bukan:

> Attention → scrolling → ads.

Outcome yang ingin dibantu:

**mendapat pekerjaan.**

**mendapat pelanggan.**

**mendapat supplier.**

**mendapat produk.**

**menemukan software.**

**membangun sesuatu.**

**menjalankan bisnis.**

**menghasilkan uang.**

---

# 19. North Star

> ### **Make the useful internet searchable.**

Atau versi yang lebih ambisius:

> ### **We don't index the internet to tell people what's there.
>
> We index it to help people do something with it.**

---

## Kesimpulan

Ini bukan proyek **"membuat Google baru."**

Ini adalah usaha membangun:

> **Utility Index — sebuah index terstruktur atas hal-hal berguna yang tersedia di internet.**

Google mengoptimalkan:

**Page → Search**

Kita mengoptimalkan:

**Utility → Search → Action**

Dan jika berhasil:

**Public Search → B2B Intelligence → Utility API → Developer Ecosystem.**

Itulah yang membuat proyek ini bisa dimulai kecil dengan **satu VPS dan satu vertical**, tetapi secara arsitektur masih memiliki jalan untuk menjadi sesuatu yang jauh lebih besar.
