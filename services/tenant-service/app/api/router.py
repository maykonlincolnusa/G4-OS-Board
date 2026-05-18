from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import TenantModel

router = APIRouter(prefix="/api/v1", tags=["tenant"])
settings = get_settings()


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.get("/tenants/current")
def current_tenant(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    tenant = db.scalar(select(TenantModel).where(TenantModel.id == x_tenant_id))
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    return {
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "slug": tenant.slug,
            "plan": tenant.plan,
        }
    }


@router.get("/tenants")
def list_tenants(db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(select(TenantModel).order_by(TenantModel.name.asc())).all()
    return {
        "items": [
            {"id": t.id, "name": t.name, "slug": t.slug, "plan": t.plan}
            for t in rows
        ]
    }
