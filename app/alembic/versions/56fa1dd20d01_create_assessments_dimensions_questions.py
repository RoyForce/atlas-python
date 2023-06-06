"""create-assessments-dimensions-questions

Revision ID: 56fa1dd20d01
Revises: 9e07696e059f
Create Date: 2023-06-03 07:45:31.697187-07:00

"""
from alembic import op
import sqlalchemy as sa
from app.alembic.utils import create_table_with_default_columns


# revision identifiers, used by Alembic.
revision = "56fa1dd20d01"
down_revision = "9e07696e059f"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table("audit_trails")
    op.drop_table("question_answers")
    op.drop_table("quiz_questions_mapping")
    op.drop_table("questions")
    op.drop_table("user_question_answers")
    op.drop_table("user_items")
    op.drop_table("quizzes")
    columns = []
    create_table_with_default_columns(
        table_name="assessments", additional_columns=columns, skip_icon=True
    )

    columns = [
        sa.Column("assessment_id", sa.Integer(), nullable=False),
        sa.Column("baseline_value", sa.Integer(), nullable=False),
        sa.Column("ideal_value", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["assessment_id"], ["assessments.id"], ondelete="CASCADE"
        ),
    ]
    create_table_with_default_columns(
        table_name="dimensions", additional_columns=columns, skip_icon=True
    )

    columns = [
        sa.Column("dimension_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["dimension_id"], ["dimensions.id"], ondelete="CASCADE"
        ),
    ]
    create_table_with_default_columns(
        table_name="questions", additional_columns=columns, skip_icon=True
    )


def downgrade():
    op.drop_table("questions")
    op.drop_table("dimensions")
    op.drop_table("assessments")
