"""
Workspace API endpoints — domain management, monitoring, dashboard.
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.services.workspace_service import WorkspaceService
from app.services.monitoring_service import MonitoringService

router = APIRouter(prefix="/workspace", tags=["Workspace"])


# ============ Request/Response Models ============

class AddDomainRequest(BaseModel):
    domain: str
    notes: Optional[str] = None
    monitor_ssl: bool = True
    monitor_dns: bool = True
    monitor_uptime: bool = True


class UpdateDomainRequest(BaseModel):
    notes: Optional[str] = None
    status: Optional[str] = None
    monitor_ssl: Optional[bool] = None
    monitor_dns: Optional[bool] = None
    monitor_uptime: Optional[bool] = None
    check_interval_minutes: Optional[int] = None


class DomainInfo(BaseModel):
    id: int
    domain: str
    notes: Optional[str]
    status: str
    monitor_ssl: bool
    monitor_dns: bool
    monitor_uptime: bool
    check_interval_minutes: int
    created_at: Optional[str]
    last_checked_at: Optional[str]


class DomainDetail(BaseModel):
    id: int
    domain: str
    notes: Optional[str]
    status: str
    monitor_ssl: bool
    monitor_dns: bool
    monitor_uptime: bool
    check_interval_minutes: int
    created_at: Optional[str]
    updated_at: Optional[str]
    last_checked_at: Optional[str]


class DashboardResponse(BaseModel):
    total_domains: int
    active_domains: int
    alert_domains: int
    plan: str


class MessageResponse(BaseModel):
    message: str


class CheckResultResponse(BaseModel):
    domain: str
    check_type: str
    result: Optional[dict] = None
    message: str


# ============ Domain Endpoints ============

@router.get("/domains", response_model=List[DomainInfo])
async def list_domains(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all domains in user's workspace."""
    return await WorkspaceService.list_domains(db=db, user=user)


@router.post("/domains", response_model=DomainInfo, status_code=status.HTTP_201_CREATED)
async def add_domain(
    request: AddDomainRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Add a domain to workspace."""
    try:
        domain = await WorkspaceService.add_domain(
            db=db,
            user=user,
            domain=request.domain,
            notes=request.notes,
            monitor_ssl=request.monitor_ssl,
            monitor_dns=request.monitor_dns,
            monitor_uptime=request.monitor_uptime,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return DomainInfo(
        id=domain.id,
        domain=domain.domain,
        notes=domain.notes,
        status=domain.status,
        monitor_ssl=domain.monitor_ssl,
        monitor_dns=domain.monitor_dns,
        monitor_uptime=domain.monitor_uptime,
        check_interval_minutes=domain.check_interval_minutes,
        created_at=domain.created_at.isoformat() if domain.created_at else None,
        last_checked_at=domain.last_checked_at.isoformat() if domain.last_checked_at else None,
    )


@router.get("/domains/{domain_id}", response_model=DomainDetail)
async def get_domain(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get domain details."""
    domain = await WorkspaceService.get_domain(db=db, user=user, domain_id=domain_id)
    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )
    return domain


