"""create users table and seed privileged profiles

Revision ID: 20260726_01
Revises:
Create Date: 2026-07-26 00:00:00
"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa

from app.core.security import hash_password


revision = "20260726_01"
down_revision = None
branch_labels = None
depends_on = None


def _create_users_table_if_needed() -> None:
    bind = op.get_bind()
    if sa.inspect(bind).has_table("users"):
        return

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("fullname", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)
    op.create_index("ix_users_id", "users", ["id"], unique=False)


def _seed_profile(email: str, fullname: str, role: str, password: str) -> None:
    bind = op.get_bind()
    users = sa.table(
        "users",
        sa.column("fullname", sa.String()),
        sa.column("email", sa.String()),
        sa.column("password", sa.String()),
        sa.column("role", sa.String()),
        sa.column("is_active", sa.Boolean()),
        sa.column("created_at", sa.DateTime()),
        sa.column("updated_at", sa.DateTime()),
    )
    exists = bind.execute(
        sa.select(users.c.email).where(users.c.email == email)
    ).first()
    if exists:
        return

    now = datetime.utcnow()
    bind.execute(
        sa.insert(users).values(
            fullname=fullname,
            email=email,
            password=hash_password(password),
            role=role,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
    )


def upgrade() -> None:
    _create_users_table_if_needed()
    _seed_profile(
        email="ilahir66@gmail.com",
        fullname="Super Admin",
        role="super_admin",
        password="SuperAdmin@01",
    )
    _seed_profile(
        email="jiwagila023@gmail.com",
        fullname="Administrator",
        role="admin",
        password="Admin@01",
    )


def downgrade() -> None:
    bind = op.get_bind()
    for email in (
        "ilahir66@gmail.com",
        "jiwagila023@gmail.com",
    ):
        bind.execute(sa.text("DELETE FROM users WHERE email = :email"), {"email": email})
