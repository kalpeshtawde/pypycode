"""Drop legacy input and function columns from test_cases

Revision ID: 017
Revises: 016
Create Date: 2026-05-26

"""
from alembic import op
import sqlalchemy as sa


revision = "017"
down_revision = "016"
branch_labels = None
depends_on = None


def upgrade():
    # Drop old legacy columns that were superseded by test_input in migration 016
    op.drop_column('test_cases', 'input')
    op.drop_column('test_cases', 'function')


def downgrade():
    op.add_column('test_cases', sa.Column('function', sa.String(128), nullable=False, server_default='solution'))
    op.add_column('test_cases', sa.Column('input', sa.Text(), nullable=False, server_default=''))
