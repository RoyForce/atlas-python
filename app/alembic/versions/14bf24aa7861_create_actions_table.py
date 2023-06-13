"""create actions table

Revision ID: 14bf24aa7861
Revises: 1272ef128b86
Create Date: 2023-06-13 05:39:40.032929-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "14bf24aa7861"
down_revision = "1272ef128b86"
branch_labels = None
depends_on = None


def upgrade():
    create_table_with_default_columns(
        table_name="actions", additional_columns=[]
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
