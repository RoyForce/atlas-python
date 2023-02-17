"""track time cloumns

Revision ID: a850bfb6f346
Revises: 62765241eb3e
Create Date: 2023-02-17 07:40:34.495620-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a850bfb6f346"
down_revision = "62765241eb3e"
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
    for table in tables:
        op.add_column(table, sa.Column("created_at", sa.DateTime))
        op.add_column(table, sa.Column("updated_at", sa.DateTime))


def downgrade():
    for table in tables:
        op.drop_column(table, "created_at")
        op.drop_column(table, "updated_at")
