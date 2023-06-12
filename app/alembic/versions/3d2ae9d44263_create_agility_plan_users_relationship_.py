"""create agility_plan users relationship table

Revision ID: 3d2ae9d44263
Revises: cd33b7222ed6
Create Date: 2023-06-12 03:16:10.119993-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3d2ae9d44263"
down_revision = "cd33b7222ed6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "re_agility_plan_user",
        sa.Column("agility_plan_id", sa.Integer),
        sa.Column("user_id", sa.Integer),
    )


def downgrade():
    op.drop_table("re_agility_plan_user")
