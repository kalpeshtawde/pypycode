"""Add tag_patterns table

Revision ID: 020
Revises: 019
Create Date: 2026-10-31

"""
from alembic import op
import sqlalchemy as sa


revision = "020"
down_revision = "019"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tag_patterns',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tag', sa.String(128), nullable=False, unique=True, index=True),
        sa.Column('pattern', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('tag_patterns')
