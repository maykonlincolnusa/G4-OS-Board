"""create core priority governance tables

Revision ID: 20260518_0001
Revises:
Create Date: 2026-05-18 20:30:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260518_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not inspector.has_table("tenants"):
        op.create_table(
            "tenants",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("name", sa.String(length=255), nullable=False),
            sa.Column("slug", sa.String(length=255), nullable=False, unique=True),
            sa.Column("plan", sa.String(length=64), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not inspector.has_table("users"):
        op.create_table(
            "users",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("email", sa.String(length=255), nullable=False),
            sa.Column("full_name", sa.String(length=255), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not inspector.has_table("meetings"):
        op.create_table(
            "meetings",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("board_id", sa.String(length=64), nullable=True),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not inspector.has_table("decisions"):
        op.create_table(
            "decisions",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("meeting_id", sa.String(length=64), nullable=True),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("description", sa.Text(), nullable=False),
            sa.Column("impact_level", sa.String(length=32), nullable=False),
            sa.Column("risk_level", sa.String(length=32), nullable=False),
            sa.Column("owner_user_id", sa.String(length=64), nullable=True),
            sa.Column("due_date", sa.Date(), nullable=True),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not inspector.has_table("actions"):
        op.create_table(
            "actions",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("decision_id", sa.String(length=64), nullable=True),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("owner_user_id", sa.String(length=64), nullable=True),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("priority", sa.String(length=32), nullable=False),
            sa.Column("due_date", sa.Date(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not inspector.has_table("risks"):
        op.create_table(
            "risks",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("title", sa.String(length=255), nullable=False),
            sa.Column("category", sa.String(length=64), nullable=False),
            sa.Column("probability", sa.Integer(), nullable=False),
            sa.Column("impact", sa.Integer(), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.Column("owner_user_id", sa.String(length=64), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )

    if not inspector.has_table("audit_logs"):
        op.create_table(
            "audit_logs",
            sa.Column("id", sa.String(length=64), primary_key=True),
            sa.Column("tenant_id", sa.String(length=64), sa.ForeignKey("tenants.id", ondelete="CASCADE"), nullable=False),
            sa.Column("actor_user_id", sa.String(length=64), nullable=True),
            sa.Column("action", sa.String(length=128), nullable=False),
            sa.Column("entity_type", sa.String(length=128), nullable=False),
            sa.Column("entity_id", sa.String(length=128), nullable=False),
            sa.Column("before_data", sa.JSON(), nullable=True),
            sa.Column("after_data", sa.JSON(), nullable=True),
            sa.Column("request_id", sa.String(length=128), nullable=True),
            sa.Column("correlation_id", sa.String(length=128), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP")),
        )


def downgrade() -> None:
    op.drop_table("audit_logs")
    op.drop_table("risks")
    op.drop_table("actions")
    op.drop_table("decisions")
    op.drop_table("meetings")
    op.drop_table("users")
    op.drop_table("tenants")
