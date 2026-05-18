from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.services.generator import generate_markdown

router = APIRouter(prefix="/api/v1", tags=["board-pack"])


class BoardPackRequest(BaseModel):
    period: str
    executive_summary: str
    decisions_pending: list[str] = []
    risks: list[str] = []


@router.post("/board-pack/generate")
def generate_board_pack(payload: BoardPackRequest, x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    md_path = generate_markdown(f"Board Pack {payload.period}", payload.model_dump())
    return {
        "tenant_id": x_tenant_id,
        "period": payload.period,
        "artifacts": {
            "markdown": str(md_path),
            "pdf": "pending-mvp",
            "pptx": "pending-mvp",
            "docx": "pending-mvp",
            "xlsx": "pending-mvp"
        }
    }

