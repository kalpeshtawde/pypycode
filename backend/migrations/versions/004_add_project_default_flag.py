"""Add project default flag

Revision ID: 004
Revises: 003
Create Date: 2026-04-05 20:05:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


DEFAULT_PROJECT_NAME = "Interview prep 2026"


def upgrade():
    op.add_column("projects", sa.Column("is_default", sa.Boolean(), nullable=True, server_default=sa.false()))

    bind = op.get_bind()
    projects = sa.table(
        "projects",
        sa.column("id", sa.String(length=36)),
        sa.column("user_id", sa.String(length=36)),
        sa.column("name", sa.String(length=25)),
        sa.column("is_default", sa.Boolean()),
        sa.column("created_at", sa.DateTime()),
    )

    bind.execute(projects.update().values(is_default=False))

    user_ids = [
        row[0]
        for row in bind.execute(sa.select(sa.distinct(projects.c.user_id))).all()
    ]

    for user_id in user_ids:
        preferred = bind.execute(
            sa.select(projects.c.id)
            .where(projects.c.user_id == user_id, projects.c.name == DEFAULT_PROJECT_NAME)
            .order_by(projects.c.created_at.asc(), projects.c.id.asc())
            .limit(1)
        ).first()

        chosen = preferred
        if chosen is None:
            chosen = bind.execute(
                sa.select(projects.c.id)
                .where(projects.c.user_id == user_id)
                .order_by(projects.c.created_at.asc(), projects.c.id.asc())
                .limit(1)
            ).first()

        if chosen is not None:
            bind.execute(
                projects.update()
                .where(projects.c.id == chosen[0])
                .values(is_default=True)
            )

    op.alter_column(
        "projects",
        "is_default",
        existing_type=sa.Boolean(),
        nullable=False,
        server_default=None,
    )


def downgrade():
    op.drop_column("projects", "is_default")
