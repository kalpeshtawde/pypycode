"""Add user profile fields (first_name, last_name, screen_name)

Revision ID: 002
Revises: 001
Create Date: 2026-04-05 12:48:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to users table
    op.add_column('users', sa.Column('first_name', sa.String(128), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(128), nullable=True))
    op.add_column('users', sa.Column('screen_name', sa.String(64), nullable=True))
    
    # Add unique constraint on screen_name
    op.create_unique_constraint('uq_users_screen_name', 'users', ['screen_name'])


def downgrade():
    # Remove unique constraint
    op.drop_constraint('uq_users_screen_name', 'users', type_='unique')
    
    # Remove columns
    op.drop_column('users', 'screen_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
