"""add is_active to test_cases

Revision ID: 010
Revises: 009_add_test_cases_table
Create Date: 2025-04-11

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '010'
down_revision = '009'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_active column to test_cases table
    op.add_column('test_cases', sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'))


def downgrade():
    # Remove is_active column from test_cases table
    op.drop_column('test_cases', 'is_active')
