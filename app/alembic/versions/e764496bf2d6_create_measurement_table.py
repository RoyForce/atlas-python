"""create measurement table

Revision ID: e764496bf2d6
Revises: a35ee60208ca
Create Date: 2023-06-23 04:36:50.975387-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e764496bf2d6"
down_revision = "a35ee60208ca"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "measurements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "objective_id", sa.Integer(), sa.ForeignKey("objectives.id")
        ),
        sa.Column("value", sa.Numeric()),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("measurements")
