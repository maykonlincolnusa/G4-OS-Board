import uuid
from datetime import date
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import DecisionModel

router = APIRouter(prefix="/api/v1", tags=["decision-memory"])
settings = get_settings()


class DecisionCreate(BaseModel):
    title: str
    description: str
    impact_level: str = "medium"
    risk_level: str = "medium"
    owner_user_id: str | None = None
    due_date: date | None = None


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.post("/decisions")
def create_decision(payload: DecisionCreate, x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    item = DecisionModel(
        id=str(uuid.uuid4()),
        tenant_id=x_tenant_id,
        title=payload.title,
        description=payload.description,
        impact_level=payload.impact_level,
        risk_level=payload.risk_level,
        owner_user_id=payload.owner_user_id,
        due_date=payload.due_date,
        status="open",
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "id": item.id,
        "tenant_id": item.tenant_id,
        "title": item.title,
        "description": item.description,
        "impact_level": item.impact_level,
        "risk_level": item.risk_level,
        "owner_user_id": item.owner_user_id,
        "due_date": item.due_date.isoformat() if item.due_date else None,
        "status": item.status,
    }


@router.get("/decisions")
def list_decisions(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(
        select(DecisionModel)
        .where(DecisionModel.tenant_id == x_tenant_id)
        .order_by(DecisionModel.created_at.desc())
    ).all()
    return {
        "items": [
            {
                "id": d.id,
                "tenant_id": d.tenant_id,
                "title": d.title,
                "description": d.description,
                "impact_level": d.impact_level,
                "risk_level": d.risk_level,
                "owner_user_id": d.owner_user_id,
                "due_date": d.due_date.isoformat() if d.due_date else None,
                "status": d.status,
            }
            for d in rows
        ]
    }
