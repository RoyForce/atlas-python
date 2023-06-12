"""create agility_plan objective relationship table

Revision ID: cd33b7222ed6
Revises: f2eedfdcea99
Create Date: 2023-06-12 03:14:31.991332-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "cd33b7222ed6"
down_revision = "f2eedfdcea99"
branch_labels = None
depends_on = None


def upgrade():
    create_table_with_default_columns(
        table_name="re_agility_plan_objective", additional_columns=[]
    )
    op.add_column(
        "re_agility_plan_objective",
        sa.Column("agility_plan_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "re_agility_plan_objective",
        sa.Column("objective_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_table("re_agility_plan_objective")
