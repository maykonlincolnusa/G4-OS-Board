from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_board_pack_workflow() -> None:
    response = client.post(
        "/api/v1/orchestrator/board-pack",
        headers={"x-tenant-id": "tenant-demo"},
        json={"period": "2026-Q2", "areas": ["Financeiro", "Vendas"]},
    )
    assert response.status_code == 200
    assert response.json()["workflow"] == "board_pack_generation"

