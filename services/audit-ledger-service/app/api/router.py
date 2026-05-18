import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import AuditLogModel

router = APIRouter(prefix="/api/v1", tags=["audit"])
settings = get_settings()


class AuditCreate(BaseModel):
    action: str
    entity_type: str
    entity_id: str
    before_data: dict | None = None
    after_data: dict | None = None
    correlation_id: str | None = None


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.post("/audit/logs")
def create_audit(
    payload: AuditCreate,
    x_tenant_id: str | None = Header(default=None),
    x_user_id: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    item = AuditLogModel(
        id=str(uuid.uuid4()),
        tenant_id=x_tenant_id,
        actor_user_id=x_user_id,
        action=payload.action,
        entity_type=payload.entity_type,
        entity_id=payload.entity_id,
        before_data=payload.before_data,
        after_data=payload.after_data,
        request_id=x_request_id,
        correlation_id=payload.correlation_id,
        created_at=datetime.now(timezone.utc),
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "id": item.id,
        "tenant_id": item.tenant_id,
        "actor_user_id": item.actor_user_id,
        "action": item.action,
        "entity_type": item.entity_type,
        "entity_id": item.entity_id,
        "before_data": item.before_data,
        "after_data": item.after_data,
        "request_id": item.request_id,
        "correlation_id": item.correlation_id,
        "created_at": item.created_at.isoformat() if item.created_at else None,
    }


@router.get("/audit/logs")
def list_logs(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(
        select(AuditLogModel)
        .where(AuditLogModel.tenant_id == x_tenant_id)
        .order_by(AuditLogModel.created_at.desc())
    ).all()
    return {
        "items": [
            {
                "id": i.id,
                "tenant_id": i.tenant_id,
                "actor_user_id": i.actor_user_id,
                "action": i.action,
                "entity_type": i.entity_type,
                "entity_id": i.entity_id,
                "before_data": i.before_data,
                "after_data": i.after_data,
                "request_id": i.request_id,
                "correlation_id": i.correlation_id,
                "created_at": i.created_at.isoformat() if i.created_at else None,
            }
            for i in rows
        ]
    }
