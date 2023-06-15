"""create agility plans relationship table

Revision ID: 803da6a5b057
Revises: 3ff343fde80d
Create Date: 2023-06-15 13:20:33.907156-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import AgilityPlanRelationType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "803da6a5b057"
down_revision = "3ff343fde80d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agility_plan_relations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agility_plan_id", sa.Integer),
        sa.Column("related_id", sa.Integer),
        sa.PrimaryKeyConstraint("id"),
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
