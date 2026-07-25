"""add optional personal profile fields

Revision ID: 20260726_02
Revises: 20260726_01
Create Date: 2026-07-26 00:00:00
"""
from alembic import op
import sqlalchemy as sa


revision = "20260726_02"
down_revision = "20260726_01"
branch_labels = None
depends_on = None


PROFILE_COLUMNS = (
    ("phone", sa.String(length=30)),
    ("address", sa.String(length=255)),
    ("date_of_birth", sa.Date()),
    ("gender", sa.String(length=20)),
)


def upgrade() -> None:
    existing_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("users")
    }
    for name, column_type in PROFILE_COLUMNS:
        if name not in existing_columns:
            op.add_column("users", sa.Column(name, column_type, nullable=True))


def downgrade() -> None:
    existing_columns = {
        column["name"] for column in sa.inspect(op.get_bind()).get_columns("users")
    }
    with op.batch_alter_table("users") as batch_op:
        for name, _ in reversed(PROFILE_COLUMNS):
            if name in existing_columns:
                batch_op.drop_column(name)
