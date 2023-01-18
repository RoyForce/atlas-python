"""additional colums

Revision ID: 62765241eb3e
Revises: 9e891ce8231e
Create Date: 2023-01-18 10:48:25.902302-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "62765241eb3e"
down_revision = "9e891ce8231e"
branch_labels = None
depends_on = None


def upgrade():
    for table in ["roles", "application_urls"]:
        op.add_column(
            table, sa.Column("description", sa.String, nullable=True)
        )


def downgrade():
    for table in ["roles", "application_urls"]:
        op.drop_column(table, "description")
