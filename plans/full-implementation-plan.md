# Rencana Implementasi Lengkap - Konektivitas.com

> Total: 7 bug + 10 gap backend + 10 gap view + 6 gap navigation = 33 item

---

## FASE 1: Bug Fix & Backend Konsistensi (6 item)

### 1a. Input Validation di Semua Router
**File:** `app/routers/dns.py`, `domain.py`, `ssl.py`, `website.py`, `ip.py`
**File:** `app/utils/validators.py` (sudah ada, tinggal pakai)

- Tambahkan `validate_domain()`, `validate_ip()`, `validate_url()`, `validate_host()` di setiap endpoint
- Return 400 Bad Request jika validasi gagal
- Sanitize input sebelum diproses

### 1b. Fix Async Blocking
**File:** `app/services/dns_service.py`, `whois_service.py`, `ssl_service.py`

- `lookup_dns()`: Bungkus `dns.resolver.resolve()` dalam `asyncio.to_thread()`
- `lookup_whois()`: Bungkus `whois.whois()` dalam `asyncio.to_thread()`
- `check_ssl()`: Bungkus socket/ssl operations dalam `asyncio.to_thread()`
- Pattern: Ikuti pola yang sudah benar di `_lookup_dns_raw()`, `_whois_raw()`, `_ssl_raw()`

### 1c. Fix XSS di copyJSON
**File:** `app/static/js/app.js`

- Ganti `data-json` attribute approach dengan cara yang lebih aman
- Gunakan `textContent` atau simpan data di JS variable, bukan di HTML attribute
- Escape HTML entities dengan benar

### 1d. Website Router HTTP Fallback
**File:** `app/routers/website.py` -> pindah ke `app/services/website_service.py`

- Coba HTTPS dulu, kalau gagal coba HTTP
- Log perubahan protocol

### 1e. Cache DNS Propagation
**File:** `app/services/dns_service.py`

- Tambahkan `@cached(ttl=60)` ke `propagation_check()` (TTL pendek karena data berubah)

### 1f. Buat website_service.py
**File:** `app/services/website_service.py` (baru)

- Pindahkan semua business logic dari `website.py` ke service layer
- Implementasi HTTP fallback (https -> http)
- Tambah caching dengan `@cached`

---

## FASE 2: New Tools Ringan (5 tools baru)

### 2a. My IP Endpoint + Page
**File:** `app/routers/ip.py` (tambah endpoint), `app/templates/tools/my_ip.html` (baru)

- Endpoint: `GET /api/v1/ip/me`
- Deteksi IP dari request headers
- Auto-lookup info lengkap
- Page: `/my-ip`

### 2b. User-Agent Checker
**File:** `app/routers/website.py` (tambah endpoint), `app/templates/tools/ua_checker.html` (baru)

- Endpoint: `GET /api/v1/ua` (auto-detect dari request) + `GET /api/v1/ua/{encoded_ua}`
- Parse: browser, OS, device type, version
- Page: `/ua-checker`

### 2c. Email Validation
**File:** `app/routers/domain.py` (tambah endpoint), `app/templates/tools/email_validator.html` (baru)

- Endpoint: `GET /api/v1/email/{email}/validate`
- Cek format, MX record, disposable detection
- Page: `/email-validator`

### 2d. NS Lookup Page
**File:** `app/templates/tools/ns_lookup.html` (baru)

- Reuse endpoint: `GET /api/v1/dns/{domain}?record_type=NS`
- Page khusus dengan UI yang lebih fokus ke NS records
- Page: `/ns-lookup`

### 2e. Basic Port Scanner
**File:** `app/routers/ip.py` (tambah endpoint), `app/templates/tools/port_scanner.html` (baru)

- Endpoint: `GET /api/v1/port/{host}` dengan query param `ports=80,443,22`
- TCP connect scan ke port umum
- Page: `/port-scanner`

---

## FASE 3: View Improvements (6 item)

### 3a. About Page
**File:** `app/templates/about.html` (baru)

- Visi, misi, filosofi
- Tech stack
- Timeline roadmap
- Page: `/about`

