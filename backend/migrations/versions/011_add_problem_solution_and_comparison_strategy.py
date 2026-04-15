"""add problem comparison strategy and reference solutions

Revision ID: 011
Revises: 010
Create Date: 2026-04-14

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "011"
down_revision = "010"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "problems",
        sa.Column("comparison_strategy", sa.String(length=32), nullable=False, server_default="exact"),
    )

    op.create_table(
        "problem_solutions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=36), nullable=False),
        sa.Column("language", sa.String(length=16), nullable=False, server_default="python"),
        sa.Column("function_name", sa.String(length=128), nullable=False, server_default="solution"),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("problem_id"),
    )
    op.create_index(op.f("ix_problem_solutions_problem_id"), "problem_solutions", ["problem_id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_problem_solutions_problem_id"), table_name="problem_solutions")
    op.drop_table("problem_solutions")
    op.drop_column("problems", "comparison_strategy")
