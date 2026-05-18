import re
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from app.services.rag_engine import rag_engine

router = APIRouter(prefix="/api/v1", tags=["rag"])

MALICIOUS_PATTERNS = [r"ignore previous instructions", r"system prompt", r"developer mode"]


class IndexRequest(BaseModel):
    document_id: str
    title: str
    area: str
    access_level: str = "internal"
    content: str


class QueryRequest(BaseModel):
    query: str
    role: str = "viewer"


ROLE_ACCESS = {
    "super_admin": {"public", "internal", "confidential", "board_only"},
    "tenant_admin": {"public", "internal", "confidential", "board_only"},
    "ceo": {"public", "internal", "confidential", "board_only"},
    "board_member": {"public", "internal", "confidential", "board_only"},
    "cfo": {"public", "internal", "confidential", "board_only"},
    "coo": {"public", "internal", "confidential"},
    "cmo": {"public", "internal"},
    "legal": {"public", "internal", "confidential"},
    "viewer": {"public", "internal"},
}


@router.post("/rag/index")
def rag_index(payload: IndexRequest, x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    suspicious = any(re.search(p, payload.content, re.IGNORECASE) for p in MALICIOUS_PATTERNS)
    chunks = rag_engine.index_document(
        tenant_id=x_tenant_id,
        document_id=payload.document_id,
        title=payload.title,
        area=payload.area,
        access_level=payload.access_level,
        content=payload.content,
    )
    return {"indexed_chunks": chunks, "prompt_injection_flag": suspicious}


@router.post("/rag/query")
def rag_query(payload: QueryRequest, x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")
    allowed = ROLE_ACCESS.get(payload.role, {"public"})
    context = rag_engine.search(x_tenant_id, payload.query, allowed)
    answer = rag_engine.answer(payload.query, context)
    return {
        "answer": answer,
        "citations": context,
        "confidence_score": min(1.0, 0.35 + (0.1 * len(context))),
    }

