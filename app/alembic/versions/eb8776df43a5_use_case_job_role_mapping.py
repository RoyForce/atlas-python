"""use case job role mapping

Revision ID: eb8776df43a5
Revises: 8f7da26167f7
Create Date: 2023-03-23 04:05:55.291575-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eb8776df43a5"
down_revision = "8f7da26167f7"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("use_cases_mappings")
    op.add_column(
        "use_cases",
        sa.Column("job_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )
    op.add_column(
        "use_cases",
        sa.Column("role_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    pass
