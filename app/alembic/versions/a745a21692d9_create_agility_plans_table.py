"""create agility_plans table

Revision ID: a745a21692d9
Revises: 14bf24aa7861
Create Date: 2023-06-13 05:40:19.423855-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import OrganizationType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "a745a21692d9"
down_revision = "14bf24aa7861"
branch_labels = None
depends_on = None


def upgrade():
    create_table_with_default_columns(
        table_name="agility_plans", additional_columns=[]
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
