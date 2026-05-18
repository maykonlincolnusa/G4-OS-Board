from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_rag_index_and_query() -> None:
    headers = {"x-tenant-id": "tenant-demo"}
    index_resp = client.post(
        "/api/v1/rag/index",
        headers=headers,
        json={
            "document_id": "doc-1",
            "title": "Relatório Financeiro",
            "area": "Financeiro",
            "access_level": "confidential",
            "content": "Receita cresceu 15% no trimestre.\n\nMargem aumentou para 18%."
        }
    )
    assert index_resp.status_code == 200

    query_resp = client.post(
        "/api/v1/rag/query",
        headers=headers,
        json={"query": "Como está a margem?", "role": "cfo"},
    )
    assert query_resp.status_code == 200
    assert "citations" in query_resp.json()

