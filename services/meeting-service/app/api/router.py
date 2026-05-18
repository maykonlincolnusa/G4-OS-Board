import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import MeetingModel

router = APIRouter(prefix="/api/v1", tags=["meetings"])
settings = get_settings()


class MeetingCreate(BaseModel):
    title: str
    starts_at: datetime
    board_id: str | None = None


class MeetingSummaryRequest(BaseModel):
    meeting_id: str
    transcript: str


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.post("/meetings")
def create_meeting(payload: MeetingCreate, x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    item = MeetingModel(
        id=str(uuid.uuid4()),
        tenant_id=x_tenant_id,
        board_id=payload.board_id,
        title=payload.title,
        starts_at=payload.starts_at,
        status="scheduled",
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return {
        "id": item.id,
        "tenant_id": item.tenant_id,
        "title": item.title,
        "starts_at": item.starts_at.isoformat(),
        "board_id": item.board_id,
        "status": item.status,
    }


@router.get("/meetings")
def list_meetings(x_tenant_id: str | None = Header(default=None), db: Session = Depends(get_db)) -> dict:
    rows = db.scalars(
        select(MeetingModel)
        .where(MeetingModel.tenant_id == x_tenant_id)
        .order_by(MeetingModel.starts_at.desc())
    ).all()
    return {
        "items": [
            {
                "id": m.id,
                "tenant_id": m.tenant_id,
                "title": m.title,
                "starts_at": m.starts_at.isoformat(),
                "board_id": m.board_id,
                "status": m.status,
            }
            for m in rows
        ]
    }


@router.post("/meetings/summarize")
def summarize_meeting(payload: MeetingSummaryRequest) -> dict:
    minutes = {
        "meeting_id": payload.meeting_id,
        "summary": "Resumo executivo gerado automaticamente.",
        "decisions": ["Escalar mentoria premium", "Reforçar política de aprovação"],
        "follow_ups": ["Definir owners por ação", "Publicar riscos no board pack"],
    }
    return minutes
