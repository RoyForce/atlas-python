"""crate screens table

Revision ID: 8f7da26167f7
Revises: 94b430f35ae8
Create Date: 2023-02-21 08:53:22.340570-08:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_refresh_updated_at_func, create_trigger



# revision identifiers, used by Alembic.
revision = '8f7da26167f7'
down_revision = '94b430f35ae8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""CREATE TABLE "screens" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "created_at" timestamp default current_timestamp,
        "updated_at" timestamp
        )"""
    )
    op.execute(
        sa.text(create_trigger.format(schema="public", table="screens"))
    )


def downgrade():
    op.execute(
        'DROP TABLE "screens"'
    )
