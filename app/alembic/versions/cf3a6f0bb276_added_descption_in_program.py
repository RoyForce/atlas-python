"""added_descption_in_program

Revision ID: cf3a6f0bb276
Revises: 3eafd6bec2a6
Create Date: 2023-05-26 00:47:48.180037-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "cf3a6f0bb276"
down_revision = "3eafd6bec2a6"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "programs",
        sa.Column("description", sa.String()),
    )


def downgrade():
    pass
