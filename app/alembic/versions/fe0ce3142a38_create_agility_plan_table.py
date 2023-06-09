"""create agility plan table

Revision ID: fe0ce3142a38
Revises: 74795461c0e6
Create Date: 2023-06-09 05:11:39.058505-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import OrganizationType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'fe0ce3142a38'
down_revision = '74795461c0e6'
branch_labels = None
depends_on = None


def upgrade():
    columns = [
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
    ]
    create_table_with_default_columns(
        table_name="agility_plans", additional_columns=columns
    )
    op.add_column(
        "agility_plans",
        sa.Column("action_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("role_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("user_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("org_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    op.drop_table("agility_plans")
