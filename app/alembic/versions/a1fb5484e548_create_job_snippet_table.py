"""create job snippet table

Revision ID: a1fb5484e548
Revises: 4592faa7aa20
Create Date: 2023-06-13 13:56:13.167690-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns


# revision identifiers, used by Alembic.
revision = "a1fb5484e548"
down_revision = "4592faa7aa20"
branch_labels = None
depends_on = None


def upgrade():
    columns = [
        sa.Column("steps", sa.JSON(), nullable=True),
    ]
    create_table_with_default_columns(
        table_name="job_snippets", additional_columns=columns, skip_icon=True
    )


def downgrade():
    op.drop_table("job_snippets")
