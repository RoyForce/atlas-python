"""job role mapping

Revision ID: e966fa303c0e
Revises: 8f67c164c554
Create Date: 2023-03-23 11:18:32.536842-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e966fa303c0e"
down_revision = "8f67c164c554"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("job_role_mappings")
    op.add_column(
        "jobs",
        sa.Column("role_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    pass
