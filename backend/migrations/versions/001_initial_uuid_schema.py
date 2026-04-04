"""Initial schema with UUID primary keys

Revision ID: 001
Revises: 
Create Date: 2026-04-03 20:37:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('username', sa.String(64), nullable=False),
        sa.Column('email', sa.String(256), nullable=False),
        sa.Column('password_hash', sa.String(256), nullable=True),
        sa.Column('google_id', sa.String(256), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('google_id')
    )

    # Create problems table
    op.create_table(
        'problems',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('slug', sa.String(128), nullable=False),
        sa.Column('title', sa.String(256), nullable=False),
        sa.Column('difficulty', sa.String(16), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('starter_code', sa.Text(), nullable=False),
        sa.Column('test_cases', sa.JSON(), nullable=False),
        sa.Column('examples', sa.JSON(), nullable=False),
        sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug')
    )

    # Create submissions table
    op.create_table(
        'submissions',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('user_id', sa.String(36), nullable=False),
        sa.Column('problem_id', sa.String(36), nullable=False),
        sa.Column('code', sa.Text(), nullable=False),
        sa.Column('language', sa.String(16), nullable=True),
        sa.Column('status', sa.String(32), nullable=True),
        sa.Column('passed_tests', sa.Integer(), nullable=True),
        sa.Column('total_tests', sa.Integer(), nullable=True),
        sa.Column('runtime_ms', sa.Float(), nullable=True),
        sa.Column('memory_kb', sa.Float(), nullable=True),
        sa.Column('error_output', sa.Text(), nullable=True),
        sa.Column('task_id', sa.String(64), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['problem_id'], ['problems.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('submissions')
    op.drop_table('problems')
    op.drop_table('users')
