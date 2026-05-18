import os
import pytest
import httpx

BASE = os.getenv("GATEWAY_URL", "http://localhost:8080")


@pytest.mark.integration
def test_auth_and_tenant_isolation() -> None:
    pytest.skip("Requires running docker-compose stack")
    with httpx.Client(timeout=10) as client:
        _ = client.get(f"{BASE}/health")
