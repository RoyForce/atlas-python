"""db_changes_for_JA_data

Revision ID: 9b0f7096fb3e
Revises: 33b129d9c3c3
Create Date: 2023-05-23 08:10:47.868889-07:00

"""
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa

from sqlalchemy import Column, Boolean

# revision identifiers, used by Alembic.
revision = "9b0f7096fb3e"
down_revision = "33b129d9c3c3"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("users", "source")
    op.drop_column("roles", "source")
    op.drop_column("roles", "source_app")
    op.drop_column("users", "source_app")
    source = postgresql.ENUM("INTERNAL", "EXTERNAL", name="source")
    source.drop(op.get_bind())
    source_app = postgresql.ENUM("JIRA-ALIGN", "JIRA", name="source_app")
    source_app.drop(op.get_bind())
    source1 = postgresql.ENUM("INTERNAL", "EXTERNAL", name="source")
    source1.drop(op.get_bind())
    source_app1 = postgresql.ENUM("JIRA-ALIGN", "JIRA", name="source_app")
    source_app1.drop(op.get_bind())

    op.alter_column(
        "users",
        "source_update_date",
        nullable=True,
        new_column_name="source_update_at",
    )
    op.alter_column(
        "roles",
        "source_update_date",
        nullable=True,
        new_column_name="source_update_at",
    )

    op.add_column(
        "users", sa.Column("cost_center_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "users", sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "users", sa.Column("updated_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "roles", sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "roles", sa.Column("updated_by", sa.Integer(), nullable=True)
    )

    op.add_column(
        "users", sa.Column("is_deleted", sa.Boolean(), default=False)
    )
    op.add_column(
        "roles", sa.Column("is_deleted", sa.Boolean(), default=False)
    )

    op.execute(
        f"""CREATE TABLE "team_types" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar
        )"""
    )
    op.execute(
        f"""CREATE TABLE "teams" (
        "id" SERIAL PRIMARY KEY,
        "name" varchar,
        "type" int,
        "program_id" int null,
        "description" varchar,
        "sprint_prefix" varchar,
        "short_name" varchar,
        "is_active" bool DEFAULT true,
        "is_deleted" bool DEFAULT false,
        "is_kanban_team" bool DEFAULT false,
        "source_id" int null,
        "source_update_at" timestamp null,
        "created_by" int null,
        "updated_by" int null,
        "created_at" timestamp,
        "updated_at" timestamp
        )"""
    )
    op.add_column(
        "teams",
        sa.Column("user_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )

    op.execute(
        f"""CREATE TABLE "programs" (
        "id" SERIAL PRIMARY KEY,
        "title" varchar,
        "portfolio_id" int null,
        "team_id" int null,
        "source_id" int null,
        "source_update_at" timestamp null,
        "is_active" bool DEFAULT true,
        "is_deleted" bool DEFAULT false,
        "created_by" int null,
        "updated_by" int null,
        "created_at" timestamp,
        "updated_at" timestamp
        )"""
    )
    op.execute(
        f"""CREATE TABLE "portfolios" (
        "id" SERIAL PRIMARY KEY,
        "title" varchar,
        "description" varchar,
        "team_id" int null,
        "is_active" int DEFAULT 1,
        "is_deleted" bool DEFAULT false,
        "source_id" int null,
        "source_update_at" timestamp null,
        "created_by" int null,
        "updated_by" int null,
        "created_at" timestamp,
        "updated_at" timestamp
        )"""
    )

    op.execute(
        f"""CREATE TABLE "cost_centers" (
        "id" SERIAL PRIMARY KEY,
        "title" varchar,
        "description" varchar,
        "hr_rate" int,
        "is_deleted" bool DEFAULT false,
        "source_id" int null,
        "source_update_at" timestamp null,
        "created_by" int null,
        "updated_by" int null,
        "created_at" timestamp,
        "updated_at" timestamp
        )"""
    )


def downgrade():
    op.drop_column("users", "cost_center_id")
    op.drop_column("users", "created_by")
    op.drop_column("users", "updated_by")
    op.drop_column("roles", "created_by")
    op.drop_column("roles", "updated_by")
    op.drop_column("users", "is_deleted")
    op.drop_column("roles", "is_deleted")
    op.drop_table("team_types")
    op.drop_table("teams")
    op.drop_table("programs")
    op.drop_table("portfolios")
    op.drop_table("cost_centers")
    pass
