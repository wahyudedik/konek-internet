"""Port Scanner Service - Basic TCP port scan"""
import asyncio
import logging
from typing import Dict, Any, List

logger = logging.getLogger("konektivitas.port")

# Common service names
SERVICE_NAMES = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPCBind",
    135: "MSRPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    27017: "MongoDB",
}

# Port presets
PORT_PRESETS = {
    "common": [21, 22, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 3389, 5432, 8080, 8443],
    "web": [80, 443, 8080, 8443],
    "mail": [25, 110, 143, 993, 995],
    "database": [3306, 5432, 1433, 1521, 27017, 6379],
    "remote": [22, 23, 3389, 5900],
}


def _get_service_name(port: int) -> str:
    """Get service name for a port"""
    return SERVICE_NAMES.get(port, "unknown")


async def _check_port(host: str, port: int, timeout: float = 2.0) -> Dict[str, Any]:
    """Check single port"""
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout,
        )
        writer.close()
        await writer.wait_closed()
        return {
            "port": port,
            "status": "open",
            "service": _get_service_name(port),
        }
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return {
            "port": port,
            "status": "closed",
            "service": _get_service_name(port),
        }
    except Exception:
        return {
            "port": port,
            "status": "closed",
            "service": _get_service_name(port),
        }


async def scan_ports(host: str, ports: List[int]) -> Dict[str, Any]:
    """Scan multiple ports async"""
    results = {
        "host": host,
        "ports_scanned": len(ports),
        "open_ports": 0,
        "closed_ports": 0,
        "results": [],
        "error": None,
    }

    try:
        # Scan all ports concurrently
        tasks = [_check_port(host, port) for port in ports]
        port_results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in port_results:
            if isinstance(result, Exception):
                continue
            results["results"].append(result)
            if result["status"] == "open":
                results["open_ports"] += 1
            else:
                results["closed_ports"] += 1

        # Sort by port number
        results["results"].sort(key=lambda x: x["port"])

    except Exception as e:
        results["error"] = str(e)
        logger.error("Port scan error for %s: %s", host, str(e))

    return results
