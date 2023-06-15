"""create agility plans table

Revision ID: 013d99a466b1
Revises: e706726cdee0
Create Date: 2023-06-15 13:20:03.979333-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import OrganizationType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "013d99a466b1"
down_revision = "e706726cdee0"
branch_labels = None
depends_on = None


def upgrade():
    create_table_with_default_columns(
        table_name="agility_plans", additional_columns=[]
    )


def downgrade():
    op.drop_table("agility_plans")
