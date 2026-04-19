"""add problem project stats table

Revision ID: 012
Revises: 011
Create Date: 2026-04-19

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "012"
down_revision = "011"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "problem_project_stats",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("attempted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("submitted", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "problem_id", "project_id", name="uix_problem_project_stats_user_problem_project"),
    )
    op.create_index(op.f("ix_problem_project_stats_user_id"), "problem_project_stats", ["user_id"], unique=False)
    op.create_index(op.f("ix_problem_project_stats_problem_id"), "problem_project_stats", ["problem_id"], unique=False)
    op.create_index(op.f("ix_problem_project_stats_project_id"), "problem_project_stats", ["project_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_problem_project_stats_project_id"), table_name="problem_project_stats")
    op.drop_index(op.f("ix_problem_project_stats_problem_id"), table_name="problem_project_stats")
    op.drop_index(op.f("ix_problem_project_stats_user_id"), table_name="problem_project_stats")
    op.drop_table("problem_project_stats")
