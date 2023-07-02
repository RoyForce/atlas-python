"""create-table-for-sprints-releases

Revision ID: ec39403ad4fd
Revises: a1fb5484e548
Create Date: 2023-06-20 06:58:43.247062-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns


# revision identifiers, used by Alembic.
revision = "ec39403ad4fd"
down_revision = "a1fb5484e548"
branch_labels = None
depends_on = None


def upgrade():
    columns = [
        sa.Column("short_name", sa.String(), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("portfolio_id", sa.Integer(), nullable=True),
        sa.Column("start_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("source_update_at", sa.DateTime(), nullable=True),
        sa.Column("program_ids", sa.ARRAY(sa.Integer()), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), default=False),
        sa.ForeignKeyConstraint(
            ["portfolio_id"], ["portfolios.id"], ondelete="CASCADE"
        ),
    ]
    create_table_with_default_columns(
        table_name="releases", additional_columns=columns, skip_icon=True
    )
    columns = [
        sa.Column("short_name", sa.String(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("program_id", sa.Integer(), nullable=True),
        sa.Column("release_id", sa.Integer(), nullable=True),
        sa.Column("source_id", sa.Integer(), nullable=True),
        sa.Column("begin_date", sa.DateTime(), nullable=True),
        sa.Column("end_date", sa.DateTime(), nullable=True),
        sa.Column("actual_end_date", sa.DateTime(), nullable=True),
        sa.Column("source_update_at", sa.DateTime(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), default=False),
        sa.ForeignKeyConstraint(["team_id"], ["teams.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["program_id"], ["programs.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["release_id"], ["releases.id"], ondelete="CASCADE"
        ),
    ]
    create_table_with_default_columns(
        table_name="sprints", additional_columns=columns, skip_icon=True
    )


def downgrade():
    op.drop_table("sprints")
    op.drop_table("releases")
