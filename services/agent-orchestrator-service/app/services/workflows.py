import asyncio
import os
import uuid
import httpx
from typing import Any, AsyncIterator

RAG_URL = os.getenv("RAG_SERVICE_URL", "http://rag-service:8000")


def _route_agent(intent: str) -> str:
    mapping = {
        "board_pack": "executive-board-agent",
        "meeting_minutes": "board-secretary-agent",
        "risk_check": "risk-officer-agent",
    }
    return mapping.get(intent, "executive-board-agent")


async def executive_question_flow(payload: dict[str, Any], tenant_id: str) -> dict[str, Any]:
    correlation_id = str(uuid.uuid4())
    async with httpx.AsyncClient(timeout=30) as client:
        rag_resp = await client.post(
            f"{RAG_URL}/api/v1/rag/query",
            headers={"x-tenant-id": tenant_id},
            json={"query": payload["question"], "role": payload.get("role", "viewer")},
        )
        rag_data = rag_resp.json()

    agent_key = _route_agent(payload.get("intent", "executive_question"))
    return {
        "workflow": "executive_question",
        "correlation_id": correlation_id,
        "agent": agent_key,
        "answer": rag_data.get("answer"),
        "citations": rag_data.get("citations", []),
        "confidence_score": rag_data.get("confidence_score", 0.4),
        "quality_review": {
            "agent": "ai-quality-evaluator-agent",
            "status": "approved" if rag_data.get("citations") else "needs-review",
        },
    }


async def executive_question_stream(payload: dict[str, Any], tenant_id: str) -> AsyncIterator[str]:
    result = await executive_question_flow(payload, tenant_id)
    answer = (result.get("answer") or "").strip()

    yield "event: meta\n"
    yield f"data: {{\"correlation_id\": \"{result.get('correlation_id')}\", \"agent\": \"{result.get('agent')}\"}}\n\n"

    for token in answer.split(" "):
        yield "event: chunk\n"
        yield f"data: {token} \n\n"
        await asyncio.sleep(0.03)

    citations = result.get("citations", [])
    confidence = result.get("confidence_score", 0.0)
    yield "event: done\n"
    yield (
        "data: "
        + str({"citations": citations, "confidence_score": confidence}).replace("'", '"')
        + "\n\n"
    )


def build_board_pack(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "workflow": "board_pack_generation",
        "executive_summary": f"Board pack do período {payload.get('period', 'N/A')} consolidado.",
        "sections": [
            "KPIs", "Riscos", "Decisões Pendentes", "Ações Atrasadas", "Recomendações"
        ],
        "agents": [
            "executive-board-agent",
            "cfo-analyst-agent",
            "revenue-growth-agent",
            "risk-officer-agent",
            "board-secretary-agent",
        ],
    }
