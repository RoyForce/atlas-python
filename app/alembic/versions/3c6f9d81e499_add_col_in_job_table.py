"""“add_col_in_job_table”

Revision ID: 3c6f9d81e499
Revises: a0bfce1f8ccf
Create Date: 2022-10-13 09:49:18.408120-07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Boolean


# revision identifiers, used by Alembic.
revision = "3c6f9d81e499"
down_revision = "a0bfce1f8ccf"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("jobs", Column("is_template", Boolean))


def downgrade():
    op.drop_column("jobs", "is_template")
