from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.workflows import executive_question_flow, executive_question_stream, build_board_pack

router = APIRouter(prefix="/api/v1", tags=["agent-orchestrator"])


class ExecutiveQuestionRequest(BaseModel):
    question: str
    role: str = "ceo"
    intent: str = "executive_question"


class BoardPackFlowRequest(BaseModel):
    period: str
    areas: list[str] = []


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": "agent-orchestrator-service"}


@router.post("/orchestrator/executive-question")
async def run_executive_question(payload: ExecutiveQuestionRequest, x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    return await executive_question_flow(payload.model_dump(), x_tenant_id)


@router.post("/orchestrator/executive-question/stream")
async def run_executive_question_stream(payload: ExecutiveQuestionRequest, x_tenant_id: str | None = Header(default=None)) -> StreamingResponse:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    generator = executive_question_stream(payload.model_dump(), x_tenant_id)
    return StreamingResponse(generator, media_type="text/event-stream")


@router.post("/orchestrator/board-pack")
def run_board_pack(payload: BoardPackFlowRequest, x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    result = build_board_pack(payload.model_dump())
    result["tenant_id"] = x_tenant_id
    return result
