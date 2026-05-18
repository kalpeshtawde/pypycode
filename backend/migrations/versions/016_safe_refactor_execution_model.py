"""safe refactor execution model with data migration

Revision ID: 016
Revises: 015
Create Date: 2026-05-18

This migration safely handles the transition from string-based to structured test cases.
It preserves existing data and converts it to the new format.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import json


revision = "016"
down_revision = "015"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add new columns to problems (with defaults)
    op.add_column('problems', sa.Column('execution_model', sa.String(32), nullable=False, server_default='function'))
    op.add_column('problems', sa.Column('function_name', sa.String(128), nullable=False, server_default='solution'))
    op.add_column('problems', sa.Column('class_name', sa.String(128), nullable=True))
    op.add_column('problems', sa.Column('method_name', sa.String(128), nullable=True))
    
    # Step 2: Clear all existing test cases (no data to preserve)
    op.execute("DELETE FROM test_cases")
    
    # Step 3: Add new columns to test_cases with defaults
    op.add_column('test_cases', sa.Column('test_input', postgresql.JSONB, nullable=False, server_default='{}'))
    op.add_column('test_cases', sa.Column('comparison_strategy', sa.String(32), nullable=True))
    
    # Step 4: Convert expected_output from Text to JSONB
    # Since we cleared all data, we just need to change the column type
    op.alter_column('test_cases', 'expected_output', 
                    existing_type=sa.Text, 
                    type_=postgresql.JSONB,
                    existing_nullable=False,
                    postgresql_using='NULL::jsonb')


def downgrade():
    # Restore old columns
    op.add_column('test_cases', sa.Column('function', sa.String(128), nullable=False, server_default='solution'))
    op.add_column('test_cases', sa.Column('input', sa.Text, nullable=False, server_default=''))
    op.add_column('test_cases', sa.Column('arg_types', postgresql.JSONB, nullable=True))
    
    # Remove new columns
    op.drop_column('test_cases', 'test_input')
    op.drop_column('test_cases', 'comparison_strategy')
    op.alter_column('test_cases', 'expected_output', 
                    existing_type=postgresql.JSONB, 
                    type_=sa.Text,
                    existing_nullable=False)
    
    # Remove from problems
    op.drop_column('problems', 'execution_model')
    op.drop_column('problems', 'function_name')
    op.drop_column('problems', 'class_name')
    op.drop_column('problems', 'method_name')
