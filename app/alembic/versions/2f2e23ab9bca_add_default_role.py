"""add default role

Revision ID: 2f2e23ab9bca
Revises: 022bb07c9b94
Create Date: 2022-08-19 13:10:30.876414-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2f2e23ab9bca"
down_revision = "022bb07c9b94"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("INSERT INTO roles (name) VALUES('MANAGER')")


def downgrade():
    pass
