from datetime import date, datetime
from sqlalchemy import Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class DecisionModel(Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), nullable=False)
    meeting_id: Mapped[str | None] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    impact_level: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    risk_level: Mapped[str] = mapped_column(String(32), nullable=False, default="medium")
    owner_user_id: Mapped[str | None] = mapped_column(String(64))
    due_date: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="open")
    created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
