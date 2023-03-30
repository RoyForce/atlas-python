"""create application type table changes

Revision ID: d00ef6a4c66c
Revises: 41b5635b9613
Create Date: 2023-03-27 04:04:25.323079-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_trigger

# revision identifiers, used by Alembic.
revision = "d00ef6a4c66c"
down_revision = "41b5635b9613"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        f"""CREATE TABLE "application_types" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "description" text,
        "created_at" timestamp default current_timestamp,
        "updated_at" timestamp
        )"""
    )
    op.execute(
        sa.text(
            create_trigger.format(schema="public", table="application_types")
        )
    )
    op.execute("""INSERT INTO application_types(name) VALUES ('Jira')""")
    op.execute("""INSERT INTO application_types(name) VALUES ('Jira Align')""")


def downgrade():
    op.execute('DROP TABLE "application_types"')
