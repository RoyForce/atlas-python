"""screen objects

Revision ID: 33b129d9c3c3
Revises: a2a23ccd1579
Create Date: 2023-05-19 12:39:11.999419-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_trigger


# revision identifiers, used by Alembic.
revision = "33b129d9c3c3"
down_revision = "a2a23ccd1579"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""CREATE TABLE "screen_objects" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "properties" json,
        "screen_id" int NOT NULL,
        "created_at" timestamp default current_timestamp,
        "updated_at" timestamp
        )"""
    )
    op.execute(
        f"""ALTER TABLE "screen_objects" ADD FOREIGN KEY ("screen_id") REFERENCES "screens" ("id")"""
    )
    op.execute(
        sa.text(create_trigger.format(schema="public", table="screen_objects"))
    )


def downgrade():
    op.execute('DROP TABLE "screen_objects"')
