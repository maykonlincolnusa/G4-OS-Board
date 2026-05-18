import uuid
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import RiskModel

router = APIRouter(prefix="/api/v1", tags=["risk-compliance"])
settings = get_settings()


class RiskCreate(BaseModel):
    title: str
    category: str
    probability: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.post("/risks")
def create_risk(payload: RiskCreate, x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    item = RiskModel(
        id=str(uuid.uuid4()),
        tenant_id=x_tenant_id,
        title=payload.title,
        category=payload.category,
        probability=payload.probability,
        impact=payload.impact,
        status="open",
    )
    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "id": item.id,
        "tenant_id": item.tenant_id,
        "title": item.title,
        "category": item.category,
        "probability": item.probability,
        "impact": item.impact,
        "status": item.status,
    }


@router.get("/risks")
def list_risks(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(
        select(RiskModel)
        .where(RiskModel.tenant_id == x_tenant_id)
        .order_by(RiskModel.created_at.desc())
    ).all()
    return {
        "items": [
            {
                "id": r.id,
                "tenant_id": r.tenant_id,
                "title": r.title,
                "category": r.category,
                "probability": r.probability,
                "impact": r.impact,
                "status": r.status,
            }
            for r in rows
        ]
    }


@router.get("/risks/alerts")
def risk_alerts(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(select(RiskModel).where(RiskModel.tenant_id == x_tenant_id)).all()
    critical = [r for r in rows if (r.impact * r.probability) >= 16]
    return {
        "critical": [
            {
                "id": r.id,
                "title": r.title,
                "category": r.category,
                "probability": r.probability,
                "impact": r.impact,
                "status": r.status,
            }
            for r in critical
        ],
        "count": len(critical),
    }
