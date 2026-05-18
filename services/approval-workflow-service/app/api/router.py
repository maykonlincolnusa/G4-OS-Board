from fastapi import APIRouter, Header, HTTPException
from app.core.config import get_settings

router = APIRouter(prefix="/api/v1")
settings = get_settings()


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.get("/tenant-context", tags=["security"])
def tenant_context(x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    return {"tenant_id": x_tenant_id, "service": settings.service_name}

