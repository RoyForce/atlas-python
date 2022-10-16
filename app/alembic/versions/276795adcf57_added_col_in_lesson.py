"""“added_col_in_lesson”

Revision ID: 276795adcf57
Revises: 3c6f9d81e499
Create Date: 2022-10-15 21:38:57.112599-07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Boolean


# revision identifiers, used by Alembic.
revision = "276795adcf57"
down_revision = "3c6f9d81e499"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("lessons", Column("is_template", Boolean))


def downgrade():
    op.drop_column("lessons", "is_template")
