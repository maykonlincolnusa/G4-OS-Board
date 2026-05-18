import os
from pathlib import Path

DB_FILE = Path("./test_action.db")
if DB_FILE.exists():
    DB_FILE.unlink()

os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{DB_FILE.as_posix()}"
os.environ["DATABASE_PROVIDER"] = "local"

from fastapi.testclient import TestClient
from app.main import app
from app.core.db import Base, engine

Base.metadata.create_all(bind=engine)

client = TestClient(app)


def test_create_action() -> None:
    response = client.post(
        "/api/v1/actions",
        headers={"x-tenant-id": "tenant-demo"},
        json={"title": "Executar plano", "priority": "high"},
    )
    assert response.status_code == 200
    assert response.json()["id"]
