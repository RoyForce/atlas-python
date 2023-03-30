"""add application_type_id in application_urls

Revision ID: de9c67896f1f
Revises: d00ef6a4c66c
Create Date: 2023-03-30 03:36:22.129337-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "de9c67896f1f"
down_revision = "d00ef6a4c66c"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "application_urls",
        sa.Column("application_type_id", sa.Integer(), nullable=True),
    )


def downgrade():
    op.drop_column("application_urls", "application_type_id")
