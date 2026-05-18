import uuid
from datetime import date
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import ActionModel

router = APIRouter(prefix="/api/v1", tags=["action-tracker"])
settings = get_settings()


class ActionCreate(BaseModel):
    title: str
    owner_user_id: str | None = None
    due_date: date | None = None
    priority: str = "medium"


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.post("/actions")
def create_action(payload: ActionCreate, x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    item = ActionModel(
        id=str(uuid.uuid4()),
        tenant_id=x_tenant_id,
        title=payload.title,
        owner_user_id=payload.owner_user_id,
        due_date=payload.due_date,
        priority=payload.priority,
        status="todo",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "tenant_id": item.tenant_id,
        "title": item.title,
        "owner_user_id": item.owner_user_id,
        "due_date": item.due_date.isoformat() if item.due_date else None,
        "priority": item.priority,
        "status": item.status,
    }


@router.get("/actions")
def list_actions(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(
        select(ActionModel)
        .where(ActionModel.tenant_id == x_tenant_id)
        .order_by(ActionModel.created_at.desc())
    ).all()
    return {
        "items": [
            {
                "id": a.id,
                "tenant_id": a.tenant_id,
                "title": a.title,
                "owner_user_id": a.owner_user_id,
                "due_date": a.due_date.isoformat() if a.due_date else None,
                "priority": a.priority,
                "status": a.status,
            }
            for a in rows
        ]
    }


@router.get("/actions/overdue")
def overdue_actions(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    today = date.today()
    rows = db.scalars(
        select(ActionModel).where(
            ActionModel.tenant_id == x_tenant_id,
            ActionModel.due_date.is_not(None),
            ActionModel.due_date < today,
            ActionModel.status != "done",
        )
    ).all()

    items = [
        {
            "id": a.id,
            "title": a.title,
            "due_date": a.due_date.isoformat() if a.due_date else None,
            "status": a.status,
            "priority": a.priority,
        }
        for a in rows
    ]
    return {"items": items, "count": len(items)}
