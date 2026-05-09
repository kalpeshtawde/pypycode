"""add ai metadata to projects and widen name column

Revision ID: 014
Revises: 013
Create Date: 2026-05-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "014"
down_revision = "013"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("projects") as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=25),
            type_=sa.String(length=80),
            existing_nullable=False,
        )
        batch_op.add_column(sa.Column("goal", sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column("strategy", sa.String(length=32), nullable=True))
        batch_op.add_column(sa.Column("level", sa.String(length=16), nullable=True))
        batch_op.add_column(sa.Column("explanation", sa.Text(), nullable=True))
        batch_op.add_column(sa.Column("ai_metadata", sa.JSON(), nullable=True))


def downgrade():
    with op.batch_alter_table("projects") as batch_op:
        batch_op.drop_column("ai_metadata")
        batch_op.drop_column("explanation")
        batch_op.drop_column("level")
        batch_op.drop_column("strategy")
        batch_op.drop_column("goal")
        batch_op.alter_column(
            "name",
            existing_type=sa.String(length=80),
            type_=sa.String(length=25),
            existing_nullable=False,
        )
