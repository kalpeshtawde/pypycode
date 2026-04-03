"""Add google_id column to users table

Revision ID: 001
Revises: 
Create Date: 2026-04-03 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add google_id column
    op.add_column('users', sa.Column('google_id', sa.String(256), nullable=True))
    # Create unique constraint on google_id
    op.create_unique_constraint('uq_users_google_id', 'users', ['google_id'])
    # Make password_hash nullable
    op.alter_column('users', 'password_hash', existing_type=sa.String(256), nullable=True)


def downgrade():
    # Remove unique constraint
    op.drop_constraint('uq_users_google_id', 'users')
    # Remove google_id column
    op.drop_column('users', 'google_id')
    # Make password_hash not nullable again
    op.alter_column('users', 'password_hash', existing_type=sa.String(256), nullable=False)
