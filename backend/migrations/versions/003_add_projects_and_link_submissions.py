"""Add projects table and link submissions to projects

Revision ID: 003
Revises: 002
Create Date: 2026-04-05 19:50:00.000000

"""
from datetime import datetime, timezone
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


DEFAULT_PROJECT_NAME = "Interview prep 2026"


def upgrade():
    op.create_table(
        "projects",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=25), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.add_column("submissions", sa.Column("project_id", sa.String(length=36), nullable=True))

    bind = op.get_bind()
    submissions = sa.table(
        "submissions",
        sa.column("id", sa.String(length=36)),
        sa.column("user_id", sa.String(length=36)),
        sa.column("project_id", sa.String(length=36)),
    )
    projects = sa.table(
        "projects",
        sa.column("id", sa.String(length=36)),
        sa.column("user_id", sa.String(length=36)),
        sa.column("name", sa.String(length=25)),
        sa.column("created_at", sa.DateTime()),
    )

    user_ids = [
        row[0]
        for row in bind.execute(
            sa.select(sa.distinct(submissions.c.user_id)).where(submissions.c.user_id.is_not(None))
        ).all()
    ]

    now_utc = datetime.now(timezone.utc)
    for user_id in user_ids:
        project_id = str(uuid.uuid4())
        bind.execute(
            projects.insert().values(
                id=project_id,
                user_id=user_id,
                name=DEFAULT_PROJECT_NAME,
                created_at=now_utc,
            )
        )
        bind.execute(
            submissions.update()
            .where(submissions.c.user_id == user_id)
            .values(project_id=project_id)
        )

    op.alter_column("submissions", "project_id", existing_type=sa.String(length=36), nullable=False)
    op.create_foreign_key(
        "fk_submissions_project_id_projects",
        "submissions",
        "projects",
        ["project_id"],
        ["id"],
    )


def downgrade():
    op.drop_constraint("fk_submissions_project_id_projects", "submissions", type_="foreignkey")
    op.drop_column("submissions", "project_id")
    op.drop_table("projects")
