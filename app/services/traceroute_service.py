"""Traceroute service - Trace route ke server tujuan"""
import asyncio
import logging
import platform
import re
import socket
import subprocess
from typing import Dict, Any, List
from app.utils.cache import cached

logger = logging.getLogger("konektivitas.traceroute")


def _resolve_hostname_sync(ip: str) -> str:
    """Synchronous reverse DNS lookup"""
    try:
        return socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror, OSError):
        return None


@cached(ttl=300)
async def traceroute(host: str, max_hops: int = 30) -> Dict[str, Any]:
    """
    Traceroute - Trace routing path ke server tujuan.
    Menggunakan OS command (tracert di Windows, traceroute di Linux/Mac).
    """
    # Resolve hostname first
    try:
        ip_address = await asyncio.to_thread(socket.gethostbyname, host)
    except socket.gaierror:
        return {
            "host": host,
            "ip_address": None,
            "hops": [],
            "error": f"Tidak dapat resolve hostname: {host}",
        }

    system = platform.system().lower()

    try:
        if system == "windows":
            hops = await _traceroute_windows(host, max_hops)
        else:
            hops = await _traceroute_unix(host, max_hops)

        # Resolve hostnames for all hops (async)
        for hop in hops:
            if hop.get("ip"):
                hop["hostname"] = await asyncio.to_thread(_resolve_hostname_sync, hop["ip"])

        return {
            "host": host,
            "ip_address": ip_address,
            "total_hops": len(hops),
            "hops": hops,
            "error": None,
        }
    except asyncio.TimeoutError:
        return {
            "host": host,
            "ip_address": ip_address,
            "hops": [],
            "error": "Traceroute timeout (>60 detik)",
        }
    except Exception as e:
        return {
            "host": host,
            "ip_address": ip_address,
            "hops": [],
            "error": f"Error: {str(e)}",
        }


def _run_tracert_sync(host: str, max_hops: int) -> str:
    """Run tracert synchronously (for use with asyncio.to_thread)"""
    cmd = ["tracert", "-d", "-h", str(max_hops), "-w", "3000", host]
    logger.debug("Running: %s", " ".join(cmd))
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=90,
        encoding="utf-8",
        errors="replace",
    )
    logger.debug("tracert exit code: %d, stdout length: %d", result.returncode, len(result.stdout))
    if result.stdout:
        logger.debug("tracert output preview: %s", result.stdout[:200])
    if result.stderr:
        logger.warning("tracert stderr: %s", result.stderr[:200])
    return result.stdout


def _run_traceroute_sync(host: str, max_hops: int) -> str:
    """Run traceroute synchronously (for use with asyncio.to_thread)"""
    cmd = ["traceroute", "-n", "-m", str(max_hops), "-w", "3", host]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=90,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout


async def _traceroute_windows(host: str, max_hops: int) -> List[dict]:
    """Run tracert on Windows via asyncio.to_thread"""
    output = await asyncio.to_thread(_run_tracert_sync, host, max_hops)
    return _parse_tracert_output(output)


async def _traceroute_unix(host: str, max_hops: int) -> List[dict]:
    """Run traceroute on Linux/Mac via asyncio.to_thread"""
    output = await asyncio.to_thread(_run_traceroute_sync, host, max_hops)
    return _parse_traceroute_output(output)


def _parse_tracert_output(output: str) -> List[dict]:
    """Parse Windows tracert output.
    
    Format:
      1     2 ms     2 ms     2 ms  192.168.1.1
      5    17 ms    17 ms    16 ms  103.215.176.188
      6     *        *        *     Request timed out.
    """
    hops = []

    for line in output.split('\n'):
        line = line.strip()
        if not line or line.startswith('Tracing') or line.startswith('Over') or line.startswith('Trace'):
            continue

        # Match hop number at start of line
        match = re.match(r'^(\d+)\s+(.*)', line)
        if not match:
            continue

        hop_num = int(match.group(1))
        rest = match.group(2).strip()

        # Extract all ms values
        times = []
        for t in re.findall(r'(\d+)\s*ms', rest):
            times.append(int(t))

        # Extract IP address (IPv4 or IPv6)
        ip_match = re.search(r'([\d]+\.[\d]+\.[\d]+\.[\d]+)', rest)
        if not ip_match:
            # Try IPv6
            ip_match = re.search(r'([0-9a-fA-F:]{2,39})', rest)
        ip = ip_match.group(1) if ip_match else None

        timed_out = '*' in rest and not times

        hop = {
            "hop": hop_num,
            "ip": ip,
            "hostname": None,
            "response_times_ms": times,
            "avg_ms": round(sum(times) / len(times), 2) if times else None,
            "min_ms": min(times) if times else None,
            "max_ms": max(times) if times else None,
            "timed_out": timed_out,
        }

        hops.append(hop)

    return hops


def _parse_traceroute_output(output: str) -> List[dict]:
    """Parse Linux/Mac traceroute output"""
    hops = []

    for line in output.split('\n'):
        line = line.strip()
        if not line or line.startswith('traceroute'):
            continue

        parts = line.split()
        if len(parts) < 2:
            continue

        try:
            hop_num = int(parts[0])
        except ValueError:
            continue

        ip = parts[1] if len(parts) > 1 else "*"

        times = []
        for part in parts[2:]:
            try:
                val = float(part.rstrip('ms'))
                times.append(val)
            except ValueError:
                continue

        timed_out = ip == "*" or (not times and len(parts) > 2 and parts[2] == "*")

        hop = {
            "hop": hop_num,
            "ip": ip if ip != "*" else None,
            "hostname": None,
            "response_times_ms": times,
            "avg_ms": round(sum(times) / len(times), 2) if times else None,
            "min_ms": min(times) if times else None,
            "max_ms": max(times) if times else None,
            "timed_out": timed_out,
        }

        hops.append(hop)

    return hops
