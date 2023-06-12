"""create agility_plan roles relationship table

Revision ID: 70474aec6938
Revises: 3d2ae9d44263
Create Date: 2023-06-12 03:16:20.246456-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "70474aec6938"
down_revision = "3d2ae9d44263"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "re_agility_plan_role",
        sa.Column("agility_plan_id", sa.Integer),
        sa.Column("role_id", sa.Integer),
    )


def downgrade():
    op.drop_table("re_agility_plan_role")
