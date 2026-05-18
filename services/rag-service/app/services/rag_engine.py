import os
from dataclasses import dataclass
from typing import Any

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None  # type: ignore[assignment]


@dataclass
class RagChunk:
    document_id: str
    title: str
    area: str
    access_level: str
    content: str


class RagEngine:
    def __init__(self) -> None:
        self._store: dict[str, list[RagChunk]] = {}
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if OpenAI and os.getenv("OPENAI_API_KEY") else None

    def index_document(self, tenant_id: str, document_id: str, title: str, area: str, access_level: str, content: str) -> int:
        chunks = [p.strip() for p in content.split("\n\n") if p.strip()]
        existing = self._store.setdefault(tenant_id, [])
        for piece in chunks:
            existing.append(RagChunk(document_id=document_id, title=title, area=area, access_level=access_level, content=piece))
        return len(chunks)

    def search(self, tenant_id: str, query: str, access_levels: set[str]) -> list[dict[str, Any]]:
        chunks = self._store.get(tenant_id, [])
        words = [w.lower() for w in query.split() if len(w) > 2]
        scored: list[tuple[float, RagChunk]] = []
        for chunk in chunks:
            if chunk.access_level not in access_levels:
                continue
            text = chunk.content.lower()
            score = sum(1 for w in words if w in text)
            if score > 0:
                scored.append((float(score), chunk))
        scored.sort(key=lambda x: x[0], reverse=True)
        top = scored[:5]
        return [
            {
                "document_id": c.document_id,
                "title": c.title,
                "area": c.area,
                "snippet": c.content[:280],
                "retrieval_score": s,
            }
            for s, c in top
        ]

    def answer(self, query: str, context: list[dict[str, Any]]) -> str:
        if not context:
            return "Não encontrei evidências suficientes para responder com confiança."
        if not self._client:
            snippets = " | ".join([c["snippet"] for c in context[:3]])
            return f"Resposta baseada em evidências internas: {snippets}"

        prompt = (
            "Você é um agente executivo. Responda somente com base no contexto. "
            "Se faltar dado, diga explicitamente.\n\n"
            f"Pergunta: {query}\n\nContexto:\n"
            + "\n".join([f"- {c['title']}: {c['snippet']}" for c in context])
        )
        response = self._client.responses.create(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), input=prompt)
        return response.output_text


rag_engine = RagEngine()

