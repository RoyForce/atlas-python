"""“drop_table_user_table_views”

Revision ID: 6cc46d40c68e
Revises: 276795adcf57
Create Date: 2022-11-03 06:32:16.680997-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "6cc46d40c68e"
down_revision = "276795adcf57"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("user_table_views")


def downgrade():
    pass
