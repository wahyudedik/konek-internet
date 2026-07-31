import whois
from typing import Dict, Any
from datetime import datetime


async def lookup_whois(domain: str) -> Dict[str, Any]:
    """WHOIS Lookup - Informasi registrasi domain"""
    results = {
        "domain": domain,
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "name_servers": [],
        "status": [],
        "error": None
    }
    
    try:
        w = whois.whois(domain)
        
        results["registrar"] = w.registrar
        
        if w.creation_date:
            if isinstance(w.creation_date, list):
                results["creation_date"] = w.creation_date[0].isoformat()
            else:
                results["creation_date"] = w.creation_date.isoformat()
        
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                results["expiration_date"] = w.expiration_date[0].isoformat()
            else:
                results["expiration_date"] = w.expiration_date.isoformat()
        
        if w.name_servers:
            results["name_servers"] = list(w.name_servers)
        
        if w.status:
            if isinstance(w.status, list):
                results["status"] = w.status
            else:
                results["status"] = [w.status]
        
    except Exception as e:
        results["error"] = str(e)
    
    return results


async def check_domain_expiry(domain: str) -> Dict[str, Any]:
    """Domain Expiry Checker - Cek masa aktif domain"""
    results = await lookup_whois(domain)
    
    if results["expiration_date"]:
        try:
            exp_date = datetime.fromisoformat(results["expiration_date"])
            now = datetime.now()
            days_left = (exp_date - now).days
            
            results["days_until_expiry"] = days_left
            results["is_expired"] = days_left < 0
            results["is_expiring_soon"] = 0 <= days_left <= 30
        except Exception as e:
            results["error"] = f"Gagal menghitung masa aktif: {str(e)}"
    
    return results