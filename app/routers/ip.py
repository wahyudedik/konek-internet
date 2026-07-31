from fastapi import APIRouter
from app.services import ip_service

router = APIRouter()


@router.get("/ip/{ip_address}")
async def ip_lookup(ip_address: str):
    """IP Lookup - Informasi IP address"""
    return await ip_service.lookup_ip(ip_address)


@router.get("/ip/{ip_address}/asn")
async def asn_lookup(ip_address: str):
    """ASN Lookup - Cek Autonomous System Number"""
    return await ip_service.lookup_asn(ip_address)


@router.get("/ip/{ip_address}/blacklist")
async def blacklist_checker(ip_address: str):
    """Blacklist Checker - Cek apakah IP ada di blacklist"""
    return await ip_service.check_blacklist(ip_address)