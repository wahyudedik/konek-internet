"""
Konten edukasi untuk semua 25 tool pages di Konektivitas.com.
Setiap tool memiliki section: apa itu, cara membaca, tips, dan tool terkait.
"""

EDUCATION_DATA = {
    # ============================================================
    # DNS TOOLS (8 tools)
    # ============================================================

    "dns_lookup": {
        "title": "📚 Belajar: Apa itu DNS?",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🌐 Apa itu DNS?",
                "content": """<p>DNS <strong>(Domain Name System)</strong> adalah sistem yang menerjemahkan nama domain menjadi IP address.</p>
<p>Seperti buku telepon internet:</p>
<ul>
<li><code>google.com</code> → <code>142.250.185.78</code></li>
<li><code>konektivitas.com</code> → IP address server kami</li>
</ul>
<p>Tanpa DNS, kamu harus mengingat angka IP untuk setiap website.</p>"""
            },
            {
                "heading": "📋 Jenis Record DNS",
                "content": """<div class="edu-table">
<table>
<tr><th>Record</th><th>Fungsi</th><th>Contoh</th></tr>
<tr><td><code>A</code></td><td>IPv4 Address</td><td>142.250.185.78</td></tr>
<tr><td><code>AAAA</code></td><td>IPv6 Address</td><td>2607:f8b0:4004:800::200e</td></tr>
<tr><td><code>MX</code></td><td>Mail Server</td><td>smtp.google.com</td></tr>
<tr><td><code>TXT</code></td><td>Teks (SPF/DKIM)</td><td>v=spf1 include:_spf...</td></tr>
<tr><td><code>CNAME</code></td><td>Alias domain</td><td>www → example.com</td></tr>
<tr><td><code>NS</code></td><td>Nameserver</td><td>ns1.google.com</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>TTL (Time To Live)</strong> → Berapa lama data di-cache (dalam detik)</li>
<li><strong>Priority</strong> → Untuk MX record, angka kecil = prioritas tinggi</li>
<li><strong>Class</strong> → Biasanya IN (Internet)</li>
</ul>
<p>Jika hasil kosong, kemungkinan domain belum dikonfigurasi atau salah ketik.</p>"""
            },
            {
                "heading": "💡 Tips & Best Practices",
                "content": """<ul>
<li>Gunakan DNS Google (8.8.8.8) atau Cloudflare (1.1.1.1) untuk cek cepat</li>
<li>TTL rendah (60-300 detik) = perubahan lebih cepat menyebar</li>
<li>TTL tinggi (3600-86400) = hemat query tapi perubahan lambat</li>
<li>Jika A record kosong, domain mungkin down atau belum dikonfigurasi</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "reverse-dns", "name": "Reverse DNS", "icon": "🔄"},
            {"slug": "mx-lookup", "name": "MX Lookup", "icon": "📧"},
            {"slug": "txt-lookup", "name": "TXT Lookup", "icon": "📄"},
            {"slug": "dns-propagation", "name": "DNS Propagation", "icon": "🌍"}
        ]
    },

    "reverse_dns": {
        "title": "📚 Belajar: Reverse DNS (PTR Record)",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🔄 Apa itu Reverse DNS?",
                "content": """<p><strong>Reverse DNS (rDNS)</strong> adalah kebalikan dari DNS biasa.</p>
<ul>
<li>DNS biasa: <code>google.com</code> → <code>142.250.185.78</code></li>
<li>Reverse DNS: <code>142.250.185.78</code> → <code>google.com</code></li>
</ul>
<p>Gunakan <strong>PTR Record</strong> untuk mapping IP ke hostname.</p>"""
            },
            {
                "heading": "🎯 Mengapa Penting?",
                "content": """<ul>
<li><strong>Email Server</strong> → Banyak email server menolak email dari IP tanpa PTR record</li>
<li><strong>Keamanan</strong> → Membantu identifikasi sumber traffic mencurigakan</li>
<li><strong>Logging</strong> → Membaca log server lebih mudah dengan nama domain</li>
<li><strong>Spam Prevention</strong> → Email server validasi reverse DNS sebelum terima email</li>
</ul>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>PTR Record</strong> → Hostname yang terkait dengan IP</li>
<li><strong>Forward-Confirmed Reverse DNS</strong> → DNS forward dari PTR harus match dengan IP asli</li>
<li>Jika tidak ada PTR record, IP tidak memiliki hostname terkait</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>PTR record diatur oleh pemilik IP (ISP/hosting), bukan domain</li>
<li>Untuk email server, pastikan PTR record match dengan A record (forward-confirmed)</li>
<li>Beberapa ISP memblokir perubahan PTR record untuk pelanggan rumahan</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"},
            {"slug": "ip-lookup", "name": "IP Lookup", "icon": "📍"},
            {"slug": "blacklist-checker", "name": "Blacklist Checker", "icon": "🚫"},
            {"slug": "mx-lookup", "name": "MX Lookup", "icon": "📧"}
        ]
    },

    "dns_propagation": {
        "title": "📚 Belajar: DNS Propagation",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🌍 Apa itu DNS Propagation?",
                "content": """<p><strong>DNS Propagation</strong> adalah proses penyebaran perubahan DNS ke seluruh nameserver di dunia.</p>
<p>Ketika kamu mengubah DNS record, perubahan tidak langsung terlihat di semua lokasi. Setiap ISP memiliki cache DNS yang perlu di-update.</p>"""
            },
            {
                "heading": "⏱️ Berapa Lama Propagasi?",
                "content": """<div class="edu-table">
<table>
<tr><th>Record Type</th><th>Waktu Normal</th><th>Waktu Maksimal</th></tr>
<tr><td>A Record</td><td>5-30 menit</td><td>24-48 jam</td></tr>
<tr><td>MX Record</td><td>30-60 menit</td><td>48-72 jam</td></tr>
<tr><td>NS Record</td><td>1-4 jam</td><td>72 jam</td></tr>
<tr><td>TXT Record</td><td>5-15 menit</td><td>24 jam</td></tr>
</table>
</div>"""
            },
            {
                "heading": "🔍 Nameserver Global yang Dicek",
                "content": """<ul>
<li><strong>Google DNS</strong> → 8.8.8.8 (populer, cepat)</li>
<li><strong>Cloudflare DNS</strong> → 1.1.1.1 (privasi, cepat)</li>
<li><strong>OpenDNS</strong> → 208.67.222.222 (Cisco)</li>
<li><strong>Quad9</strong> → 9.9.9.9 (keamanan)</li>
<li><strong>AdGuard DNS</strong> → 94.140.14.14 (block ads)</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Tunggu minimal 1 jam sebelum cek propagation</li>
<li>Jika ada perbedaan antar nameserver, tunggu beberapa jam lagi</li>
<li>Gunakan TTL rendah (300 detik) untuk perubahan cepat</li>
<li>Flush DNS cache local: <code>ipconfig /flushdns</code> (Windows)</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"},
            {"slug": "reverse-dns", "name": "Reverse DNS", "icon": "🔄"},
            {"slug": "cname-lookup", "name": "CNAME Lookup", "icon": "🔗"}
        ]
    },

    "mx_lookup": {
        "title": "📚 Belajar: MX Record (Mail Exchange)",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "📧 Apa itu MX Record?",
                "content": """<p><strong>MX (Mail Exchange)</strong> record menunjukkan server yang menangani email untuk domain.</p>
<p>Ketika seseorang mengirim email ke <code>user@example.com</code>, sistem email mencari MX record untuk domain <code>example.com</code> untuk mengetahui server mana yang harus dikirimi email.</p>"""
            },
            {
                "heading": "🎯 Kenapa MX Record Penting?",
                "content": """<ul>
<li><strong>Email Berfungsi</strong> → Tanpa MX record, email tidak dapat dikirim ke domain</li>
<li><strong>Redundancy</strong> → Multiple MX record untuk backup jika server utama down</li>
<li><strong>Load Balancing</strong> → Distribusi beban email ke beberapa server</li>
<li><strong>Migrasi Email</strong> → Mengubah MX record untuk pindah provider email</li>
</ul>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Priority</strong> → Angka kecil = prioritas tinggi (dihubungi duluan)</li>
<li><strong>Target</strong> → Alamat server email yang menangani pesan</li>
<li>Contoh: MX 10 mail1.example.com, MX 20 mail2.example.com → mail1 dihubungi duluan</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Gunakan minimal 2 MX record untuk redundancy</li>
<li>Google Workspace: MX 1 aspmx.l.google.com</li>
<li>Microsoft 365: MX 0 domain-com.mail.protection.outlook.com</li>
<li>Jangan gunakan IP address di MX record, gunakan hostname</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "spf-checker", "name": "SPF Checker", "icon": "🛡️"},
            {"slug": "dmarc-checker", "name": "DMARC Checker", "icon": "🔐"},
            {"slug": "txt-lookup", "name": "TXT Lookup", "icon": "📄"},
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"}
        ]
    },

    "txt_lookup": {
        "title": "📚 Belajar: TXT Record",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "📄 Apa itu TXT Record?",
                "content": """<p><strong>TXT Record</strong> adalah record DNS yang berisi teks. Digunakan untuk:</p>
<ul>
<li><strong>Verifikasi Domain</strong> → Membuktikan kepemilikan domain</li>
<li><strong>Email Authentication</strong> → SPF, DKIM, DMARC</li>
<li><strong>Informasi</strong> → Catatan untuk admin jaringan</li>
</ul>"""
            },
            {
                "heading": "🛡️ TXT Record Penting untuk Email",
                "content": """<div class="edu-table">
<table>
<tr><th>TXT Type</th><th>Fungsi</th><th>Contoh</th></tr>
<tr><td><code>SPF</code></td><td>Siapa boleh kirim email</td><td>v=spf1 include:_spf.google.com ~all</td></tr>
<tr><td><code>DKIM</code></td><td>Verifikasi email tidak diubah</td><td>v=DKIM1; k=rsa; p=MIGf...</td></tr>
<tr><td><code>DMARC</code></td><td>Kebijakan keamanan email</td><td>v=DMARC1; p=quarantine</td></tr>
<tr><td><code>Verification</code></td><td>Bukti kepemilikan</td><td>google-site-verification=xxx</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Value</strong> → Isi teks dari record</li>
<li><strong>TTL</strong> → Berapa lama data di-cache</li>
<li>Multiple TXT records dapat ada untuk domain yang sama</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Pastikan SPF record hanya ada SATU untuk domain</li>
<li>DNS Limit: SPF record maksimal 255 karakter per record, 10 DNS lookups</li>
<li>Gunakan <code>~all</code> (soft fail) atau <code>-all</code> (hard fail) di SPF</li>
<li>DKIM key minimal 1024 bit, rekomendasi 2048 bit</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "spf-checker", "name": "SPF Checker", "icon": "🛡️"},
            {"slug": "dmarc-checker", "name": "DMARC Checker", "icon": "🔐"},
            {"slug": "mx-lookup", "name": "MX Lookup", "icon": "📧"},
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"}
        ]
    },

    "cname_lookup": {
        "title": "📚 Belajar: CNAME Record",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🔗 Apa itu CNAME?",
                "content": """<p><strong>CNAME (Canonical Name)</strong> adalah record yang membuat alias/pendekatan untuk domain lain.</p>
<p>Contoh: <code>www.example.com</code> → <code>example.com</code></p>
<p>Ketika seseorang mengakses <code>www.example.com</code>, DNS akan mengarahkan ke IP address dari <code>example.com</code>.</p>"""
            },
            {
                "heading": "🎯 Kapan Menggunakan CNAME?",
                "content": """<ul>
<li><strong>CDN</strong> → Mengarahkan ke server CDN (Cloudflare, AWS CloudFront)</li>
<li><strong>Subdomain</strong> → <code>blog.example.com</code> → <code>example.com</code></li>
<li><strong>Redirect</strong> → <code>www</code> → root domain</li>
<li><strong>Tracking</strong> → Subdomain untuk tracking clicks</li>
</ul>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>CNAME Target</strong> → Domain yang dituju</li>
<li><strong>TTL</strong> → Waktu cache</li>
<li>CNAME harus diakhiri titik (<code>.</code>) di DNS response</li>
</ul>"""
            },
            {
                "heading": "💡 Tips & Limitasi",
                "content": """<ul>
<li><strong>TIDAK BOLEH</strong> → CNAME di root domain (example.com)</li>
<li><strong>TIDAK BOLEH</strong> → CNAME jika sudah ada record lain (MX, TXT)</li>
<li><strong>BOLEH</strong> → CNAME di subdomain (www, blog, api)</li>
<li>Alternatif untuk root domain: A record atau ALIAS/ANAME record</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"},
            {"slug": "redirect-checker", "name": "Redirect Checker", "icon": "↩️"},
            {"slug": "dns-propagation", "name": "DNS Propagation", "icon": "🌍"}
        ]
    },

    "spf_checker": {
        "title": "📚 Belajar: SPF (Sender Policy Framework)",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🛡️ Apa itu SPF?",
                "content": """<p><strong>SPF (Sender Policy Framework)</strong> adalah standar email authentication yang menentukan server mana yang diizinkan mengirim email untuk domain.</p>
<p>Tanpa SPF, siapa saja bisa mengirim email yang terlihat berasal dari domain kamu (<em>email spoofing</em>).</p>"""
            },
            {
                "heading": "📧 Cara Kerja SPF",
                "content": """<ol>
<li>Kamu menambahkan TXT record SPF di DNS</li>
<li>Penerima email mengecek SPF record</li>
<li>Jika server pengirim tidak ada di SPF → email ditandai spam/ditolak</li>
</ol>
<p>Contoh SPF record Google Workspace:</p>
<p><code>v=spf1 include:_spf.google.com ~all</code></p>"""
            },
            {
                "heading": "📖 Cara Membaca SPF",
                "content": """<div class="edu-table">
<table>
<tr><th>Tag</th><th>Fungsi</th></tr>
<tr><td><code>v=spf1</code></td><td>Versi SPF</td></tr>
<tr><td><code>include:</code></td><td>Include SPF dari service lain</td></tr>
<tr><td><code>ip4:</code></td><td>Izinkan IP v4 tertentu</td></tr>
<tr><td><code>ip6:</code></td><td>Izinkan IP v6 tertentu</td></tr>
<tr><td><code>~all</code></td><td>Soft fail (tetap diterima tapi ditandai)</td></tr>
<tr><td><code>-all</code></td><td>Hard fail (ditolak)</td></tr>
<tr><td><code>?all</code></td><td>Neutral (tidak ada aksi)</td></tr>
</table>
</div>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Gunakan <code>-all</code> untuk keamanan ketat (email tidak valid = ditolak)</li>
<li>Gunakan <code>~all</code> untuk transisi perlahan (email tidak valid = spam folder)</li>
<li>SPF memiliki limit: maksimal 10 DNS lookups (include = 1 lookup)</li>
<li>Gunakan tool ini untuk cek apakah SPF sudah benar</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dmarc-checker", "name": "DMARC Checker", "icon": "🔐"},
            {"slug": "txt-lookup", "name": "TXT Lookup", "icon": "📄"},
            {"slug": "mx-lookup", "name": "MX Lookup", "icon": "📧"}
        ]
    },

    "dmarc_checker": {
        "title": "📚 Belajar: DMARC (Domain-based Message Authentication)",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🔐 Apa itu DMARC?",
                "content": """<p><strong>DMARC (Domain-based Message Authentication, Reporting & Conformance)</strong> adalah standar keamanan email yang membangun di atas SPF dan DKIM.</p>
<p>DMARC memberitahu server penerima apa yang harus dilakukan dengan email yang tidak lulus autentikasi.</p>"""
            },
            {
                "heading": "📧 Cara Kerja DMARC",
                "content": """<ol>
<li>Email dikirim ke penerima</li>
<li>Penerima mengecek SPF dan DKIM</li>
<li>Jika tidak valid, penerima mengecek DMARC policy</li>
<li>Policy menentukan: terima, quarantine, atau reject</li>
</ol>"""
            },
            {
                "heading": "📖 Cara Membaca DMARC Policy",
                "content": """<div class="edu-table">
<table>
<tr><th>Policy</th><th>Aksi</th><th>Kapan Digunakan</th></tr>
<tr><td><code>p=none</code></td><td>Tidak ada aksi (monitor saja)</td><td>Fase awal monitoring</td></tr>
<tr><td><code>p=quarantine</code></td><td>Masuk folder spam</td><td>Setelah yakin SPF/DKIM benar</td></tr>
<tr><td><code>p=reject</code></td><td>Ditolak sepenuhnya</td><td>Keamanan maksimal</td></tr>
</table>
</div>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Mulai dengan <code>p=none</code> untuk monitoring dulu</li>
<li>Setelah 2-4 minggu, naikkan ke <code>p=quarantine</code></li>
<li>Tambahkan <code>rua=mailto:</code> untuk laporan DMARC</li>
<li>Pastikan SPF dan DKIM sudah benar sebelum mengaktifkan DMARC reject</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "spf-checker", "name": "SPF Checker", "icon": "🛡️"},
            {"slug": "txt-lookup", "name": "TXT Lookup", "icon": "📄"},
            {"slug": "mx-lookup", "name": "MX Lookup", "icon": "📧"}
        ]
    },

    # ============================================================
    # DOMAIN TOOLS (2 tools)
    # ============================================================

    "whois_lookup": {
        "title": "📚 Belajar: WHOIS Lookup",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🌍 Apa itu WHOIS?",
                "content": """<p><strong>WHOIS</strong> adalah protokol untuk mengecek informasi registrasi domain.</p>
<p>Seperti "akte lahir" untuk domain yang berisi:</p>
<ul>
<li>Siapa pemilik domain (registrant)</li>
<li>Kapan didaftarkan (creation date)</li>
<li>Kapan expired (expiry date)</li>
<li>Server DNS yang digunakan (nameservers)</li>
</ul>"""
            },
            {
                "heading": "📋 Informasi WHOIS",
                "content": """<div class="edu-table">
<table>
<tr><th>Field</th><th>Arti</th></tr>
<tr><td><code>Registrar</code></td><td>Tempat domain didaftarkan (Namecheap, GoDaddy, dll)</td></tr>
<tr><td><code>Creation Date</code></td><td>Tanggal pertama kali domain didaftarkan</td></tr>
<tr><td><code>Expiry Date</code></td><td>Tanggal domain akan expired</td></tr>
<tr><td><code>Updated Date</code></td><td>Tanggal terakhir perubahan data</td></tr>
<tr><td><code>Name Servers</code></td><td>Server DNS yang mengelola domain</td></tr>
<tr><td><code>Status</code></td><td>Status domain (ok, pendingTransfer, dll)</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Registrar</strong> → Pastikan registrar resmi dan terpercaya</li>
<li><strong>Expiry Date</strong> → Penting untuk perpanjang sebelum expired</li>
<li><strong>Name Servers</strong> → Pastikan nameserver sudah benar</li>
<li><strong>Privacy Protection</strong> → Jika WHOIS privacy aktif, data pemilik disembunyikan</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Gunakan WHOIS privacy untuk melindungi data pribadi</li>
<li>Cek expiry date secara berkala untuk mencegah domain expired</li>
<li>Beberapa domain (ID, EU) memiliki aturan WHOIS berbeda</li>
<li>WHOIS lookup hanya untuk domain, bukan untuk IP address</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "domain-expiry", "name": "Domain Expiry", "icon": "⏰"},
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"},
            {"slug": "ssl-checker", "name": "SSL Checker", "icon": "🔒"}
        ]
    },

    "domain_expiry": {
        "title": "📚 Belajar: Domain Expiry & Lifecycle",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "⏰ Apa itu Domain Expiry?",
                "content": """<p>Domain tidak dimiliki selamanya, tetapi <strong>disewa</strong> untuk periode tertentu (1-10 tahun).</p>
<p>Ketika domain expired, pemilik lain dapat mendaftarkannya. Ini bisa berakibat fatal untuk bisnis.</p>"""
            },
            {
                "heading": "🔄 Lifecycle Domain",
                "content": """<ol>
<li><strong>Active</strong> → Domain aktif dan berfungsi</li>
<li><strong>Grace Period</strong> → 0-30 hari setelah expired (masih bisa diperpanjang)</li>
<li><strong>Redemption</strong> → 30-60 hari setelah expired (biaya lebih mahal)</li>
<li><strong>Pending Delete</strong> → 5 hari sebelum dihapus permanen</li>
<li><strong>Available</strong> → Domain bebas didaftarkan siapa saja</li>
</ol>"""
            },
            {
                "heading": "🎯 Mengapa Penting?",
                "content": """<ul>
<li><strong>Bisnis</strong> → Website dan email berhenti berfungsi</li>
<li><strong>SEO</strong> → Ranking Google turun drastis</li>
<li><strong>Brand</strong> → Domain bisa dicuri/didaftarkan orang lain</li>
<li><strong>Email</strong> → Semua email ke domain gagal terkirim</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Perpanjang domain 30-60 hari sebelum expired</li>
<li>Gunakan auto-renew jika tersedia</li>
<li>Cek expiry date minimal sebulan sekali</li>
<li>Siapkan backup plan jika domain akan expired</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "whois-lookup", "name": "WHOIS Lookup", "icon": "🌍"},
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"},
            {"slug": "ssl-checker", "name": "SSL Checker", "icon": "🔒"}
        ]
    },

    # ============================================================
    # SSL TOOLS (2 tools)
    # ============================================================

    "ssl_checker": {
        "title": "📚 Belajar: SSL/TLS Certificate",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🔒 Apa itu SSL/TLS?",
                "content": """<p><strong>SSL (Secure Sockets Layer)</strong> / <strong>TLS (Transport Layer Security)</strong> adalah protokol enkripsi yang mengamankan komunikasi antara browser dan server.</p>
<p>Website dengan SSL memiliki URL <code>https://</code> dan ikon gembok di browser.</p>"""
            },
            {
                "heading": "🛡️ Jenis Sertifikat SSL",
                "content": """<div class="edu-table">
<table>
<tr><th>Tipe</th><th>Level Verifikasi</th><th>Biaya</th><th>Contoh Issuer</th></tr>
<tr><td><code>Domain Validated (DV)</code></td><td>Hanya domain</td><td>Gratis</td><td>Let's Encrypt</td></tr>
<tr><td><code>Organization Validated (OV)</code></td><td>Nama organisasi</td><td>$20-100/th</td><td>Comodo, DigiCert</td></tr>
<tr><td><code>Extended Validation (EV)</code></td><td>Verifikasi lengkap</td><td>$100-500/th</td><td>GeoTrust, Symantec</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Issuer</strong> → Siapa yang menerbitkan sertifikat</li>
<li><strong>Valid From/Until</strong> → Masa aktif sertifikat</li>
<li><strong>Subject</strong> → Domain yang dilindungi</li>
<li><strong>Key Size</strong> → Kekuatan enkripsi (minimal 2048 bit)</li>
<li><strong>SAN</strong> → Domain tambahan yang dilindungi</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Gunakan <strong>Let's Encrypt</strong> untuk SSL gratis dan otomatis</li>
<li>SSL expired = browser akan menampilkan warning "Not Secure"</li>
<li>SSL gratis (DV) sudah cukup untuk kebanyakan website</li>
<li>Gunakan certbot untuk auto-renew SSL</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ssl-expiry", "name": "SSL Expiry", "icon": "⏰"},
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"},
            {"slug": "domain-expiry", "name": "Domain Expiry", "icon": "🌐"}
        ]
    },

    "ssl_expiry": {
        "title": "📚 Belajar: SSL Expiry & Renewal",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "⏰ Kapan SSL Expired?",
                "content": """<p>Sertifikat SSL memiliki masa aktif terbatas:</p>
<ul>
<li><strong>Let's Encrypt</strong> → 90 hari (gratis, auto-renew)</li>
<li><strong>Commercial SSL</strong> → 1 tahun (bayar)</li>
<li><strong>Extended Validation</strong> → 1-2 tahun (bayar mahal)</li>
</ul>"""
            },
            {
                "heading": "⚠️ Akibat SSL Expired",
                "content": """<ul>
<li>Browser menampilkan warning <strong>"Your connection is not private"</strong></li>
<li>Pengunjung tidak bisa mengakses website dengan normal</li>
<li>SEO ranking turun drastis</li>
<li>Email client tidak bisa terhubung (IMAP/SMTP)</li>
<li>API calls dari mobile apps gagal</li>
</ul>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Sisa Hari</strong> → Berapa hari lagi sebelum expired</li>
<li><strong>Tanggal Expired</strong> → Tanggal pasti SSL berakhir</li>
<li>Warna hijau = aman, kuning = perlu diperhatikan, merah = segera perpanjang</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Gunakan certbot untuk auto-renew Let's Encrypt</li>
<li>Setup cron job untuk renew otomatis 30 hari sebelum expired</li>
<li>Cek SSL expiry minimal seminggu sekali</li>
<li>Backup SSL certificate dan private key</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ssl-checker", "name": "SSL Checker", "icon": "🔒"},
            {"slug": "domain-expiry", "name": "Domain Expiry", "icon": "⏰"},
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"}
        ]
    },

    # ============================================================
    # WEBSITE TOOLS (4 tools)
    # ============================================================

    "ping_checker": {
        "title": "📚 Belajar: Ping & Latency",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "📡 Apa itu Ping?",
                "content": """<p><strong>Ping</strong> adalah alat untuk mengukur waktu respons antara komputer kamu dan server tujuan.</p>
<p>Menggunakan protokol <strong>ICMP (Internet Control Message Protocol)</strong>, ping mengirim paket data dan menunggu balasan.</p>"""
            },
            {
                "heading": "📊 Angka Ping yang Baik",
                "content": """<div class="edu-table">
<table>
<tr><th>Range</th><th>Kualitas</th><th>Cocok Untuk</th></tr>
<tr><td><code>< 20ms</code></td><td>🟢 Sangat Baik</td><td>Gaming, Video Call</td></tr>
<tr><td><code>20-50ms</code></td><td>🟢 Baik</td><td>Streaming, Browsing</td></tr>
<tr><td><code>50-100ms</code></td><td>🟡 Sedang</td><td>Browsing, Email</td></tr>
<tr><td><code>100-200ms</code></td><td>🟠 Lambat</td><td>Browsing biasa</td></tr>
<tr><td><code>> 200ms</code></td><td>🔴 Sangat Lambat</td><td>Kadang timeout</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Response Time (ms)</strong> → Waktu bolak-balik paket data</li>
<li><strong>Status</strong> → Server aktif atau tidak</li>
<li>Semakin rendah ms = semakin cepat koneksi</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Ping tinggi bisa disebabkan: jarak jauh, traffic jaringan, server overload</li>
<li>Gunakan tools ini untuk cek apakah website down atau hanya lambat</li>
<li>Ping dari Indonesia ke server Eropa biasanya 200-300ms</li>
<li>Ping dari Indonesia ke server Singapura biasanya 10-30ms</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "http-status", "name": "HTTP Status", "icon": "🔢"},
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"},
            {"slug": "ip-lookup", "name": "IP Lookup", "icon": "📍"}
        ]
    },

    "http_status": {
        "title": "📚 Belajar: HTTP Status Codes",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🔢 Apa itu HTTP Status Code?",
                "content": """<p><strong>HTTP Status Code</strong> adalah kode 3 digit yang dikirim server sebagai respon terhadap request browser.</p>
<p>Kode ini memberitahu apakah request berhasil, redirect, error, atau masalah lainnya.</p>"""
            },
            {
                "heading": "📋 Kode Status Penting",
                "content": """<div class="edu-table">
<table>
<tr><th>Kode</th><th>Nama</th><th>Arti</th></tr>
<tr><td><code>200</code></td><td>OK</td><td>Request berhasil</td></tr>
<tr><td><code>301</code></td><td>Moved Permanently</td><td>Redirect permanen</td></tr>
<tr><td><code>302</code></td><td>Found</td><td>Redirect sementara</td></tr>
<tr><td><code>304</code></td><td>Not Modified</td><td>Gunakan cache</td></tr>
<tr><td><code>403</code></td><td>Forbidden</td><td>Akses ditolak</td></tr>
<tr><td><code>404</code></td><td>Not Found</td><td>Halaman tidak ditemukan</td></tr>
<tr><td><code>429</code></td><td>Too Many Requests</td><td>Rate limit</td></tr>
<tr><td><code>500</code></td><td>Internal Server Error</td><td>Error server</td></tr>
<tr><td><code>502</code></td><td>Bad Gateway</td><td>Gateway error</td></tr>
<tr><td><code>503</code></td><td>Service Unavailable</td><td>Server sibuk/down</td></tr>
<tr><td><code>504</code></td><td>Gateway Timeout</td><td>Gateway timeout</td></tr>
</table>
</div>"""
            },
            {
                "heading": "🎯 Kategori Kode",
                "content": """<ul>
<li><strong>2xx (Sukses)</strong> → Request berhasil diproses</li>
<li><strong>3xx (Redirect)</strong> → Pengguna perlu melakukan aksi tambahan</li>
<li><strong>4xx (Client Error)</strong> → Kesalahan dari sisi pengguna/bROWSER</li>
<li><strong>5xx (Server Error)</strong> → Kesalahan dari sisi server</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>200 OK adalah yang diinginkan untuk semua halaman</li>
<li>404 berarti URL salah atau halaman sudah dihapus</li>
<li>500 berarti ada bug di server atau konfigurasi salah</li>
<li>301 redirect baik untuk SEO, 302 untuk maintenance sementara</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "redirect-checker", "name": "Redirect Checker", "icon": "↩️"},
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"},
            {"slug": "ping-checker", "name": "Ping Checker", "icon": "📡"}
        ]
    },

    "redirect_checker": {
        "title": "📚 Belajar: HTTP Redirects",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "↩️ Apa itu Redirect?",
                "content": """<p><strong>Redirect</strong> adalah pengalihan otomatis dari URL awal ke URL lain.</p>
<p>Contoh: <code>http://example.com</code> → <code>https://www.example.com</code></p>"""
            },
            {
                "heading": "🔄 Jenis Redirect",
                "content": """<div class="edu-table">
<table>
<tr><th>Kode</th><th>Nama</th><th>Penggunaan</th></tr>
<tr><td><code>301</code></td><td>Moved Permanently</td><td>URL berubah permanen (SEO: link juice dipindahkan)</td></tr>
<tr><td><code>302</code></td><td>Found</td><td>Redirect sementara (maintenance, A/B testing)</td></tr>
<tr><td><code>307</code></td><td>Temporary Redirect</td><td>Redirect sementara (method harus sama)</td></tr>
<tr><td><code>308</code></td><td>Permanent Redirect</td><td>Redirect permanen (method harus sama)</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Chain</strong> → Rantai redirect dari awal ke akhir</li>
<li><strong>Status per Hop</strong> → Kode status di setiap langkah redirect</li>
<li><strong>Final URL</strong> → URL terakhir setelah semua redirect</li>
<li>Jika ada > 5 hop, bisa jadi redirect loop</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Hindari redirect chain lebih dari 3 hop (lambat untuk user & SEO)</li>
<li>Gunakan 301 untuk redirect permanen (HTTPS migration, www → non-www)</li>
<li>Google merekomendasikan redirect 1 hop langsung ke final URL</li>
<li>Redirect loop = website tidak bisa diakses (error)</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "http-status", "name": "HTTP Status", "icon": "🔢"},
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"},
            {"slug": "cname-lookup", "name": "CNAME Lookup", "icon": "🔗"}
        ]
    },

    "header_checker": {
        "title": "📚 Belajar: HTTP Headers",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "📋 Apa itu HTTP Headers?",
                "content": """<p><strong>HTTP Headers</strong> adalah metadata yang dikirim server bersama response.</p>
<p>Headers berisi informasi tentang content type, security, caching, dan banyak lagi.</p>"""
            },
            {
                "heading": "🛡️ Security Headers Penting",
                "content": """<div class="edu-table">
<table>
<tr><th>Header</th><th>Fungsi</th><th>Nilai Ideal</th></tr>
<tr><td><code>Strict-Transport-Security</code></td><td>Paksa HTTPS</td><td>max-age=31536000</td></tr>
<tr><td><code>X-Content-Type-Options</code></td><td>Cegah MIME sniffing</td><td>nosniff</td></tr>
<tr><td><code>X-Frame-Options</code></td><td>Cegah clickjacking</td><td>DENY</td></tr>
<tr><td><code>X-XSS-Protection</code></td><td>Filter XSS</td><td>1; mode=block</td></tr>
<tr><td><code>Content-Security-Policy</code></td><td>Resource loading policy</td><td>Disesuaikan</td></tr>
<tr><td><code>Referrer-Policy</code></td><td>Kontrol referrer info</td><td>strict-origin-when-cross-origin</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Header Lainnya yang Penting",
                "content": """<ul>
<li><strong>Content-Type</strong> → Tipe konten (text/html, application/json)</li>
<li><strong>Cache-Control</strong> → Instruksi caching browser</li>
<li><strong>Set-Cookie</strong> → Cookie yang di-set oleh server</li>
<li><strong>Server</strong> → Software server (Apache, Nginx, dll)</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Pastikan ada <strong>HSTS</strong> header untuk website HTTPS</li>
<li>Gunakan <strong>CSP</strong> untuk mencegah XSS attacks</li>
<li>Sembunyikan <strong>Server</strong> header untuk keamanan</li>
<li>Gunakan tool ini untuk audit security headers website kamu</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ssl-checker", "name": "SSL Checker", "icon": "🔒"},
            {"slug": "http-status", "name": "HTTP Status", "icon": "🔢"},
            {"slug": "ping-checker", "name": "Ping Checker", "icon": "📡"}
        ]
    },

    # ============================================================
    # IP TOOLS (3 tools)
    # ============================================================

    "ip_lookup": {
        "title": "📚 Belajar: IP Address & Geolocation",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "📍 Apa itu IP Address?",
                "content": """<p><strong>IP (Internet Protocol) Address</strong> adalah alamat unik yang diberikan ke setiap perangkat di jaringan internet.</p>
<p>Seperti alamat rumah di dunia nyata, IP address memungkinkan data dikirim ke perangkat yang benar.</p>"""
            },
            {
                "heading": "🔢 Jenis IP Address",
                "content": """<div class="edu-table">
<table>
<tr><th>Tipe</th><th>Contoh</th><th>Penggunaan</th></tr>
<tr><td><code>IPv4</code></td><td>192.168.1.1</td><td>Standar, masih umum</td></tr>
<tr><td><code>IPv6</code></td><td>2001:db8::1</td><td>Generasi baru, alamat lebih banyak</td></tr>
<tr><td><code>Public</code></td><td>103.56.12.1</td><td>Terlihat dari internet</td></tr>
<tr><td><code>Private</code></td><td>192.168.x.x, 10.x.x.x</td><td>Hanya di jaringan lokal</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Informasi dari IP Lookup",
                "content": """<ul>
<li><strong>Country/City</strong> → Lokasi geografis IP</li>
<li><strong>ISP</strong> → Penyedia internet yang mengelola IP</li>
<li><strong>Timezone</strong> → Zona waktu lokasi IP</li>
<li><strong>Organisation</strong> → Nama organisasi pemilik IP</li>
<li><strong>ASN</strong> → Autonomous System Number</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>IP public berubah (dynamic) untuk kebanyakan user rumahan</li>
<li>Gunakan VPN untuk mengubah IP public kamu</li>
<li>IP lookup menunjukkan lokasi ISP, bukan lokasi fisik kamu sebenarnya</li>
<li>Private IP tidak bisa di-lookup dari internet</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "asn-lookup", "name": "ASN Lookup", "icon": "🏢"},
            {"slug": "blacklist-checker", "name": "Blacklist Checker", "icon": "🚫"},
            {"slug": "reverse-dns", "name": "Reverse DNS", "icon": "🔄"}
        ]
    },

    "asn_lookup": {
        "title": "📚 Belajar: ASN (Autonomous System Number)",
        "difficulty": "lanjut",
        "sections": [
            {
                "heading": "🏢 Apa itu ASN?",
                "content": """<p><strong>ASN (Autonomous System Number)</strong> adalah nomor unik yang mengidentifikasi jaringan (AS) di internet.</p>
<p>Setiap ISP, perusahaan besar, dan penyedia layanan cloud memiliki ASN sendiri untuk routing BGP.</p>"""
            },
            {
                "heading": "🌐 Cara Kerja BGP & ASN",
                "content": """<ul>
<li><strong>BGP (Border Gateway Protocol)</strong> → Protokol routing antar jaringan di internet</li>
<li><strong>Autonomous System (AS)</strong> → Jaringan yang dikelola oleh satu organisasi</li>
<li><strong>ASN</strong> → Nomor identifikasi untuk setiap AS</li>
</ul>
<p>Tanpa ASN, router internet tidak tahu ke mana mengirim data.</p>"""
            },
            {
                "heading": "📖 Informasi dari ASN Lookup",
                "content": """<ul>
<li><strong>ASN Number</strong> → Nomor unik (contoh: AS13335 untuk Cloudflare)</li>
<li><strong>Organization</strong> → Nama organisasi pemilik ASN</li>
<li><strong>Country</strong> → Negara registrasi ASN</li>
<li><strong>Prefix</strong> → Range IP yang dikelola</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>ASN membantu melihat siapa yang mengelola IP address tertentu</li>
<li>Gunakan untuk investigasi traffic mencurigakan</li>
<li>ASN bisa digunakan untuk GeoIP dan filtering</li>
<li>Beberapa ASN milik ISP besar: Telkom (AS17974), Indosat (AS9919)</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ip-lookup", "name": "IP Lookup", "icon": "📍"},
            {"slug": "blacklist-checker", "name": "Blacklist Checker", "icon": "🚫"},
            {"slug": "reverse-dns", "name": "Reverse DNS", "icon": "🔄"}
        ]
    },

    "blacklist_checker": {
        "title": "📚 Belajar: IP Blacklists (DNSBL)",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🚫 Apa itu IP Blacklist?",
                "content": """<p><strong>IP Blacklist</strong> (juga dikenal sebagai <strong>DNSBL - DNS-based Blackhole List</strong>) adalah daftar IP yang dicurigai melakukan aktivitas spam atau abuse.</p>
<p>Jika IP kamu ada di blacklist, email mungkin tidak terkirim atau masuk spam folder.</p>"""
            },
            {
                "heading": "📋 Blacklist Populer",
                "content": """<div class="edu-table">
<table>
<tr><th>Blacklist</th><th>Fungsi</th><th>Situs</th></tr>
<tr><td><code>Spamhaus SBL</code></td><td>Spam yang dikonfirmasi</td><td>spamhaus.org</td></tr>
<tr><td><code>Spamhaus XBL</code></td><td>Exploited systems</td><td>spamhaus.org</td></tr>
<tr><td><code>SpamCop</code></td><td>Spam reports</td><td>spamcop.net</td></tr>
<tr><td><code>Surbl</code></td><td>Spam URLs</td><td>surbl.org</td></tr>
<tr><td><code>Uceprotect</code></td><td>Abusive networks</td><td>uceprotect.net</td></tr>
</table>
</div>"""
            },
            {
                "heading": "📖 Cara Membaca Hasil",
                "content": """<ul>
<li><strong>Listed</strong> → IP ada di blacklist (bermasalah)</li>
<li><strong>Clean</strong> → IP tidak ada di blacklist (aman)</li>
<li>Setiap blacklist memiliki kriteria berbeda untuk listing</li>
</ul>"""
            },
            {
                "heading": "💡 Tips & Solusi",
                "content": """<ul>
<li>Regular cek blacklist minimal seminggu sekali</li>
<li>Jika IP di-blacklist, cek penyebabnya (spam, malware, open relay)</li>
<li>Request removal di situs blacklist yang bersangkutan</li>
<li>Gunakan dedicated IP untuk email server</li>
<li>Setup SPF, DKIM, DMARC untuk mencegah email masuk spam</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ip-lookup", "name": "IP Lookup", "icon": "📍"},
            {"slug": "asn-lookup", "name": "ASN Lookup", "icon": "🏢"},
            {"slug": "reverse-dns", "name": "Reverse DNS", "icon": "🔄"}
        ]
    },

    # ============================================================
    # NEW TOOLS - FASE 2 (5 tools baru)
    # ============================================================

    "my_ip": {
        "title": "📚 Belajar: IP Address Anda",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🌐 Apa itu IP Address?",
                "content": """<p><strong>IP (Internet Protocol) Address</strong> adalah alamat numerik yang ditetapkan ke setiap perangkat yang terhubung ke jaringan internet.</p>
<p>Pikirkan IP address seperti alamat rumah — ini adalah cara internet mengetahui ke mana mengirim data yang kamu minta.</p>
<ul>
<li><strong>IPv4</strong> → Format 4 angka (contoh: <code>192.168.1.1</code>)</li>
<li><strong>IPv6</strong> → Format panjang hex (contoh: <code>2001:db8::1</code>)</li>
</ul>"""
            },
            {
                "heading": "📋 Informasi yang Bisa Diketahui dari IP",
                "content": """<div class="edu-table">
<table>
<tr><th>Informasi</th><th>Contoh</th><th>Kegunaan</th></tr>
<tr><td>Negara/Kota</td><td>Jakarta, Indonesia</td><td>Geo-location</td></tr>
<tr><td>ISP</td><td>Telkom Indonesia</td><td>Penyedia layanan internet</td></tr>
<tr><td>ASN</td><td>AS17974</td><td>Organisasi jaringan</td></tr>
<tr><td>Timezone</td><td>Asia/Jakarta</td><td>Zona waktu</td></tr>
<tr><td>Organization</td><td>PT Telkom</td><td>Pemilik IP block</td></tr>
</table>
</div>"""
            },
            {
                "heading": "💡 Tips & Pengetahuan",
                "content": """<ul>
<li><strong>Public IP</strong> → IP yang terlihat di internet (dari ISP)</li>
<li><strong>Private IP</strong> → IP lokal (192.168.x.x, 10.x.x.x)</li>
<li><strong>Dynamic IP</strong> → IP berubah-ubah (biasanya home internet)</li>
<li><strong>Static IP</strong> → IP tetap (biasanya server/VPS)</li>
<li>Gunakan VPN untuk mengubah IP public kamu</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ip-lookup", "name": "IP Lookup", "icon": "📍"},
            {"slug": "reverse-dns", "name": "Reverse DNS", "icon": "🔄"},
            {"slug": "asn-lookup", "name": "ASN Lookup", "icon": "🏢"},
            {"slug": "blacklist-checker", "name": "Blacklist Checker", "icon": "🚫"}
        ]
    },

    "ua_checker": {
        "title": "📚 Belajar: User-Agent String",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🖥️ Apa itu User-Agent?",
                "content": """<p><strong>User-Agent</strong> adalah string teks yang dikirim browser ke website untuk mengidentifikasi diri.</p>
<p>Setiap kali kamu membuka website, browser mengirim header User-Agent yang berisi informasi tentang:</p>
<ul>
<li>Nama dan versi browser</li>
<li>Sistem operasi</li>
<li>Jenis device (desktop/mobile/tablet)</li>
<li>Engine rendering (Blink, Gecko, WebKit)</li>
</ul>"""
            },
            {
                "heading": "📋 Contoh User-Agent String",
                "content": """<div class="edu-table">
<table>
<tr><th>Browser</th><th>Contoh UA</th></tr>
<tr><td>Chrome (Windows)</td><td><code>Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0</code></td></tr>
<tr><td>Firefox (macOS)</td><td><code>Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0</code></td></tr>
<tr><td>Safari (iPhone)</td><td><code>Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1</code></td></tr>
<tr><td>Chrome (Android)</td><td><code>Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile</code></td></tr>
</table>
</div>"""
            },
            {
                "heading": "🎯 Mengapa User-Agent Penting?",
                "content": """<ul>
<li><strong>Analytics</strong> → Website tahu pengunjung pakai device apa</li>
<li><strong>Compatibility</strong> → Server mengirim konten yang sesuai device</li>
<li><strong>Security</strong> → Mendeteksi bot atau scraper</li>
<li><strong>Debugging</strong> → Membantu diagnosa masalah browser</li>
<li><strong>Scraping Detection</strong> → Bot sering pakai UA palsu</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"},
            {"slug": "http-status", "name": "HTTP Status", "icon": "🌐"},
            {"slug": "ping-checker", "name": "Ping Checker", "icon": "📡"}
        ]
    },

    "email_validator": {
        "title": "📚 Belajar: Validasi Email",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "📧 Apa itu Validasi Email?",
                "content": """<p><strong>Validasi Email</strong> adalah proses memverifikasi apakah alamat email benar-benar ada dan dapat menerima pesan.</p>
<p>Validasi meliputi beberapa tahap:</p>
<ul>
<li><strong>Cek Format</strong> → Apakah sesuai pola email@domain.com</li>
<li><strong>Cek MX Record</strong> → Apakah domain punya mail server</li>
<li><strong>Cek Disposable</strong> → Apakah email temporary/disposable</li>
<li><strong>SMTP Check</strong> → Apakah mail server benar-benar menerima</li>
</ul>"""
            },
            {
                "heading": "📋 Komponen Email Address",
                "content": """<div class="edu-table">
<table>
<tr><th>Bagian</th><th>Contoh</th><th>Aturan</th></tr>
<tr><td>Local Part</td><td>user.name+tag</td><td>Max 64 karakter</td></tr>
<tr><td>@</td><td>@</td><td>Pemisah wajib</td></tr>
<tr><td>Domain</td><td>gmail.com</td><td>Harus punya MX record</td></tr>
</table>
</div>"""
            },
            {
                "heading": "🚫 Disposable Email",
                "content": """<ul>
<li><strong>Disposable Email</strong> → Email sekali pakai yang biasanya berakhir dalam beberapa menit/jam</li>
<li>Contoh: tempmail.com, mailinator.com, guerrillamail.com</li>
<li>Banyak digunakan untuk daftar akun tanpa ingin menerima email marketing</li>
<li>Beberapa website memblokir email disposable untuk mencegah spam</li>
<li>Skor validasi akan lebih rendah jika menggunakan disposable email</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>MX Record harus ada agar email bisa dikirim ke domain</li>
<li>MX Record dengan priority lebih rendah = server utama</li>
<li>Gunakan email bisnis (@domain.com) untuk profesionalisme</li>
<li>Hindari email temporary untuk akun penting</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "mx-lookup", "name": "MX Lookup", "icon": "📧"},
            {"slug": "spf-checker", "name": "SPF Checker", "icon": "🛡️"},
            {"slug": "dmarc-checker", "name": "DMARC Checker", "icon": "🔐"},
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"}
        ]
    },

    "ns_lookup": {
        "title": "📚 Belajar: Name Server (NS Record)",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🗂️ Apa itu Name Server?",
                "content": """<p><strong>Name Server (NS)</strong> adalah server yang menangani DNS lookup untuk domain.</p>
<p>Ketika kamu mendaftarkan domain, kamu harus menunjuk minimal 2 name server yang akan mengelola DNS record domain kamu.</p>
<ul>
<li><strong>NS1</strong> → Name server utama</li>
<li><strong>NS2</strong> → Name server backup/sekunder</li>
</ul>"""
            },
            {
                "heading": "📋 Contoh NS Records",
                "content": """<div class="edu-table">
<table>
<tr><th>Provider</th><th>NS Records</th></tr>
<tr><td>Cloudflare</td><td><code>ns1.cloudflare.com</code>, <code>ns2.cloudflare.com</code></td></tr>
<tr><td>Google Domains</td><td><code>ns1.googledomains.com</code>, <code>ns2.googledomains.com</code></td></tr>
<tr><td>Namesilo</td><td><code>dns1.p01.nsone.net</code>, <code>dns2.p01.nsone.net</code></td></tr>
<tr><td>Default Registrar</td><td><code>ns1.registrar.com</code>, <code>ns2.registrar.com</code></td></tr>
</table>
</div>"""
            },
            {
                "heading": "🎯 Mengapa NS Lookup Penting?",
                "content": """<ul>
<li><strong>Verifikasi Setup</strong> → Pastikan NS sudah benar setelah pindah provider</li>
<li><strong>Troubleshooting</strong> → Jika website down, cek NS dulu</li>
<li><strong>Keamanan</strong> → Pastikan NS tidak diubah tanpa izin</li>
<li><strong>Migrasi</strong> → Saat pindah hosting, update NS records</li>
</ul>"""
            },
            {
                "heading": "💡 Tips",
                "content": """<ul>
<li>Selalu gunakan minimal 2 NS untuk redundansi</li>
<li>NS propagation bisa memakan waktu 24-48 jam</li>
<li>Jangan pernah menghapus semua NS records sekaligus</li>
<li>Gunakan DNS hosting terpercaya seperti Cloudflare untuk NS gratis</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔍"},
            {"slug": "dns-propagation", "name": "DNS Propagation", "icon": "🌍"},
            {"slug": "whois-lookup", "name": "WHOIS Lookup", "icon": "📋"}
        ]
    },

    "port_scanner": {
        "title": "📚 Belajar: Port Scanning",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "🔍 Apa itu Port Scanning?",
                "content": """<p><strong>Port Scanning</strong> adalah teknik untuk menemukan port terbuka pada host/jaringan.</p>
<p>Setiap layanan internet berjalan di port tertentu. Port scanner membantu mengetahui layanan apa yang aktif di suatu server.</p>
<ul>
<li><strong>Port</strong> → Angka 1-65535 yang merepresentasikan layanan</li>
<li><strong>Open</strong> → Port aktif dan menerima koneksi</li>
<li><strong>Closed</strong> → Port tidak aktif atau diblokir</li>
</ul>"""
            },
            {
                "heading": "📋 Port Populer",
                "content": """<div class="edu-table">
<table>
<tr><th>Port</th><th>Layanan</th><th>Keterangan</th></tr>
<tr><td><code>21</code></td><td>FTP</td><td>File Transfer Protocol</td></tr>
<tr><td><code>22</code></td><td>SSH</td><td>Secure Shell (remote access)</td></tr>
<tr><td><code>25</code></td><td>SMTP</td><td>Simple Mail Transfer (email)</td></tr>
<tr><td><code>53</code></td><td>DNS</td><td>Domain Name System</td></tr>
<tr><td><code>80</code></td><td>HTTP</td><td>Website tanpa SSL</td></tr>
<tr><td><code>443</code></td><td>HTTPS</td><td>Website dengan SSL</td></tr>
<tr><td><code>3306</code></td><td>MySQL</td><td>Database MySQL</td></tr>
<tr><td><code>5432</code></td><td>PostgreSQL</td><td>Database PostgreSQL</td></tr>
<tr><td><code>3389</code></td><td>RDP</td><td>Remote Desktop (Windows)</td></tr>
<tr><td><code>8080</code></td><td>HTTP Alt</td><td>HTTP alternatif/proxy</td></tr>
</table>
</div>"""
            },
            {
                "heading": "🎯 Mengapa Port Scan Penting?",
                "content": """<ul>
<li><strong>Keamanan</strong> → Pastikan hanya port yang diperlukan yang terbuka</li>
<li><strong>Audit</strong> → Cek layanan yang berjalan di server</li>
<li><strong>Troubleshooting</strong> → Kenapa koneksi ke layanan tertentu gagal?</li>
<li><strong>Compliance</strong> → Banyak standar keamanan mensyaratkan port scan</li>
</ul>"""
            },
            {
                "heading": "💡 Tips & Best Practices",
                "content": """<ul>
<li>Batasi scan hanya port yang diperlukan (max 20 port)</li>
<li>Timeout 2 detik sudah cukup untuk sebagian besar port</li>
<li>Hindari scan port yang bukan milik Anda tanpa izin</li>
<li>Gunakan firewall untuk memblokir port yang tidak digunakan</li>
<li>Port 22 (SSH) dan 3389 (RDP) yang terbuka = potensi target brute force</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "ip-lookup", "name": "IP Lookup", "icon": "📍"},
            {"slug": "ping-checker", "name": "Ping Checker", "icon": "📡"},
            {"slug": "blacklist-checker", "name": "Blacklist Checker", "icon": "🚫"}
        ]
    },

    # ============================================================
    # CDN TOOLS (1 tool)
    # ============================================================

    "cdn_detect": {
        "title": "📚 Belajar: Apa itu CDN?",
        "difficulty": "pemula",
        "sections": [
            {
                "heading": "🌐 Apa itu CDN?",
                "content": """<p>CDN <strong>(Content Delivery Network)</strong> adalah jaringan server global yang mendistribusikan konten website lebih dekat ke pengguna.</p>
<p>Bayangkan website Anda di-host di Jakarta, tapi ada pengunjung dari Amerika. Tanpa CDN, data harus menempuh ribuan kilometer. Dengan CDN, konten di-cache di server terdekat.</p>
<p>CDN membantu:</p>
<ul>
<li><strong>Mempercepat</strong> loading website</li>
<li><strong>Mengurangi beban</strong> server utama</li>
<li><strong>Perlindungan</strong> dari serangan DDoS</li>
<li><strong>SSL/TLS</strong> termination</li>
</ul>"""
            },
            {
                "heading": "🔍 Cara Kerja Deteksi CDN",
                "content": """<div class="edu-table">
<table>
<tr><th>Metode</th><th>Penjelasan</th></tr>
<tr><td><strong>CNAME Chain</strong></td><td>Mengecek apakah domain mengarah ke server CDN melalui DNS CNAME record</td></tr>
<tr><td><strong>HTTP Headers</strong></td><td>Mengecek header seperti <code>cf-ray</code> (Cloudflare), <code>x-amz-cf-id</code> (CloudFront)</td></tr>
</table>
</div>
<p>Tool ini menggabungkan kedua metode untuk deteksi yang lebih akurat.</p>"""
            },
            {
                "heading": "🏢 Provider CDN Populer",
                "content": """<div class="edu-table">
<table>
<tr><th>Provider</th><th>CNAME Pattern</th><th>Header Identifier</th></tr>
<tr><td><strong>Cloudflare</strong></td><td><code>*.cloudflare.com</code></td><td><code>cf-ray</code></td></tr>
<tr><td><strong>AWS CloudFront</strong></td><td><code>*.cloudfront.net</code></td><td><code>x-amz-cf-id</code></td></tr>
<tr><td><strong>Akamai</strong></td><td><code>*.akamaiedge.net</code></td><td><code>x-akamai-transformed</code></td></tr>
<tr><td><strong>Fastly</strong></td><td><code>*.fastly.net</code></td><td><code>x-fastly-request-id</code></td></tr>
<tr><td><strong>Azure CDN</strong></td><td><code>*.azureedge.net</code></td><td><code>x-azure-ref</code></td></tr>
<tr><td><strong>StackPath</strong></td><td><code>*.hwcdn.net</code></td><td><code>x-hw</code></td></tr>
</table>
</div>"""
            },
            {
                "heading": "💡 Tips & Best Practices",
                "content": """<ul>
<li>Jika tidak terdeteksi CDN, website mungkin langsung di-host di server asli (direct hosting)</li>
<li>Beberapa website menggunakan CDN tapi tanpa CNAME — deteksi via header lebih akurat</li>
<li>Cloudflare adalah CDN paling populer di Indonesia</li>
<li>CDN gratis tersedia: Cloudflare Free, CloudFront Free Tier, Fastly Free Tier</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "header-checker", "name": "Header Checker", "icon": "📋"},
            {"slug": "cname-lookup", "name": "CNAME Lookup", "icon": "🔗"},
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔧"}
        ]
    },

    # ============================================================
    # BATCH TOOLS
    # ============================================================

    "batch_lookup": {
        "title": "📚 Belajar: Batch Lookup",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "📋 Apa itu Batch Lookup?",
                "content": """<p><strong>Batch Lookup</strong> adalah fitur yang memungkinkan Anda mengecek multiple domain sekaligus dalam satu waktu.</p>
<p>Daripada mengecek satu per satu, Anda bisa memasukkan hingga 10 domain sekaligus dan mendapatkan hasilnya dalam satu tabel ringkas.</p>"""
            },
            {
                "heading": "🎯 Jenis Pengecekan",
                "content": """<div class="edu-table">
<table>
<tr><th>Jenis</th><th>Yang Dicek</th><th>Cocok Untuk</th></tr>
<tr><td><code>DNS</code></td><td>DNS records (A, MX, TXT, dll)</td><td>Cek resolusi DNS multiple domain</td></tr>
<tr><td><code>SSL</code></td><td>Sertifikat SSL validity & issuer</td><td>Audit SSL certificate</td></tr>
<tr><td><code>WHOIS</code></td><td>Informasi registrasi domain</td><td>Cek registrar & expiry date</td></tr>
</table>
</div>"""
            },
            {
                "heading": "💡 Tips Penggunaan",
                "content": """<ul>
<li>Masukkan satu domain per baris di textarea</li>
<li>Maksimal 10 domain per batch untuk menjaga performa</li>
<li>Hasil bisa di-export ke CSV untuk laporan</li>
<li>Cocok untuk audit SSL domain klien atau monitoring DNS</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔧"},
            {"slug": "ssl-checker", "name": "SSL Checker", "icon": "🔒"},
            {"slug": "whois-lookup", "name": "WHOIS Lookup", "icon": "🌍"}
        ]
    },
    "compare": {
        "title": "📚 Belajar: Tool Comparison",
        "difficulty": "menengah",
        "sections": [
            {
                "heading": "⚔️ Apa itu Tool Comparison?",
                "content": """<p><strong>Tool Comparison</strong> adalah fitur yang memungkinkan Anda membandingkan dua domain secara berdampingan dalam satu tampilan.</p>
<p>Daripada mengecek domain satu per satu, Anda bisa langsung melihat perbedaan antara dua domain — cocok untuk membandingkan kompetitor, migrasi domain, atau audit keamanan.</p>"""
            },
            {
                "heading": "🎯 Jenis Perbandingan",
                "content": """<div class="edu-table">
<table>
<tr><th>Jenis</th><th>Yang Dibandingkan</th><th>Cocok Untuk</th></tr>
<tr><td><code>DNS</code></td><td>DNS records (A, MX, TXT, NS, dll)</td><td>Membandingkan konfigurasi DNS</td></tr>
<tr><td><code>SSL</code></td><td>Sertifikat SSL: validity, issuer, expiry</td><td>Audit keamanan TLS</td></tr>
<tr><td><code>WHOIS</code></td><td>Informasi registrasi: registrar, expiry, nameserver</td><td>Perbandingan registrasi domain</td></tr>
</table>
</div>"""
            },
            {
                "heading": "💡 Tips Penggunaan",
                "content": """<ul>
<li>Masukkan domain tanpa <code>https://</code> atau <code>www</code> — cukup <code>example.com</code></li>
<li>Perbedaan akan di-highlight secara otomatis untuk memudahkan analisis</li>
<li>Cocok untuk membandingkan domain kompetitor atau sebelum sesudah migrasi</li>
<li>Hasil bisa di-export ke CSV untuk laporan perbandingan</li>
</ul>"""
            }
        ],
        "related_tools": [
            {"slug": "dns-lookup", "name": "DNS Lookup", "icon": "🔧"},
            {"slug": "ssl-checker", "name": "SSL Checker", "icon": "🔒"},
            {"slug": "whois-lookup", "name": "WHOIS Lookup", "icon": "🌍"},
            {"slug": "batch-lookup", "name": "Batch Lookup", "icon": "📋"}
        ]
    },
}
