import ssl
import socket
from typing import Dict, Any
from datetime import datetime


async def check_ssl(domain: str) -> Dict[str, Any]:
    """SSL Checker - Verifikasi sertifikat SSL"""
    results = {
        "domain": domain,
        "valid": False,
        "issuer": None,
        "subject": None,
        "not_before": None,
        "not_after": None,
        "serial_number": None,
        "error": None
    }
    
    try:
        context = ssl.create_default_context()
        
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                
                results["valid"] = True
                results["issuer"] = dict(x[0] for x in cert.get("issuer", []))
                results["subject"] = dict(x[0] for x in cert.get("subject", []))
                results["serial_number"] = cert.get("serialNumber")
                
                not_before = cert.get("notBefore")
                not_after = cert.get("notAfter")
                
                if not_before:
                    results["not_before"] = not_before
                if not_after:
                    results["not_after"] = not_after
                    
    except ssl.SSLCertVerificationError as e:
        results["error"] = f"SSL verification gagal: {str(e)}"
    except socket.timeout:
        results["error"] = "Timeout saat koneksi ke server"
    except socket.gaierror:
        results["error"] = "Domain tidak dapat diresolve"
    except ConnectionRefusedError:
        results["error"] = "Koneksi ditolak pada port 443"
    except Exception as e:
        results["error"] = str(e)
    
    return results


async def check_ssl_expiry(domain: str) -> Dict[str, Any]:
    """SSL Expiry Checker - Cek masa aktif SSL"""
    results = await check_ssl(domain)
    
    if results.get("not_after"):
        try:
            # Parse format SSL certificate date
            expiry_str = results["not_after"]
            exp_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z")
            now = datetime.utcnow()
            days_left = (exp_date - now).days
            
            results["days_until_expiry"] = days_left
            results["is_expired"] = days_left < 0
            results["is_expiring_soon"] = 0 <= days_left <= 30
        except Exception as e:
            results["error"] = f"Gagal menghitung masa aktif SSL: {str(e)}"
    
    return results