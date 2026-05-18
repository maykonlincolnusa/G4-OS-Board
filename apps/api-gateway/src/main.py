from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
import os
import jwt
import httpx
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

JWT_SECRET = os.getenv("JWT_SECRET", "change-me")
JWT_ALGO = "HS256"

SERVICE_MAP = {
    "auth": os.getenv("AUTH_SERVICE_URL", "http://auth-service:8000"),
    "tenant": os.getenv("TENANT_SERVICE_URL", "http://tenant-service:8000"),
    "meeting": os.getenv("MEETING_SERVICE_URL", "http://meeting-service:8000"),
    "decision": os.getenv("DECISION_SERVICE_URL", "http://decision-memory-service:8000"),
    "action": os.getenv("ACTION_SERVICE_URL", "http://action-tracker-service:8000"),
    "risk": os.getenv("RISK_SERVICE_URL", "http://risk-compliance-service:8000"),
    "rag": os.getenv("RAG_SERVICE_URL", "http://rag-service:8000"),
    "agent": os.getenv("AGENT_SERVICE_URL", "http://agent-orchestrator-service:8000"),
    "boardpack": os.getenv("BOARDPACK_SERVICE_URL", "http://board-pack-generator-service:8000"),
    "audit": os.getenv("AUDIT_SERVICE_URL", "http://audit-ledger-service:8000"),
}


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    app.state.http = httpx.AsyncClient(timeout=60)
    yield
    await app.state.http.aclose()


app = FastAPI(title="Board Governance API Gateway", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "healthy", "service": "api-gateway"}


@app.get("/api/v1/catalog")
def catalog() -> dict:
    return {"services": SERVICE_MAP}


def _validate_token(authorization: str | None) -> dict:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")
    token = authorization.split(" ", maxsplit=1)[1]
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail=f"Invalid token: {exc}") from exc


def _is_public_auth_route(service: str, path: str, method: str) -> bool:
    if service != "auth":
        return False
    normalized = path.strip("/")
    return (normalized == "login" and method.upper() == "POST") or (normalized == "health" and method.upper() == "GET")


@app.api_route("/api/v1/{service}/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(
    request: Request,
    service: str,
    path: str,
    x_tenant_id: str | None = Header(default=None),
    authorization: str | None = Header(default=None),
):
    if service not in SERVICE_MAP:
        raise HTTPException(status_code=404, detail="Service not found")

    is_public = _is_public_auth_route(service, path, request.method)
    claims = {"sub": "public", "role": "public", "tenant_id": x_tenant_id or ""}

    if not is_public:
        if not x_tenant_id:
            raise HTTPException(status_code=400, detail="x-tenant-id header is required")
        claims = _validate_token(authorization)
        if claims.get("tenant_id") != x_tenant_id and claims.get("role") != "super_admin":
            raise HTTPException(status_code=403, detail="Tenant scope mismatch")

    url = f"{SERVICE_MAP[service]}/api/v1/{path}"
    payload = await request.body()

    forward_headers = {
        "content-type": request.headers.get("content-type", "application/json"),
        "x-user-id": claims.get("sub", "unknown"),
        "x-user-role": claims.get("role", "viewer"),
    }
    if x_tenant_id:
        forward_headers["x-tenant-id"] = x_tenant_id

    wants_stream = "text/event-stream" in request.headers.get("accept", "") or request.query_params.get("stream") == "1"
    if wants_stream:
        upstream = app.state.http.stream(
            request.method,
            url,
            content=payload,
            params=request.query_params,
            headers=forward_headers,
        )

        async def _iter() -> AsyncIterator[bytes]:
            async with upstream:
                async for chunk in upstream.aiter_bytes():
                    yield chunk

        return StreamingResponse(_iter(), status_code=upstream.status_code, media_type=upstream.headers.get("content-type", "text/event-stream"))

    response = await app.state.http.request(
        request.method,
        url,
        content=payload,
        params=request.query_params,
        headers=forward_headers,
    )
    try:
        data = response.json()
    except ValueError:
        data = {"raw": response.text}
    return {"status_code": response.status_code, "data": data}

