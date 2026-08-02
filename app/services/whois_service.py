import whois
import logging
from typing import Dict, Any
from datetime import datetime
from app.utils.cache import cached

logger = logging.getLogger("konektivitas.whois")


@cached(ttl=3600)
async def lookup_whois(domain: str) -> Dict[str, Any]:
    """WHOIS Lookup - Informasi registrasi domain"""
    return await _whois_raw(domain)


@cached(ttl=3600)
async def check_domain_expiry(domain: str) -> Dict[str, Any]:
    """Domain Expiry Checker - Cek masa aktif domain"""
    results = await _whois_raw(domain)
    
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


async def _whois_raw(domain: str) -> Dict[str, Any]:
    """Internal WHOIS lookup tanpa caching"""
    import asyncio
    
    results = {
        "domain": domain,
        "registrar": None,
        "creation_date": None,
        "expiration_date": None,
        "updated_date": None,
        "name_servers": [],
        "status": [],
        "registrant": None,
        "admin_contact": None,
        "tech_contact": None,
        "error": None
    }
    
    def _whois_sync():
        logger.debug("WHOIS lookup for: %s", domain)
        return whois.whois(domain)
    
    try:
        w = await asyncio.to_thread(_whois_sync)
        results["registrar"] = w.registrar
        
        # Creation date
        if w.creation_date:
            if isinstance(w.creation_date, list):
                results["creation_date"] = w.creation_date[0].isoformat()
            else:
                results["creation_date"] = w.creation_date.isoformat()
        
        # Expiration date
        if w.expiration_date:
            if isinstance(w.expiration_date, list):
                results["expiration_date"] = w.expiration_date[0].isoformat()
            else:
                results["expiration_date"] = w.expiration_date.isoformat()
        
        # Updated date
        updated = getattr(w, 'updated_date', None) or getattr(w, 'last_updated', None)
        if updated:
            if isinstance(updated, list):
                results["updated_date"] = updated[0].isoformat() if updated[0] else None
            else:
                results["updated_date"] = updated.isoformat()
        
        # Name servers
        if w.name_servers:
            results["name_servers"] = list(set(w.name_servers))
        
        # Status
        if w.status:
            if isinstance(w.status, list):
                results["status"] = list(set(w.status))
            else:
                results["status"] = [w.status]
        
        # Registrant info
        registrant_name = getattr(w, 'name', None) or getattr(w, 'registrant_name', None)
        registrant_org = getattr(w, 'org', None) or getattr(w, 'registrant_organization', None)
        registrant_email = getattr(w, 'emails', None)
        if isinstance(registrant_email, list):
            registrant_email = registrant_email[0] if registrant_email else None
        registrant_country = getattr(w, 'country', None)
        
        results["registrant"] = {
            "name": registrant_name,
            "organization": registrant_org,
            "email": registrant_email,
            "country": registrant_country,
        }
        
        # Admin contact
        admin_name = getattr(w, 'admin_name', None)
        admin_email = getattr(w, 'admin_email', None)
        results["admin_contact"] = {
            "name": admin_name,
            "email": admin_email,
        }
        
        # Tech contact
        tech_name = getattr(w, 'tech_name', None)
        tech_email = getattr(w, 'tech_email', None)
        results["tech_contact"] = {
            "name": tech_name,
            "email": tech_email,
        }
        
    except Exception as e:
        results["error"] = str(e)
    
    return results
