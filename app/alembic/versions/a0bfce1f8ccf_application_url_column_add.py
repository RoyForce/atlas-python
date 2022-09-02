"""application url column add

Revision ID: a0bfce1f8ccf
Revises: 2f2e23ab9bca
Create Date: 2022-09-02 08:58:41.237376-07:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, String


# revision identifiers, used by Alembic.
revision = 'a0bfce1f8ccf'
down_revision = '2f2e23ab9bca'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('application_urls',
        Column('url', String())   
    )


def downgrade():
    op.drop_column('application_urls', 'url')