### 3b. API Documentation Page
**File:** `app/templates/api_docs.html` (baru)

- Daftar semua 24+ endpoints
- Contoh request/response
- Rate limit info
- Page: `/api`

### 3c. Tool History (localStorage)
**File:** `app/static/js/app.js` (update)

- Simpan 5-10 query terakhir per tool
- Tampilkan di bawah form sebagai "Riwayat Pencarian"
- Bisa klik untuk query ulang

### 3d. FAQ JSON-LD Schema
**File:** `app/templates/base.html`, `app/data/education.py`

- Tambah FAQPage structured data untuk SEO
- Generate dari education sections yang ada

### 3e. Mobile Card Layout untuk Result Tables
**File:** `app/static/css/style.css` (update)

- Di mobile: table rows jadi card layout
- Lebih mudah dibaca di layar kecil

### 3f. Breadcrumb Link ke Category
**File:** `app/templates/partials/breadcrumb.html` (update)

- Category name jadi clickable link ke homepage dengan filter

---

## FASE 4: Feature Enhancement (7 item)

### 4a. Dark Mode Toggle
**File:** `app/static/css/style.css`, `app/static/js/app.js`, `app/templates/base.html`

- CSS variables untuk theme colors
- Toggle button di header
- Simpan preference di localStorage
- System preference detection

### 4b. URL Query State
**File:** `app/static/js/app.js`, semua template tools

- Update URL dengan query param saat submit
- Load query dari URL saat page load
- Shareable URLs

### 4c. Keyboard Shortcuts
**File:** `app/static/js/app.js`, `app/templates/base.html`

- Ctrl+K: Focus search
- Escape: Close dropdown/menus
- Toast notification untuk shortcuts

### 4d. PWA manifest.json
**File:** `app/static/manifest.json` (baru), `app/static/sw.js` (baru)

- Manifest dengan icon, theme color, display
- Basic service worker untuk offline
- Link di base.html

### 4e. WHOIS Extra Fields
**File:** `app/services/whois_service.py`

- Tambah: registrant name, org, email
- Admin contact, Tech contact
- Domain status codes

### 4f. SSL Certificate Chain
**File:** `app/services/ssl_service.py`

- Tampilkan intermediate certificates
- Certificate chain validation
- Subject Alternative Names (SANs)

### 4g. HTTP Version Detection
**File:** `app/services/website_service.py`

- Deteksi HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3
- Tampilkan di header checker results

---

## Update Dokumen

### FEATURES.md
- Tambah semua new tools ke daftar
- Update status fase

### AGENT.md
- Update struktur file
- Update daftar endpoints
- Update URL patterns

### sitemap.xml
- Tambah semua URL baru

### robots.txt
- Pastikan benar

---

## File yang Perlu Dibuat/Diupdate

### File Baru (14):
1. `app/services/website_service.py`
2. `app/services/ua_service.py`
3. `app/services/email_service.py`
4. `app/services/port_service.py`
5. `app/templates/tools/my_ip.html`
6. `app/templates/tools/ua_checker.html`
7. `app/templates/tools/email_validator.html`
8. `app/templates/tools/ns_lookup.html`
9. `app/templates/tools/port_scanner.html`
10. `app/templates/about.html`
11. `app/templates/api_docs.html`
12. `app/static/manifest.json`
13. `app/static/sw.js`
14. `app/data/faq_data.py`

### File yang Perlu Diupdate (19):
1. `app/routers/dns.py`
2. `app/routers/domain.py`
3. `app/routers/ssl.py`
4. `app/routers/website.py`
5. `app/routers/ip.py`
6. `app/services/dns_service.py`
7. `app/services/whois_service.py`
8. `app/services/ssl_service.py`
9. `app/services/ip_service.py`
10. `app/main.py`
11. `app/static/js/app.js`
12. `app/static/css/style.css`
13. `app/templates/base.html`
14. `app/templates/index.html`
15. `app/templates/partials/breadcrumb.html`
16. `app/templates/partials/education.html`
17. `FEATURES.md`
18. `AGENT.md`
19. `app/static/sitemap.xml` (dynamic di main.py)
