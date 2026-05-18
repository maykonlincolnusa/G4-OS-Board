import os
from pathlib import Path

DB_FILE = Path("./test_auth_health.db")
if DB_FILE.exists():
    DB_FILE.unlink()

os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{DB_FILE.as_posix()}"
os.environ["DATABASE_PROVIDER"] = "local"

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