@router.put("/domains/{domain_id}", response_model=DomainDetail)
async def update_domain(
    domain_id: int,
    request: UpdateDomainRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update domain settings."""
    domain = await WorkspaceService.update_domain(
        db=db,
        user=user,
        domain_id=domain_id,
        notes=request.notes,
        status=request.status,
        monitor_ssl=request.monitor_ssl,
        monitor_dns=request.monitor_dns,
        monitor_uptime=request.monitor_uptime,
        check_interval_minutes=request.check_interval_minutes,
    )

    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )

    return DomainDetail(
        id=domain.id,
        domain=domain.domain,
        notes=domain.notes,
        status=domain.status,
        monitor_ssl=domain.monitor_ssl,
        monitor_dns=domain.monitor_dns,
        monitor_uptime=domain.monitor_uptime,
        check_interval_minutes=domain.check_interval_minutes,
        created_at=domain.created_at.isoformat() if domain.created_at else None,
        updated_at=domain.updated_at.isoformat() if domain.updated_at else None,
        last_checked_at=domain.last_checked_at.isoformat() if domain.last_checked_at else None,
    )


@router.delete("/domains/{domain_id}", response_model=MessageResponse)
async def delete_domain(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a domain from workspace."""
    success = await WorkspaceService.delete_domain(db=db, user=user, domain_id=domain_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )
    return MessageResponse(message="Domain berhasil dihapus.")


# ============ Manual Check Endpoints ============

@router.post("/domains/{domain_id}/check-ssl", response_model=CheckResultResponse)
async def check_ssl(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger SSL check for a domain."""
    # Verify ownership
    domain = await WorkspaceService.get_domain(db=db, user=user, domain_id=domain_id)
    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )

    result = await MonitoringService.check_ssl(db=db, domain_id=domain_id)
    await db.commit()

    if result is None:
        return CheckResultResponse(
            domain=domain["domain"],
            check_type="ssl",
            result=None,
            message="SSL check gagal atau tidak tersedia.",
        )

    return CheckResultResponse(
        domain=result["domain"],
        check_type="ssl",
        result=result,
        message="SSL check berhasil.",
    )


@router.post("/domains/{domain_id}/check-dns", response_model=CheckResultResponse)
async def check_dns(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger DNS check for a domain."""
    domain = await WorkspaceService.get_domain(db=db, user=user, domain_id=domain_id)
    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )

    result = await MonitoringService.check_dns(db=db, domain_id=domain_id)
    await db.commit()

    if result is None:
        return CheckResultResponse(
            domain=domain["domain"],
            check_type="dns",
            result=None,
            message="DNS check gagal atau tidak tersedia.",
        )

    return CheckResultResponse(
        domain=result["domain"],
        check_type="dns",
        result=result,
        message="DNS check berhasil.",
    )


@router.post("/domains/{domain_id}/check-uptime", response_model=CheckResultResponse)
async def check_uptime(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger uptime check for a domain."""
    domain = await WorkspaceService.get_domain(db=db, user=user, domain_id=domain_id)
    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )

    result = await MonitoringService.check_uptime(db=db, domain_id=domain_id)
    await db.commit()

    if result is None:
        return CheckResultResponse(
            domain=domain["domain"],
            check_type="uptime",
            result=None,
            message="Uptime check gagal atau tidak tersedia.",
        )

    return CheckResultResponse(
        domain=result["domain"],
        check_type="uptime",
        result=result,
        message="Uptime check berhasil.",
    )


@router.post("/domains/{domain_id}/check-all", response_model=CheckResultResponse)
async def check_all(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger all checks (SSL, DNS, Uptime) for a domain."""
    domain = await WorkspaceService.get_domain(db=db, user=user, domain_id=domain_id)
    if domain is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Domain tidak ditemukan.",
        )

    results = {}
    ssl_result = await MonitoringService.check_ssl(db=db, domain_id=domain_id)
    if ssl_result:
        results["ssl"] = ssl_result

    dns_result = await MonitoringService.check_dns(db=db, domain_id=domain_id)
    if dns_result:
        results["dns"] = dns_result

    uptime_result = await MonitoringService.check_uptime(db=db, domain_id=domain_id)
    if uptime_result:
        results["uptime"] = uptime_result

    await db.commit()

    return CheckResultResponse(
        domain=domain["domain"],
        check_type="all",
        result=results,
        message=f"Checks selesai. {len(results)} check berhasil.",
    )


# ============ Monitoring History ============

@router.get("/domains/{domain_id}/ssl/history")
async def get_ssl_history(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get SSL history for a domain."""
    history = await WorkspaceService.get_ssl_history(db=db, user=user, domain_id=domain_id)
    return {"domain_id": domain_id, "history": history}


@router.get("/domains/{domain_id}/dns/history")
async def get_dns_history(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get DNS history for a domain."""
    history = await WorkspaceService.get_dns_history(db=db, user=user, domain_id=domain_id)
    return {"domain_id": domain_id, "history": history}


@router.get("/domains/{domain_id}/uptime/logs")
async def get_uptime_logs(
    domain_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get uptime logs for a domain."""
    logs = await WorkspaceService.get_uptime_logs(db=db, user=user, domain_id=domain_id)
    return {"domain_id": domain_id, "logs": logs}


# ============ Dashboard ============

@router.get("/dashboard", response_model=DashboardResponse)
async def get_dashboard(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard overview stats."""
    return await WorkspaceService.get_dashboard(db=db, user=user)
