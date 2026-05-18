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
    
    # Step 2: Add new columns to test_cases with defaults
    op.add_column('test_cases', sa.Column('test_input', postgresql.JSONB, nullable=True, server_default='{}'))
    op.add_column('test_cases', sa.Column('comparison_strategy', sa.String(32), nullable=True))
    
    # Step 3: Migrate data from old format to new format
    # This uses raw SQL to convert existing data
    op.execute("""
        UPDATE test_cases
        SET test_input = CASE 
            WHEN "input" IS NOT NULL THEN 
                jsonb_build_object('args', json_array_elements(
                    CASE 
                        WHEN "input" ~ '^\\[' THEN "input"::json
                        ELSE json_build_array("input")
                    END
                ))
            ELSE '{}'::jsonb
        END
        WHERE test_input = '{}'::jsonb OR test_input IS NULL
    """)
    
    # Step 4: Convert expected_output to JSONB, handling both JSON and string values
    op.execute("""
        UPDATE test_cases
        SET expected_output = CASE
            WHEN expected_output IS NULL THEN 'null'::jsonb
            WHEN expected_output ~ '^\\d+$' THEN expected_output::integer::jsonb
            WHEN expected_output ~ '^\\[' THEN expected_output::jsonb
            WHEN expected_output ~ '^{' THEN expected_output::jsonb
            WHEN expected_output = 'true' OR expected_output = 'false' THEN expected_output::boolean::jsonb
            ELSE expected_output::text::jsonb
        END
        WHERE expected_output IS NOT NULL
    """)
    
    # Step 5: Make test_input NOT NULL after migration
    op.alter_column('test_cases', 'test_input', nullable=False)
    
    # Step 6: Change expected_output type to JSONB
    op.alter_column('test_cases', 'expected_output', 
                    existing_type=sa.Text, 
                    type_=postgresql.JSONB,
                    existing_nullable=False)
    
    # Step 7: Keep old columns for backward compatibility (optional, can be removed later)
    # This allows rollback if needed
    # Don't drop columns yet - keep them for safety


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
