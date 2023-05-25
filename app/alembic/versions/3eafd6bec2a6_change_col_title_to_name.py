"""change-col-title-to-name

Revision ID: 3eafd6bec2a6
Revises: 9b0f7096fb3e
Create Date: 2023-05-25 03:44:16.891136-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3eafd6bec2a6"
down_revision = "9b0f7096fb3e"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "portfolios",
        "title",
        nullable=True,
        new_column_name="name",
    )
    op.alter_column(
        "programs",
        "title",
        nullable=True,
        new_column_name="name",
    )
    op.alter_column(
        "cost_centers",
        "title",
        nullable=True,
        new_column_name="name",
    )
    pass


def downgrade():
    pass
