"""create agility_plan_action table

Revision ID: a693ed586b0a
Revises: 3ab5f03e6f9f
Create Date: 2023-06-18 06:06:03.866549-07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "a693ed586b0a"
down_revision = "3ab5f03e6f9f"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agility_plan_action_relationship",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("agility_plan_id", sa.Integer()),
        sa.Column("action_id", sa.Integer()),
        sa.Column("start_time", sa.Date()),
        sa.Column("end_time", sa.Date()),
        sa.Column("dependency", sa.Integer()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("agility_plan_action_relationship")
