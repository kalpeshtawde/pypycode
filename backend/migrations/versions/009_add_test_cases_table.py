"""Add test_cases table and remove test_cases JSON column from problems

Revision ID: 009
Revises: 008
Create Date: 2026-04-11 21:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade():
    # Create test_cases table
    op.create_table(
        "test_cases",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("problem_id", sa.String(36), sa.ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("serial_number", sa.Integer(), nullable=False),
        sa.Column("function", sa.String(128), nullable=False, server_default="solution"),
        sa.Column("input", sa.Text(), nullable=False),
        sa.Column("expected_output", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    
    # Drop the old test_cases JSON column from problems table
    op.drop_column("problems", "test_cases")


def downgrade():
    # Add back the test_cases column
    op.add_column("problems", sa.Column("test_cases", sa.JSON(), nullable=False, server_default="[]"))
    
    # Drop the test_cases table
    op.drop_table("test_cases")
