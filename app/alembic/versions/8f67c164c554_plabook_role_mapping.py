"""plabook role mapping

Revision ID: 8f67c164c554
Revises: eb8776df43a5
Create Date: 2023-03-23 10:53:46.341793-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8f67c164c554"
down_revision = "eb8776df43a5"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("playbook_role_mappings")
    op.add_column(
        "playbooks",
        sa.Column("role_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    pass
