from datetime import datetime, timedelta, timezone
import jwt
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.db import get_db
from app.domain.models import UserModel

router = APIRouter(prefix="/api/v1", tags=["auth"])
settings = get_settings()


class LoginRequest(BaseModel):
    email: str
    password: str


@router.get("/health", tags=["health"])
def health_check() -> dict:
    return {"status": "healthy", "service": settings.service_name}


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> dict:
    if payload.password != settings.auth_demo_password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = db.scalar(select(UserModel).where(UserModel.email == payload.email.lower()))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    claims = {
        "sub": user.id,
        "name": user.full_name,
        "role": "ceo",  # MVP default role mapping
        "tenant_id": user.tenant_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=8),
    }
    token = jwt.encode(claims, settings.jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer", "user": claims}


@router.get("/roles")
def list_roles() -> dict:
    return {
        "roles": [
            "super_admin", "tenant_admin", "ceo", "board_member", "founder", "cfo",
            "coo", "cmo", "legal", "manager", "mentor", "consultant", "viewer",
        ]
    }
