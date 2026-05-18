import os
from pathlib import Path

DB_FILE = Path("./test_tenant.db")
if DB_FILE.exists():
    DB_FILE.unlink()

os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{DB_FILE.as_posix()}"
os.environ["DATABASE_PROVIDER"] = "local"

from fastapi.testclient import TestClient
from app.main import app
from app.core.db import Base, engine, SessionLocal
from app.domain.models import TenantModel

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    db.add(TenantModel(id="tenant-demo", name="Tenant Demo", slug="tenant-demo", plan="enterprise"))
    db.commit()

client = TestClient(app)


def test_current_tenant_requires_header() -> None:
    response = client.get("/api/v1/tenants/current")
    assert response.status_code == 400


def test_current_tenant_success() -> None:
    response = client.get("/api/v1/tenants/current", headers={"x-tenant-id": "tenant-demo"})
    assert response.status_code == 200
    assert response.json()["tenant"]["id"] == "tenant-demo"
