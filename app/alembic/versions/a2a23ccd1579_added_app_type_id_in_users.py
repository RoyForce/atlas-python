"""added-app-type-id-in-users

Revision ID: a2a23ccd1579
Revises: ee7a7d491ab4
Create Date: 2023-04-19 04:46:47.462127-07:00

"""
from sqlalchemy.dialects import postgresql
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a2a23ccd1579"
down_revision = "ee7a7d491ab4"
branch_labels = None
depends_on = None


def upgrade():
    source = postgresql.ENUM("INTERNAL", "EXTERNAL", name="source")
    source.create(op.get_bind(), checkfirst=True)
    op.add_column("users", sa.Column("source", source))
    op.alter_column("users", "source", server_default="INTERNAL")

    source_app = postgresql.ENUM("JIRA-ALIGN", "JIRA", name="source_type")
    source_app.create(op.get_bind(), checkfirst=True)
    op.add_column("users", sa.Column("source_app", source_app))
    op.add_column("users", sa.Column("source_id", sa.Integer(), nullable=True))
    op.add_column(
        "users",
        sa.Column(
            "source_update_date", sa.TIMESTAMP(timezone=True), nullable=True
        ),
    )

    source = postgresql.ENUM("INTERNAL", "EXTERNAL", name="source")
    source.create(op.get_bind(), checkfirst=True)
    op.add_column("roles", sa.Column("source", source))
    op.alter_column("roles", "source", server_default="INTERNAL")

    source_app = postgresql.ENUM("JIRA-ALIGN", "JIRA", name="source_type")
    source_app.create(op.get_bind(), checkfirst=True)
    op.add_column("roles", sa.Column("source_app", source_app))
    op.add_column("roles", sa.Column("source_id", sa.Integer(), nullable=True))
    op.add_column(
        "roles",
        sa.Column(
            "source_update_date", sa.TIMESTAMP(timezone=True), nullable=True
        ),
    )


def downgrade():
    op.drop_column("users", "source")
    source = postgresql.ENUM("INTERNAL", "EXTERNAL", name="source")
    source.drop(op.get_bind())

    op.drop_column("users", "source_app")
    source_app = postgresql.ENUM("JIRA-ALIGN", "JIRA", name="source_app")
    source_app.drop(op.get_bind())

    op.drop_column("users", "source_id")
    op.drop_column("users", "source_update_date")

    op.drop_column("roles", "source")
    source = postgresql.ENUM("INTERNAL", "EXTERNAL", name="source")
    source.drop(op.get_bind())

    op.drop_column("roles", "source_app")
    source_app = postgresql.ENUM("JIRA-ALIGN", "JIRA", name="source_app")
    source_app.drop(op.get_bind())

    op.drop_column("roles", "source_id")
    op.drop_column("roles", "source_update_date")
