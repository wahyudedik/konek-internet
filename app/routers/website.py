from fastapi import APIRouter
import httpx

router = APIRouter()


@router.get("/ping/{domain}")
async def ping_checker(domain: str):
    """Ping Checker - Uji konektivitas ke server"""
    results = {
        "domain": domain,
        "reachable": False,
        "response_time_ms": None,
        "status_code": None,
        "error": None
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://{domain}", timeout=10.0)
            results["reachable"] = True
            results["status_code"] = response.status_code
            results["response_time_ms"] = response.elapsed.total_seconds() * 1000
    except httpx.TimeoutException:
        results["error"] = "Timeout"
    except httpx.ConnectError:
        results["error"] = "Koneksi gagal"
    except Exception as e:
        results["error"] = str(e)
    
    return results


@router.get("/http-status/{domain}")
async def http_status(domain: str):
    """HTTP Status Checker - Cek status HTTP response"""
    results = {
        "domain": domain,
        "status_code": None,
        "status_text": None,
        "error": None
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://{domain}", timeout=10.0)
            results["status_code"] = response.status_code
            results["status_text"] = response.reason_phrase
    except Exception as e:
        results["error"] = str(e)
    
    return results


@router.get("/redirect/{domain}")
async def redirect_checker(domain: str):
    """Redirect Checker - Lacak redirect chains"""
    results = {
        "domain": domain,
        "redirects": [],
        "final_url": None,
        "error": None
    }
    
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(f"https://{domain}", timeout=10.0)
            
            # Catat semua redirect
            for resp in response.history:
                results["redirects"].append({
                    "url": str(resp.url),
                    "status_code": resp.status_code
                })
            
            results["final_url"] = str(response.url)
            results["final_status"] = response.status_code
    except Exception as e:
        results["error"] = str(e)
    
    return results


@router.get("/headers/{domain}")
async def header_checker(domain: str):
    """Header Checker - Analisis HTTP headers"""
    results = {
        "domain": domain,
        "headers": {},
        "error": None
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://{domain}", timeout=10.0)
            results["headers"] = dict(response.headers)
    except Exception as e:
        results["error"] = str(e)
    
    return results