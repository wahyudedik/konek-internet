"""Email Validation Service - Validasi email address"""
import re
import asyncio
import logging
from typing import Dict, Any, List

logger = logging.getLogger("konektivitas.email")

# Email regex (RFC 5322 simplified)
_EMAIL_PATTERN = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
)

# Disposable email domains
_DISPOSABLE_DOMAINS = {
    "tempmail.com", "temp-mail.org", "tempail.com", "tempmailo.com",
    "throwaway.email", "guerrillamail.com", "guerrillamail.net",
    "mailinator.com", "yopmail.com", "yopmail.fr", "trashmail.com",
    "trashmail.net", "trashmail.org", "trashmail.me",
    "discard.email", "discardmail.com", "discardmail.de",
    "sharklasers.com", "guerrillamailblock.com",
    "grr.la", "dispostable.com", "maildrop.cc",
    "mailcatch.com", "tempinbox.com", "tempinbox.co.uk",
    "10minutemail.com", "10minutemail.co.uk",
    "getnada.com", "mohmal.com", "fakeinbox.com",
    "harakirimail.com", "tempr.email", "jnxjn.com",
    "spamgourmet.com", "spamcero.com",
    "getairmail.com", "meltmail.com",
    "boun.cr", "bouncr.com",
    "chammy.info", "devnullmail.com",
    "einmalmail.de", "getonemail.net",
    "gowikibooks.com", "gsy.de",
    "h8s.org", "hates-porn.com",
    "ichimail.com", "ie4u.de",
    "lroid.com", "maboard.com",
    "mailzilla.com", "mbt.cc",
    "mega.zik.dj", "meinspamschutz.de",
    "meltmail.com", "nospam.ze.tc",
    "nospamfor.us", "nowmymail.com",
    "owlpic.com", "proxymail.eu",
    "rcpt.at", "reallymymail.com",
    "recode.me", "regbypass.com",
    "rhyta.com", "rklips.com",
    "rmqkr.net", "safetymail.info",
    "sandelf.de", "saynotospams.com",
    "scatmail.com", "schafmail.de",
    "schrott-email.de", "slaskpost.se",
    "slipry.net", "sogetthis.com",
    "soodonims.com", "spamex.com",
    "mailforspam.com", "spamfree24.com",
    "spamfree24.de", "spamfree24.org",
    "spamherelots.com", "spamhereplease.com",
    "spamhole.com", "spamify.com",
    "spaminator.de", "spamkill.info",
    "spaml.com", "spaml.de",
    "spammotel.com", "spamobox.com",
    "spamoff.de", "spamslicer.com",
    "spamspot.com", "spamstack.net",
    "spamthis.co.uk", "spamthisplease.com",
    "spamtrail.com", "spamtrap.ro",
    "speed.1s.fr", "superrito.com",
    "teleworm.us", "tempemail.co.za",
    "tempemail.net", "tempemail.net",
    "tempomail.fr", "temporarily.de",
    "tempthe.net", "thankyou2010.com",
    "thisisnotmyrealemail.com", "throwam.com",
    "tittbit.in", "tizi.com",
    "tmailinator.com", "toiea.com",
    "toomail.biz", "topranklist.com",
    "tradermail.info", "trash-amil.com",
    "trashdevil.com", "trashemail.de",
    "trashymail.com", "trashymail.net",
    "trbvm.com", "trbvn.com",
    "trbvo.com", "trbwv.com",
    "turual.com", "twinmail.de",
    "tyldd.com", "uggsrock.com",
    "umail.net", "upliftnow.com",
    "uplipht.com", "venompen.com",
    "veryrealliemail.com", "vidbucket.info",
    "views.fm", "veryreallyreal.com",
    "vidtag.info", "vinbros.com",
    "vomoto.com", "vpn.st",
    "vsimcard.com", "vubby.com",
    "wasteland.rfc822.org", "webemail.me",
    "weg-werf-email.de", "wegwerfadresse.de",
    "wegwerfemail.com", "wegwerfemail.de",
    "wegwerfmail.de", "wegwerfmail.net",
    "wegwerfmail.org", "wetrainbayarea.com",
    "wetrainbayarea.org", "wh4f.org",
    "whatiaas.com", "whatpaas.com",
    "whyspam.me", "wikidocuslice.com",
    "willhackforfood.biz", "willselfdestruct.com",
    "winemaven.info", "wronghead.com",
    "wuzup.net", "wuzupmail.net",
    "wwwnew.eu", "xagloo.com",
    "xemaps.com", "xents.com",
    "xjoi.com", "xmaily.com",
    "xoxy.net", "zehnminutenmail.de",
    "1chuan.com", "fdfdsfs.com",
    "tempmailer.com", "tempmailer.de",
    "temp-mail.io", "tempmail.pw",
}


