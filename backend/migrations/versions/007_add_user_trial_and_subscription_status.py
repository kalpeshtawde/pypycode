"""Add user trial and subscription status fields

Revision ID: 007
Revises: 006
Create Date: 2026-04-09 09:55:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users",
        sa.Column("subscription_status", sa.String(length=64), nullable=False, server_default="none"),
    )
    op.add_column("users", sa.Column("trial_started_at", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("trial_ends_at", sa.DateTime(), nullable=True))
    op.add_column("users", sa.Column("trial_used", sa.Boolean(), nullable=False, server_default=sa.false()))

    op.alter_column("users", "subscription_status", server_default=None)
    op.alter_column("users", "trial_used", server_default=None)


def downgrade():
    op.drop_column("users", "trial_used")
    op.drop_column("users", "trial_ends_at")
    op.drop_column("users", "trial_started_at")
    op.drop_column("users", "subscription_status")
