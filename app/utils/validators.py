"""Input validation utilities untuk Konektivitas.com"""
import re
from typing import Optional, Tuple

# Regex patterns
_DOMAIN_PATTERN = re.compile(
    r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.){1,127}[a-zA-Z]{2,}$'
)

_IPV4_PATTERN = re.compile(
    r'^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$'
)

_IPV6_PATTERN = re.compile(
    r'^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$|'
    r'^(?:[0-9a-fA-F]{1,4}:){1,7}:|'
    r'^(?:[0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}$|'
    r'^::(?:[0-9a-fA-F]{1,4}:){0,5}[0-9a-fA-F]{1,4}$'
)

_URL_PATTERN = re.compile(
    r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE
)


def validate_domain(domain: str) -> Tuple[bool, Optional[str]]:
    """
    Validate domain name.
    Returns (is_valid, error_message)
    """
    domain = domain.strip().lower()
    
    if not domain:
        return False, "Domain tidak boleh kosong"
    
    if len(domain) > 253:
        return False, "Domain terlalu panjang (maksimal 253 karakter)"
    
    if not _DOMAIN_PATTERN.match(domain):
        return False, "Format domain tidak valid"
    
    # Check for common mistakes
    if '://' in domain:
        return False, "Masukkan domain saja, tanpa http:// atau https://"
    
    if '/' in domain:
        return False, "Masukkan domain saja, tanpa path"
    
    return True, None


def validate_ip(ip_address: str) -> Tuple[bool, Optional[str]]:
    """
    Validate IP address (IPv4 or IPv6).
    Returns (is_valid, error_message)
    """
    ip_address = ip_address.strip()
    
    if not ip_address:
        return False, "IP address tidak boleh kosong"
    
    if _IPV4_PATTERN.match(ip_address):
        return True, None
    
    if _IPV6_PATTERN.match(ip_address):
        return True, None
    
    return False, "Format IP address tidak valid"


def validate_url(url: str) -> Tuple[bool, Optional[str]]:
    """
    Validate URL.
    Returns (is_valid, error_message)
    """
    url = url.strip()
    
    if not url:
        return False, "URL tidak boleh kosong"
    
    if len(url) > 2048:
        return False, "URL terlalu panjang (maksimal 2048 karakter)"
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    if _URL_PATTERN.match(url):
        return True, None
    
    return False, "Format URL tidak valid"


def validate_host(host: str) -> Tuple[bool, Optional[str]]:
    """
    Validate host (can be domain or IP).
    Returns (is_valid, error_message)
    """
    host = host.strip()
    
    if not host:
        return False, "Host tidak boleh kosong"
    
    # Try IP first
    if _IPV4_PATTERN.match(host) or _IPV6_PATTERN.match(host):
        return True, None
    
    # Try domain
    if _DOMAIN_PATTERN.match(host):
        return True, None
    
    return False, "Format host tidak valid (gunakan domain atau IP address)"


def sanitize_input(text: str, max_length: int = 255) -> str:
    """Sanitize user input - trim, limit length, remove null bytes"""
    if not text:
        return ""
    
    text = text.strip()
    text = text.replace('\x00', '')  # Remove null bytes
    
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


