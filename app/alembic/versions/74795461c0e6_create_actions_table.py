"""create actions table

Revision ID: 74795461c0e6
Revises: e706726cdee0
Create Date: 2023-06-09 02:08:20.699730-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "74795461c0e6"
down_revision = "e706726cdee0"
branch_labels = None
depends_on = None


def upgrade():
    columns = [
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
    ]
    create_table_with_default_columns(
        table_name="actions", additional_columns=columns
    )
    action_type_enum = postgresql.ENUM(ActionType, name="action_type_enum")
    action_type_enum.create(op.get_bind())
    op.add_column(
        "actions",
        sa.Column("action_type", action_type_enum, nullable=True),
    )


def downgrade():
    op.drop_table("actions")
    op.drop_column("actions", "action_type")
    op.execute("DROP TYPE organization_type_enum;")