def validate_email_format(email: str) -> tuple:
    """Validasi format email"""
    if not email:
        return False, "Email tidak boleh kosong"
    if len(email) > 254:
        return False, "Email terlalu panjang (maksimal 254 karakter)"
    if not _EMAIL_PATTERN.match(email):
        return False, "Format email tidak valid"
    return True, None


def _get_domain(email: str) -> str:
    """Extract domain from email"""
    if "@" not in email:
        return email.lower()
    return email.split("@")[1].lower()


def _is_disposable(email: str) -> bool:
    """Cek apakah email menggunakan disposable domain"""
    domain = _get_domain(email)
    return domain in _DISPOSABLE_DOMAINS


def _check_mx_sync(domain: str) -> List[Dict[str, Any]]:
    """Blocking MX record lookup"""
    import dns.resolver
    mx_records = []
    try:
        answers = dns.resolver.resolve(domain, "MX", lifetime=10)
        for rdata in answers:
            mx_records.append({
                "priority": rdata.preference,
                "host": str(rdata.exchange).rstrip("."),
            })
        # Sort by priority
        mx_records.sort(key=lambda x: x["priority"])
    except dns.resolver.NXDOMAIN:
        pass
    except dns.resolver.NoAnswer:
        pass
    except dns.resolver.NoNameservers:
        pass
    except Exception as e:
        logger.warning("MX lookup error for %s: %s", domain, str(e))
    return mx_records


def _smtp_check_sync(domain: str, mx_host: str) -> bool:
    """Blocking SMTP connect check (optional)"""
    import socket
    try:
        sock = socket.create_connection((mx_host, 25), timeout=5)
        banner = sock.recv(1024).decode("utf-8", errors="ignore")
        sock.close()
        return banner.startswith("220")
    except Exception:
        return False


async def validate_email(email: str) -> Dict[str, Any]:
    """Validasi email lengkap: format, MX, disposable"""
    email = email.strip().lower()
    domain = _get_domain(email)

    result = {
        "email": email,
        "format_valid": True,
        "domain": domain,
        "mx_valid": False,
        "mx_records": [],
        "disposable": _is_disposable(email),
        "smtp_valid": False,
        "score": 0,
        "verdict": "",
    }

    # MX lookup
    try:
        mx_records = await asyncio.to_thread(_check_mx_sync, domain)
        result["mx_records"] = mx_records
        result["mx_valid"] = len(mx_records) > 0
    except Exception as e:
        logger.warning("MX lookup failed: %s", str(e))

    # SMTP check (optional, only if MX exists)
    if result["mx_valid"] and mx_records:
        try:
            smtp_ok = await asyncio.to_thread(
                _smtp_check_sync, domain, mx_records[0]["host"]
            )
            result["smtp_valid"] = smtp_ok
        except Exception:
            pass

    # Calculate score
    score = 0
    if result["format_valid"]:
        score += 30
    if result["mx_valid"]:
        score += 40
    if result["smtp_valid"]:
        score += 20
    if not result["disposable"]:
        score += 10

    result["score"] = score

    # Verdict
    if score >= 90:
        result["verdict"] = "Sangat Baik"
    elif score >= 70:
        result["verdict"] = "Baik"
    elif score >= 50:
        result["verdict"] = "Cukup"
    else:
        result["verdict"] = "Diragukan"

    return result
