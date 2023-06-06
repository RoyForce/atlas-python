"""create-table-for-objective-result

Revision ID: e706726cdee0
Revises: 56fa1dd20d01
Create Date: 2023-06-04 22:54:30.907732-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns, create_trigger
from app.db.enums import MetricsType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "e706726cdee0"
down_revision = "56fa1dd20d01"
branch_labels = None
depends_on = None


def upgrade():
    columns = [
        sa.Column("start_value", sa.DECIMAL(), nullable=True),
        sa.Column("target_value", sa.DECIMAL(), nullable=True),
    ]
    create_table_with_default_columns(
        table_name="objectives", additional_columns=columns, skip_icon=True
    )

    metrics_type_enum = postgresql.ENUM(MetricsType, name="metrics_type_enum")
    metrics_type_enum.create(op.get_bind())
    op.add_column(
        "objectives",
        sa.Column("metrics_type", metrics_type_enum, nullable=False),
    )

    op.execute(
        f"""CREATE TABLE "results" (
        "id" SERIAL PRIMARY KEY,
        "objective_id" int,
        "value" int null,
        "created_by" int null,
        "updated_by" int null,
        "created_at" timestamp default current_timestamp,
        "updated_at" timestamp
        )"""
    )

    op.execute(
        f"""ALTER TABLE "results" ADD FOREIGN KEY ("objective_id") REFERENCES "objectives" ("id")"""
    )

    op.execute(
        sa.text(create_trigger.format(schema="public", table="results"))
    )


def downgrade():
    op.drop_table("results")
    op.drop_table("objectives")
    sa.Enum(name="metrics_type_enum").drop(op.get_bind(), checkfirst=False)
