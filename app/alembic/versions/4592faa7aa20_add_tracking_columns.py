"""add-tracking-columns

Revision ID: 4592faa7aa20
Revises: e706726cdee0
Create Date: 2023-06-08 11:22:58.977268-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4592faa7aa20"
down_revision = "e706726cdee0"
branch_labels = None
depends_on = None


tables = [
    "courses",
    "jobs",
    "lessons",
    "use_cases",
    "screens",
    "application_types",
    "application_urls",
    "screen_objects",
]


def upgrade():
    for table in tables:
        op.add_column(
            table,
            sa.Column("created_by", sa.Integer(), nullable=True),
        )
        op.add_column(
            table,
            sa.Column("updated_by", sa.Integer(), nullable=True),
        )


def downgrade():
    # for table in tables:
    #     op.drop_column(table, "created_by")
    #     op.drop_column(table, "updated_by")
    pass
