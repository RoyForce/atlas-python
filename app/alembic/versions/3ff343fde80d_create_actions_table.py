"""create actions table

Revision ID: 3ff343fde80d
Revises: 013d99a466b1
Create Date: 2023-06-15 13:20:16.936873-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "3ff343fde80d"
down_revision = "013d99a466b1"
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
    op.execute("DROP TYPE action_type_enum;")
