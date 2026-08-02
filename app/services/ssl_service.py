import ssl
import socket
import logging
from typing import Dict, Any
from datetime import datetime, timezone
from app.utils.cache import cached

logger = logging.getLogger("konektivitas.ssl")


@cached(ttl=3600)
async def check_ssl(domain: str) -> Dict[str, Any]:
    """SSL Checker - Verifikasi sertifikat SSL dengan chain info"""
    import asyncio
    
    results = {
        "domain": domain,
        "valid": False,
        "issuer": None,
        "subject": None,
        "not_before": None,
        "not_after": None,
        "serial_number": None,
        "subject_alt_names": [],
        "signature_algorithm": None,
        "chain": None,
        "error": None
    }
    
    def _ssl_sync():
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                # Get DER cert for chain info
                der_cert = ssock.getpeercert(True)
                return {
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "subject": dict(x[0] for x in cert.get("subject", [])),
                    "serial_number": cert.get("serialNumber"),
                    "not_before": cert.get("notBefore"),
                    "not_after": cert.get("notAfter"),
                    "subject_alt_names": _extract_sans(cert),
                    "has_chain": der_cert is not None,
                }
    
    try:
        cert_info = await asyncio.to_thread(_ssl_sync)
        results["valid"] = True
        results["issuer"] = cert_info["issuer"]
        results["subject"] = cert_info["subject"]
        results["serial_number"] = cert_info["serial_number"]
        results["not_before"] = cert_info["not_before"]
        results["not_after"] = cert_info["not_after"]
        results["subject_alt_names"] = cert_info["subject_alt_names"]
        results["signature_algorithm"] = await asyncio.to_thread(_get_signature_algorithm, domain)
        
        # Chain info
        chain_info = await asyncio.to_thread(_get_chain_info, domain)
        results["chain"] = chain_info
        
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


@cached(ttl=3600)
async def check_ssl_expiry(domain: str) -> Dict[str, Any]:
    """SSL Expiry Checker - Cek masa aktif SSL"""
    results = await _ssl_raw(domain)
    
    if results.get("not_after"):
        try:
            expiry_str = results["not_after"]
            exp_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            days_left = (exp_date - now).days
            
            results["days_until_expiry"] = days_left
            results["is_expired"] = days_left < 0
            results["is_expiring_soon"] = 0 <= days_left <= 30
        except Exception as e:
            results["error"] = f"Gagal menghitung masa aktif SSL: {str(e)}"
    
    return results


async def _ssl_raw(domain: str) -> Dict[str, Any]:
    """Internal SSL check tanpa caching"""
    import asyncio
    
    results = {
        "domain": domain,
        "valid": False,
        "issuer": None,
        "subject": None,
        "not_before": None,
        "not_after": None,
        "serial_number": None,
        "subject_alt_names": [],
        "signature_algorithm": None,
        "chain": None,
        "error": None
    }
    
    def _ssl_sync():
        logger.debug("Checking SSL for: %s", domain)
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                return {
                    "issuer": dict(x[0] for x in cert.get("issuer", [])),
                    "subject": dict(x[0] for x in cert.get("subject", [])),
                    "serial_number": cert.get("serialNumber"),
                    "not_before": cert.get("notBefore"),
                    "not_after": cert.get("notAfter"),
                    "subject_alt_names": _extract_sans(cert),
                }
    
    try:
        cert_info = await asyncio.to_thread(_ssl_sync)
        results["valid"] = True
        results.update(cert_info)
        results["signature_algorithm"] = await asyncio.to_thread(_get_signature_algorithm, domain)
        
        chain_info = await asyncio.to_thread(_get_chain_info, domain)
        results["chain"] = chain_info
    except Exception as e:
        results["error"] = str(e)
    
    return results


def _extract_sans(cert: dict) -> list:
    """Extract Subject Alternative Names from certificate"""
    sans = []
    for ext in cert.get('subjectAltName', ()):
        if isinstance(ext, tuple) and len(ext) >= 2:
            sans.append(ext[1])
    return sans


def _get_signature_algorithm(domain: str) -> str:
    """Get signature algorithm from SSL certificate"""
    try:
        import subprocess
        result = subprocess.run(
            ['openssl', 's_client', '-connect', f'{domain}:443', '-servername', domain],
            input=b'',
            capture_output=True,
            timeout=10
        )
        cert_text = result.stdout.decode('utf-8', errors='ignore')
        for line in cert_text.split('\n'):
            if 'Signature Algorithm:' in line:
                return line.split('Signature Algorithm:')[1].strip()
    except Exception:
        pass
    
    # Fallback: try with ssl module
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cipher = ssock.cipher()
                if cipher:
                    return cipher[1] if len(cipher) > 1 else "Unknown"
    except Exception:
        pass
    
    return None


def _get_chain_info(domain: str) -> dict:
    """Get certificate chain information"""
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                chain = ssock.getpeercert(True)
                cipher_info = ssock.cipher()
                # Decode DER certificate to get issuer info
                issuer_info = None
                try:
                    import cryptography.x509
                    cert_der = ssock.getpeercert(binary_form=True)
                    if cert_der:
                        cert = cryptography.x509.load_der_x509_certificate(cert_der)
                        issuer_info = ", ".join(
                            f"{attr.oid._name}={attr.value}"
                            for attr in cert.issuer
                        )
                except Exception:
                    pass
                
                return {
                    "has_chain": chain is not None,
                    "cipher": cipher_info[0] if cipher_info else None,
                    "cipher_version": cipher_info[1] if cipher_info else None,
                    "cipher_bits": cipher_info[2] if cipher_info else None,
                    "issuer": issuer_info,
                }
    except Exception:
        return {"has_chain": False, "cipher": None, "cipher_version": None, "cipher_bits": None, "issuer": None}