# Tool metadata untuk SEO - setiap tool punya metadata unik
TOOL_META = {
    "dns_lookup": {
        "title": "DNS Lookup - Cek DNS Records Gratis",
        "description": "Query DNS records (A, AAAA, MX, TXT, CNAME, NS) untuk domain apapun secara gratis dan cepat.",
        "keywords": "dns lookup, dns records, a record, aaaa record, mx record, txt record, cname, ns record, query dns",
        "category": "DNS",
        "icon": "🔧",
    },
    "reverse_dns": {
        "title": "Reverse DNS Lookup - IP ke Domain",
        "description": "Lookup IP address untuk menemukan hostname yang terkait. Reverse DNS check gratis.",
        "keywords": "reverse dns, ptr record, ip to domain, reverse lookup, dns reverse",
        "category": "DNS",
        "icon": "🔧",
    },
    "dns_propagation": {
        "title": "DNS Propagation Checker - Cek DNS Global",
        "description": "Cek propagasi DNS dari 7 nameserver global: Google, Cloudflare, OpenDNS, Quad9.",
        "keywords": "dns propagation, dns checker, nameserver, google dns, cloudflare dns, opendns, quad9",
        "category": "DNS",
        "icon": "🔧",
    },
    "mx_lookup": {
        "title": "MX Lookup - Cek Mail Exchange Records",
        "description": "Cek Mail Exchange records untuk konfigurasi email domain Anda.",
        "keywords": "mx lookup, mail exchange, mx record, email server, smtp, mail server",
        "category": "DNS",
        "icon": "🔧",
    },
    "txt_lookup": {
        "title": "TXT Lookup - Cek TXT Records",
        "description": "Cek TXT records termasuk SPF, DKIM, dan verifikasi domain.",
        "keywords": "txt lookup, txt record, spf record, dkim, domain verification, text record",
        "category": "DNS",
        "icon": "🔧",
    },
    "cname_lookup": {
        "title": "CNAME Lookup - Cek Canonical Name Records",
        "description": "Cek Canonical Name records dan alias domain.",
        "keywords": "cname lookup, cname record, canonical name, alias domain, cdn",
        "category": "DNS",
        "icon": "🔧",
    },
    "spf_checker": {
        "title": "SPF Checker - Validasi SPF Records",
        "description": "Validasi Sender Policy Framework records untuk keamanan email.",
        "keywords": "spf checker, spf record, sender policy framework, email security, spf validation",
        "category": "DNS",
        "icon": "🔧",
    },
    "dmarc_checker": {
        "title": "DMARC Checker - Validasi DMARC Policies",
        "description": "Validasi DMARC policies untuk keamanan email dan anti-spoofing.",
        "keywords": "dmarc checker, dmarc record, dmarc policy, email security, anti-spoofing",
        "category": "DNS",
        "icon": "🔧",
    },
    "whois_lookup": {
        "title": "WHOIS Lookup - Informasi Registrasi Domain",
        "description": "Informasi lengkap registrasi domain: registrar, tanggal registrasi, expiry, nameserver.",
        "keywords": "whois lookup, whois domain, domain registration, registrar, nameserver, domain info",
        "category": "Domain",
        "icon": "🌍",
    },
    "domain_expiry": {
        "title": "Domain Expiry Checker - Cek Masa Aktif Domain",
        "description": "Cek sisa waktu aktif domain dan dapatkan peringatan sebelum expired.",
        "keywords": "domain expiry, domain expiring, domain active, domain status, domain check",
        "category": "Domain",
        "icon": "🌍",
    },
    "ssl_checker": {
        "title": "SSL Checker - Verifikasi Sertifikat SSL",
        "description": "Verifikasi sertifikat SSL: issuer, expiry, validity, dan detail lainnya.",
        "keywords": "ssl checker, ssl certificate, https, tls, ssl verification, certificate check",
        "category": "SSL",
        "icon": "🔒",
    },
    "ssl_expiry": {
        "title": "SSL Expiry Checker - Cek Masa Aktif SSL",
        "description": "Cek sisa waktu aktif sertifikat SSL sebelum perlu diperbarui.",
        "keywords": "ssl expiry, ssl expiring, certificate expiry, ssl valid, https certificate",
        "category": "SSL",
        "icon": "🔒",
    },
    "ping_checker": {
        "title": "Ping Checker - Uji Konektivitas Server",
        "description": "Uji konektivitas dan response time ke server website.",
        "keywords": "ping checker, ping test, server ping, latency, response time, connectivity",
        "category": "Website",
        "icon": "🌐",
    },
    "http_status": {
        "title": "HTTP Status Checker - Cek Status HTTP",
        "description": "Cek status HTTP response (200, 301, 404, 500, dll) dari website.",
        "keywords": "http status, http checker, status code, 200, 301, 404, 500, http response",
        "category": "Website",
        "icon": "🌐",
    },
    "redirect_checker": {
        "title": "Redirect Checker - Lacak Redirect Chains",
        "description": "Lacak rantai redirect dari URL awal ke URL final.",
        "keywords": "redirect checker, redirect chain, 301 redirect, 302 redirect, url redirect",
        "category": "Website",
        "icon": "🌐",
    },
    "header_checker": {
        "title": "Header Checker - Analisis HTTP Headers",
        "description": "Analisis HTTP headers: Content-Type, Cache-Control, Security headers.",
        "keywords": "http header, header checker, content-type, cache-control, security headers",
        "category": "Website",
        "icon": "🌐",
    },
    "ip_lookup": {
        "title": "IP Lookup - Informasi Lengkap IP Address",
        "description": "Informasi lengkap IP address: lokasi, ISP, timezone, organisasi.",
        "keywords": "ip lookup, ip address, ip info, location, isp, geolocation, ip check",
        "category": "IP",
        "icon": "📡",
    },
    "asn_lookup": {
        "title": "ASN Lookup - Cek Autonomous System Number",
        "description": "Cek Autonomous System Number dan organisasi jaringan.",
        "keywords": "asn lookup, autonomous system, asn number, network org, bgp, routing",
        "category": "IP",
        "icon": "📡",
    },
    "blacklist_checker": {
        "title": "Blacklist Checker - Cek IP Blacklist",
        "description": "Cek apakah IP address ada di blacklist email/abuse.",
        "keywords": "blacklist checker, ip blacklist, spamhaus, spam check, abuse, dnsbl",
        "category": "IP",
        "icon": "📡",
    },
    "my_ip": {
        "title": "My IP Address - Cek IP Address Anda",
        "description": "Deteksi dan cek detail IP address Anda saat ini termasuk lokasi, ISP, dan ASN",
        "keywords": "my ip, ip address saya, cek ip, what is my ip",
        "category": "IP",
        "icon": "🌐",
    },
    "ua_checker": {
        "title": "User-Agent Checker - Deteksi Browser & Device",
        "description": "Parse dan analisis User-Agent string untuk mendeteksi browser, OS, dan device",
        "keywords": "user agent, browser detector, ua checker, device detection",
        "category": "Website",
        "icon": "🖥️",
    },
    "email_validator": {
        "title": "Email Validator - Cek Validitas Email",
        "description": "Validasi email address termasuk format, MX record, dan deteksi disposable email",
        "keywords": "email validator, email checker, valid email, mx lookup",
        "category": "IP",
        "icon": "📧",
    },
    "ns_lookup": {
        "title": "NS Lookup - Cek Name Server",
        "description": "Lookup name server (NS record) untuk domain guna mengetahui DNS server yang digunakan",
        "keywords": "ns lookup, name server, dns server, ns record",
        "category": "DNS",
        "icon": "🗂️",
    },
    "port_scanner": {
        "title": "Port Scanner - Cek Port Terbuka",
        "description": "Scan port TCP pada host untuk mengetahui port yang terbuka dan layanan yang berjalan",
        "keywords": "port scanner, open port, tcp scan, port check",
        "category": "IP",
        "icon": "🔍",
    },
    "cdn_detect": {
        "title": "CDN Detection - Deteksi Provider CDN",
        "description": "Deteksi apakah website menggunakan CDN dan identifikasi providernya: Cloudflare, CloudFront, Akamai, Fastly.",
        "keywords": "cdn detection, detect cdn, cdn checker, cloudflare, cloudfront, akamai, fastly, cdn provider",
        "category": "Website",
        "icon": "🌐",
    },
}


def get_tool_meta(tool_key: str) -> dict:
    """Get metadata for a specific tool"""
    return TOOL_META.get(tool_key, {
        "title": "Konektivitas.com",
        "description": "Infrastruktur Internet Gratis untuk Indonesia",
        "keywords": "dns lookup, whois, ssl checker, ip lookup, tools internet, indonesia",
        "category": "",
        "icon": "🌐",
    })
