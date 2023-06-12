"""add columns in agility_plans

Revision ID: f2eedfdcea99
Revises: fe0ce3142a38
Create Date: 2023-06-10 18:19:22.725813-07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Boolean


# revision identifiers, used by Alembic.
revision = "f2eedfdcea99"
down_revision = "fe0ce3142a38"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "agility_plans",
        sa.Column("lead_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("sponsor_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("core_team_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("coach_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "agility_plans",
        sa.Column("objective_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    op.drop_column("agility_plans", "lead_ids")
    op.drop_column("agility_plans", "sponsor_ids")
    op.drop_column("agility_plans", "core_team_ids")
    op.drop_column("agility_plans", "coach_ids")
    op.drop_column("agility_plans", "objective_ids")
