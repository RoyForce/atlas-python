"""“added_event_and_event_mapping”

Revision ID: fffd2635a3a1
Revises: 276795adcf57
Create Date: 2022-10-16 00:44:06.096483-07:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "fffd2635a3a1"
down_revision = "276795adcf57"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""CREATE TABLE "events" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "table_config" text
        )"""
    )

    op.execute(
        f"""CREATE TABLE "event_mappings" (
        "id" SERIAL PRIMARY KEY,
        "event_id" int,
        "job_id" int,
        "role_id" int,
        "value" bool DEFAULT false
        )"""
    )

    op.execute(
        f"""ALTER TABLE "event_mappings" ADD FOREIGN KEY ("event_id") REFERENCES "events" ("id")"""
    )
    op.execute(
        f"""ALTER TABLE "event_mappings" ADD FOREIGN KEY ("job_id") REFERENCES "jobs" ("id")"""
    )
    op.execute(
        f"""ALTER TABLE "event_mappings" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id")"""
    )


def downgrade():
    op.drop_table("event_mappings")
    op.drop_table("events")
