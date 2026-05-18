import re
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1", tags=["documents"])
DOCUMENTS: list[dict] = []

MALICIOUS_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"exfiltrate",
    r"override policy",
]


class DocumentIngestRequest(BaseModel):
    title: str
    area: str
    category: str
    access_level: str = "internal"
    content: str


@router.post("/documents")
def ingest_document(payload: DocumentIngestRequest, x_tenant_id: str | None = Header(default=None)) -> dict:
    if not x_tenant_id:
        raise HTTPException(status_code=400, detail="x-tenant-id header is required")

    suspicious = any(re.search(pattern, payload.content, re.IGNORECASE) for pattern in MALICIOUS_PATTERNS)
    chunks = [chunk.strip() for chunk in payload.content.split("\n\n") if chunk.strip()]

    item = {
        "id": f"doc-{len(DOCUMENTS)+1}",
        "tenant_id": x_tenant_id,
        "title": payload.title,
        "area": payload.area,
        "category": payload.category,
        "access_level": payload.access_level,
        "content": payload.content,
        "chunks": chunks,
        "prompt_injection_flag": suspicious,
    }
    DOCUMENTS.append(item)
    return {"document_id": item["id"], "chunks": len(chunks), "suspicious": suspicious}


@router.get("/documents")
def list_documents(x_tenant_id: str | None = Header(default=None)) -> dict:
    return {"items": [{k: v for k, v in d.items() if k != "content"} for d in DOCUMENTS if d["tenant_id"] == x_tenant_id]}

