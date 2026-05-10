"""add arg_types to test_cases

Revision ID: 015
Revises: 014
Create Date: 2026-05-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "015"
down_revision = "014"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "test_cases",
        sa.Column("arg_types", postgresql.JSONB, nullable=True),
    )


def downgrade():
    op.drop_column("test_cases", "arg_types")
