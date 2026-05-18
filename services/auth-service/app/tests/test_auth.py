import os
from pathlib import Path

DB_FILE = Path("./test_auth.db")
if DB_FILE.exists():
    DB_FILE.unlink()

os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{DB_FILE.as_posix()}"
os.environ["DATABASE_PROVIDER"] = "local"
os.environ["JWT_SECRET"] = "test-secret"

from fastapi.testclient import TestClient
from app.main import app
from app.core.db import Base, engine, SessionLocal
from app.domain.models import UserModel

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    db.add(
        UserModel(
            id="u-1",
            tenant_id="t-1",
            email="ceo@novaboard.ai",
            full_name="Ana Ribeiro",
        )
    )
    db.commit()

client = TestClient(app)


def test_login_success() -> None:
    response = client.post("/api/v1/login", json={"email": "ceo@novaboard.ai", "password": "123456"})
    assert response.status_code == 200
    assert "access_token" in response.json()
