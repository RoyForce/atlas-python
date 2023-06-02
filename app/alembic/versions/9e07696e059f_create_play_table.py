"""create play table

Revision ID: 9e07696e059f
Revises: cf3a6f0bb276
Create Date: 2023-06-01 07:09:40.761081-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import OrganizationType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "9e07696e059f"
down_revision = "cf3a6f0bb276"
branch_labels = None
depends_on = None


def upgrade():
    columns = [
        sa.Column("playbook_id", sa.Integer(), nullable=False),
        sa.Column("jobs", sa.JSON(), nullable=True),
        sa.Column("start_datetime", sa.DateTime(), nullable=True),
        sa.Column("duration", sa.Interval(), nullable=True),
        sa.Column("order", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["playbook_id"], ["playbooks.id"], ondelete="CASCADE"
        ),
    ]
    create_table_with_default_columns(
        table_name="plays", additional_columns=columns
    )

    op.add_column(
        "playbooks", sa.Column("is_active", sa.Boolean(), nullable=True)
    )
    op.add_column(
        "playbooks", sa.Column("created_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "playbooks", sa.Column("updated_by", sa.Integer(), nullable=True)
    )
    op.add_column(
        "playbooks",
        sa.Column("owner_id", sa.Integer(), nullable=True),
    )
    op.add_column(
        "playbooks",
        sa.Column("coaches", sa.JSON(), nullable=True),
    )
    organization_type_enum = postgresql.ENUM(
        OrganizationType, name="organization_type_enum"
    )
    organization_type_enum.create(op.get_bind())
    op.add_column(
        "playbooks",
        sa.Column("org_type", organization_type_enum, nullable=True),
    )
    op.add_column(
        "playbooks",
        sa.Column("org_ids", sa.ARRAY(sa.Integer()), nullable=True),
    )


def downgrade():
    op.drop_table("plays")
    op.drop_column("playbooks", "is_active")
    op.drop_column("playbooks", "created_by")
    op.drop_column("playbooks", "updated_by")
    op.drop_column("playbooks", "owner_id")
    op.drop_column("playbooks", "coaches")
    op.drop_column("playbooks", "org_type")
    op.drop_column("playbooks", "org_ids")
    op.execute("DROP TYPE organization_type_enum;")
