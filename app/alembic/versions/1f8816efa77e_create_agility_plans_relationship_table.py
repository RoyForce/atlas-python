"""create agility_plans_relationship table

Revision ID: 1f8816efa77e
Revises: a745a21692d9
Create Date: 2023-06-13 05:40:39.461678-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import AgilityPlanRelationType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "1f8816efa77e"
down_revision = "a745a21692d9"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agility_plan_relations",
        sa.Column("agility_plan_id", sa.Integer),
        sa.Column("related_id", sa.Integer),
    )
    agility_plan_relation_enum = postgresql.ENUM(
        AgilityPlanRelationType, name="agility_plan_relation_enum"
    )
    agility_plan_relation_enum.create(op.get_bind())
    op.add_column(
        "agility_plan_relations",
        sa.Column("relation_type", agility_plan_relation_enum, nullable=True),
    )


def downgrade():
    op.drop_table("agility_plan_relations")
