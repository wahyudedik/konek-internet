"""FAQ data untuk Konektivitas.com - digunakan untuk JSON-LD FAQPage schema."""

FAQ_DATA = [
    {
        "question": "Apa itu Konektivitas.com?",
        "answer": "Konektivitas.com adalah platform infrastruktur internet Indonesia yang membantu siapa pun memahami, mengelola, dan mengembangkan aset digital mereka. Tersedia 25+ tools gratis untuk cek DNS, WHOIS, SSL, IP address, dan banyak lagi."
    },
    {
        "question": "Apakah semua tools gratis?",
        "answer": "Ya, 25+ Public Tools di Konektivitas.com dapat digunakan secara gratis tanpa registrasi. Untuk fitur lanjutan seperti monitoring dan workspace, tersedia paket premium dan enterprise."
    },
    {
        "question": "Apa saja yang bisa dicek di Konektivitas.com?",
        "answer": "Anda bisa mengecek DNS records (A, AAAA, MX, TXT, CNAME, NS), WHOIS domain, SSL certificate, HTTP status, IP address, port scanner, email validator, CDN detection, dan banyak lagi — total 25 tools dalam 5 kategori."
    },
    {
        "question": "Bagaimana cara menggunakan API Konektivitas.com?",
        "answer": "Kunjungi halaman API Documentation di /api-docs untuk melihat daftar lengkap endpoint dan cara penggunaannya. API kami gratis dengan rate limit 60 request per menit per IP."
    },
    {
        "question": "Apakah ada batasan penggunaan?",
        "answer": "Rate limit ditetapkan 60 request per menit per IP address untuk menjaga kualitas layanan. Semua tools tetap dapat digunakan tanpa registrasi."
    },
    {
        "question": "Apakah data saya aman?",
        "answer": "Ya, Konektivitas.com tidak menyimpan data pribadi pengguna. Semua query hanya diproses secara real-time dan tidak disimpan di database kami."
    },
    # ============ DNS Tools ============
    {
        "question": "Bagaimana cara cek DNS record?",
        "answer": "Gunakan tool DNS Lookup, masukkan nama domain, pilih jenis record yang ingin dicek (A, AAAA, MX, TXT, CNAME, NS), lalu klik 'Cek Sekarang'. Hasil akan ditampilkan dalam hitungan detik."
    },
    {
        "question": "Apa itu Reverse DNS dan bagaimana cara mengeceknya?",
        "answer": "Reverse DNS adalah proses mencari nama domain dari sebuah IP address. Gunakan tool Reverse DNS, masukkan IP address, dan sistem akan mencari PTR record yang terkait."
    },
    {
        "question": "Bagaimana cara mengecek propagasi DNS global?",
        "answer": "Gunakan tool DNS Propagation untuk melihat status DNS record dari berbagai lokasi server di seluruh dunia. Ini membantu memverifikasi apakah perubahan DNS sudah menyebar ke semua DNS server."
    },
    {
        "question": "Apa itu MX record dan bagaimana cara mengeceknya?",
        "answer": "MX (Mail Exchange) record menunjukkan server email yang menerima email untuk domain. Gunakan tool MX Lookup, masukkan nama domain, dan lihat daftar mail server beserta prioritasnya."
    },
    {
        "question": "Bagaimana cara mengecek SPF record?",
        "answer": "Gunakan tool SPF Checker, masukkan nama domain, dan sistem akan memvalidasi SPF record. SPF membantu mencegah email spam dengan menentukan server mana yang diizinkan mengirim email atas nama domain Anda."
    },
    {
        "question": "Bagaimana cara mengecek DMARC record?",
        "answer": "Gunakan tool DMARC Checker untuk memverifikasi konfigurasi DMARC domain Anda. DMARC bekerja bersama SPF dan DKIM untuk melindungi domain dari email phishing dan spoofing."
    },
    # ============ Domain Tools ============
    {
        "question": "Bagaimana cara mengecek WHOIS domain?",
        "answer": "Gunakan tool WHOIS Lookup, masukkan nama domain, dan lihat informasi registrasi termasuk pemilik domain, registrar, tanggal registrasi, dan tanggal kadaluarsa."
    },
    {
        "question": "Bagaimana cara mengecek masa aktif domain?",
        "answer": "Gunakan tool Domain Expiry untuk melihat kapan domain akan kadaluarsa. Ini penting agar Anda tidak kehilangan domain karena lupa memperpanjang."
    },
    # ============ SSL Tools ============
    {
        "question": "Bagaimana cara mengecek SSL certificate?",
        "answer": "Gunakan tool SSL Checker, masukkan nama domain, dan lihat detail termasuk issuer, expiry date, validity status, dan sisa hari aktif sertifikat."
    },
    {
        "question": "Bagaimana cara mengecek expiry SSL certificate?",
        "answer": "Gunakan tool SSL Expiry untuk melihat kapan sertifikat SSL Anda akan kadaluarsa. Sertifikat SSL yang kedaluwarsa akan membuat website Anda tidak aman dan mengakibatkan peringatan di browser."
    },
    # ============ Website Tools ============
    {
        "question": "Bagaimana cara mengecek apakah website aktif?",
        "answer": "Gunakan tool Ping Checker, masukkan hostname atau IP address, dan sistem akan mengirim paket ICMP untuk mengecek apakah server merespons."
    },
    {
        "question": "Bagaimana cara mengecek HTTP status code?",
        "answer": "Gunakan tool HTTP Status, masukkan URL website, dan lihat HTTP response code (200 OK, 301 Redirect, 404 Not Found, 500 Server Error, dll)."
    },
    {
        "question": "Bagaimana cara melacak redirect chain?",
        "answer": "Gunakan tool Redirect Checker, masukkan URL, dan sistem akan melacak setiap redirect dari URL awal hingga URL final. Ini membantu memahami alur redirect website Anda."
    },
    {
        "question": "Bagaimana cara mengecek HTTP headers?",
        "answer": "Gunakan tool Header Checker untuk melihat semua HTTP response headers dari sebuah URL, termasuk version HTTP yang digunakan (HTTP/1.0, 1.1, 2, atau 3)."
    },
    {
        "question": "Bagaimana cara mendeteksi CDN yang digunakan website?",
        "answer": "Gunakan tool CDN Detection, masukkan nama domain, dan sistem akan menganalisis CNAME record dan HTTP headers untuk mengidentifikasi provider CDN yang digunakan."
    },
    # ============ IP Tools ============
    {
        "question": "Bagaimana cara mengecek informasi IP address?",
        "answer": "Gunakan tool IP Lookup, masukkan IP address, dan lihat informasi lengkap termasuk lokasi geografis, ISP, ASN, dan banyak lagi."
    },
    {
        "question": "Bagaimana cara mengecek IP address saya?",
        "answer": "Gunakan tool My IP untuk langsung mengetahui IP address publik Anda beserta informasi geografis dan ISP yang Anda gunakan."
    },
    {
        "question": "Bagaimana cara mengecek apakah IP masuk blacklist?",
        "answer": "Gunakan tool Blacklist Checker, masukkan IP address, dan sistem akan mengecek ke beberapa blacklist database untuk melihat apakah IP Anda terdaftar di salah satu daftar hitam."
    },
    {
        "question": "Bagaimana cara mengecek port yang terbuka?",
        "answer": "Gunakan tool Port Scanner, masukkan hostname atau IP address, dan tentukan port yang ingin dicek. Sistem akan mengecek port mana yang terbuka dan dapat diakses."
    },
    {
        "question": "Bagaimana cara memvalidasi email address?",
        "answer": "Gunakan tool Email Validator, masukkan alamat email, dan sistem akan memvalidasi format, mendeteksi disposable email provider, dan memverifikasi MX record domain email."
    },
]
