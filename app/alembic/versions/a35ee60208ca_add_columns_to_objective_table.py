"""add columns to objective table

Revision ID: a35ee60208ca
Revises: a693ed586b0a
Create Date: 2023-06-23 01:15:22.141697-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a35ee60208ca"
down_revision = "a693ed586b0a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "objectives",
        sa.Column(
            "agility_plan_id", sa.Integer(), sa.ForeignKey("agility_plans.id")
        ),
    )
    op.add_column(
        "objectives",
        sa.Column("stwert", sa.ForeignKey("users.id")),
    )


def downgrade():
    op.drop_column("objectives", "agility_plan_id")
    op.drop_column("objectives", "stwert")
