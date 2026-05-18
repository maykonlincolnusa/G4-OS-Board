from fastapi import FastAPI
from app.api.router import router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings.service_name)

app = FastAPI(
    title=f"{settings.service_name} API",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)
app.include_router(router)


@app.get("/", tags=["health"])
def root() -> dict:
    return {"service": settings.service_name, "status": "ok"}

