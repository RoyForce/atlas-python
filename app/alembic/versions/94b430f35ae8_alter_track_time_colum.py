"""alter track time colum

Revision ID: 94b430f35ae8
Revises: a850bfb6f346
Create Date: 2023-02-17 11:42:48.963512-08:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_refresh_updated_at_func, create_trigger


# revision identifiers, used by Alembic.
revision = "94b430f35ae8"
down_revision = "a850bfb6f346"
branch_labels = None
depends_on = None

tables = [
    "application_urls",
    "jobs",
    "users",
    "courses",
    "lessons",
    "playbooks",
    "roles",
    "use_cases",
]


def upgrade():
    op.execute(sa.text(create_refresh_updated_at_func.format(schema="public")))
    for table in tables:
        op.alter_column(
            table,
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        )
        op.alter_column(
            table,
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        )
        op.execute(
            sa.text(create_trigger.format(schema="public", table=table))
        )


def downgrade():
    pass
