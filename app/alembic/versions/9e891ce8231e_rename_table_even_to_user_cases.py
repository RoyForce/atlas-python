"""rename_table_even_to_user_cases

Revision ID: 9e891ce8231e
Revises: 6cc46d40c68e
Create Date: 2022-11-06 03:33:14.114049-08:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9e891ce8231e"
down_revision = "6cc46d40c68e"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""CREATE TABLE "use_cases" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "table_config" text
        )"""
    )

    op.execute(
        f"""CREATE TABLE "use_cases_mappings" (
        "id" SERIAL PRIMARY KEY,
        "use_case_id" int,
        "job_id" int,
        "role_id" int,
        "value" bool DEFAULT false
        )"""
    )

    op.execute(
        f"""ALTER TABLE "use_cases_mappings" ADD FOREIGN KEY ("use_case_id") REFERENCES "use_cases" ("id")"""
    )
    op.execute(
        f"""ALTER TABLE "use_cases_mappings" ADD FOREIGN KEY ("job_id") REFERENCES "jobs" ("id")"""
    )
    op.execute(
        f"""ALTER TABLE "use_cases_mappings" ADD FOREIGN KEY ("role_id") REFERENCES "roles" ("id")"""
    )


def downgrade():
    op.drop_table("use_cases_mappings")
    op.drop_table("use_cases")
