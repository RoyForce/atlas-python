""" job_screen_mapping

Revision ID: 8ca466894d02
Revises: e966fa303c0e
Create Date: 2023-03-25 08:01:03.426970-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8ca466894d02"
down_revision = "e966fa303c0e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "screens",
        sa.Column("job_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    op.drop_column("screens", "job_ids")
