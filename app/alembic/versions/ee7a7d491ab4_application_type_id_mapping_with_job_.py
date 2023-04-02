"""application type id mapping with job and screen

Revision ID: ee7a7d491ab4
Revises: de9c67896f1f
Create Date: 2023-04-02 00:10:58.273168-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ee7a7d491ab4"
down_revision = "de9c67896f1f"
branch_labels = None
depends_on = None


def upgrade():
    for table in ["jobs", "screens"]:
        op.add_column(
            table,
            sa.Column("application_type_id", sa.Integer(), nullable=True),
        )


def downgrade():
    for table in ["jobs", "screens"]:
        op.drop_column(table, "application_type_id")
