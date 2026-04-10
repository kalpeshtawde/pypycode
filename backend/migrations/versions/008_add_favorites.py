"""Add favorites table for user-problem favorites

Revision ID: 008
Revises: 007
Create Date: 2026-04-10 09:30:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "favorites",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.String(36), sa.ForeignKey("users.id"), nullable=False, index=True),
        sa.Column("problem_id", sa.String(36), sa.ForeignKey("problems.id"), nullable=False, index=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "problem_id", name="uix_user_problem"),
    )


def downgrade():
    op.drop_table("favorites")
