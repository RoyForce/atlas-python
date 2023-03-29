"""create_column_screen_url_screens

Revision ID: 41b5635b9613
Revises: 8ca466894d02
Create Date: 2023-03-29 01:59:34.038071-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "41b5635b9613"
down_revision = "8ca466894d02"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "screens",
        sa.Column("screen_url", sa.String(), nullable=True),
    )


def downgrade():
    pass
