"""added-app-type-id-in-users

Revision ID: a2a23ccd1579
Revises: ee7a7d491ab4
Create Date: 2023-04-19 04:46:47.462127-07:00

"""
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a2a23ccd1579"
down_revision = "ee7a7d491ab4"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "users", sa.Column("app_type_id", sa.Integer(), nullable=True)
    )


def downgrade():
    op.drop_column("users", "app_type_id")
