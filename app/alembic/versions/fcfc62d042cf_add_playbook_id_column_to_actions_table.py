"""add playbook_id column to actions table

Revision ID: fcfc62d042cf
Revises: 803da6a5b057
Create Date: 2023-06-15 18:17:12.456861-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "fcfc62d042cf"
down_revision = "803da6a5b057"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "actions",
        sa.Column("playbook_id", sa.Integer(), nullable=True),
    )


def downgrade():
    pass
