from app.core.config import get_settings


def get_health() -> dict:
    settings = get_settings()
    return {"status": "healthy", "service": settings.service_name}

