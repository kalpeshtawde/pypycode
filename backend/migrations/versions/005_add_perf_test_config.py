"""Add performance test configuration table

Revision ID: 005
Revises: 004
Create Date: 2026-04-05 20:45:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


perf_test_configs = sa.table(
    "perf_test_configs",
    sa.column("name", sa.String(length=64)),
    sa.column("enabled", sa.Boolean()),
    sa.column("base_url", sa.String(length=256)),
    sa.column("users", sa.Integer()),
    sa.column("ramp_up_seconds", sa.Integer()),
    sa.column("loops", sa.Integer()),
    sa.column("login_path", sa.String(length=128)),
    sa.column("submit_path", sa.String(length=128)),
    sa.column("login_email", sa.String(length=256)),
    sa.column("login_password", sa.String(length=256)),
    sa.column("problem_slug", sa.String(length=128)),
    sa.column("code", sa.Text()),
    sa.column("project_id", sa.String(length=36)),
)


def upgrade():
    op.create_table(
        "perf_test_configs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=64), nullable=False, unique=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("base_url", sa.String(length=256), nullable=False),
        sa.Column("users", sa.Integer(), nullable=False, server_default="100"),
        sa.Column("ramp_up_seconds", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("loops", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("login_path", sa.String(length=128), nullable=False),
        sa.Column("submit_path", sa.String(length=128), nullable=False),
        sa.Column("login_email", sa.String(length=256), nullable=False),
        sa.Column("login_password", sa.String(length=256), nullable=False),
        sa.Column("problem_slug", sa.String(length=128), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )

    bind = op.get_bind()
    bind.execute(
        perf_test_configs.insert().values(
            name="default",
            enabled=True,
            base_url="http://api_perf:5000",
            users=100,
            ramp_up_seconds=1,
            loops=1,
            login_path="/auth/login",
            submit_path="/submissions/",
            login_email="demo@pypycode.dev",
            login_password="demo1234",
            problem_slug="two-sum",
            code="def solution(nums, target):\n    return [0, 1]",
            project_id=None,
        )
    )

    op.alter_column("perf_test_configs", "enabled", server_default=None)
    op.alter_column("perf_test_configs", "users", server_default=None)
    op.alter_column("perf_test_configs", "ramp_up_seconds", server_default=None)
    op.alter_column("perf_test_configs", "loops", server_default=None)


def downgrade():
    op.drop_table("perf_test_configs")
