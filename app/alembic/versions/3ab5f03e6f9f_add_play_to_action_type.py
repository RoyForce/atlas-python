"""add PLAY to action type

Revision ID: 3ab5f03e6f9f
Revises: fcfc62d042cf
Create Date: 2023-06-15 22:27:13.388357-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.db.enums import ActionType
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "3ab5f03e6f9f"
down_revision = "fcfc62d042cf"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE actions DROP COLUMN action_type;")
    op.execute("DROP TYPE action_type_enum;")
    action_type_enum = postgresql.ENUM(ActionType, name="action_type_enum")
    action_type_enum.create(op.get_bind())
    op.add_column(
        "actions",
        sa.Column("action_type", action_type_enum, nullable=True),
    )


def downgrade():
    pass
