from alembic import op
import sqlalchemy as sa

create_refresh_updated_at_func = """
    CREATE FUNCTION {schema}.refresh_updated_at()
    RETURNS TRIGGER
    LANGUAGE plpgsql AS
    $func$
    BEGIN
       NEW.updated_at := now();
       RETURN NEW;
    END
    $func$;
    """

create_trigger = """
    CREATE TRIGGER trig_{table}_updated BEFORE UPDATE ON {schema}.{table}
    FOR EACH ROW EXECUTE PROCEDURE {schema}.refresh_updated_at();
    """


def create_table_with_default_columns(
    table_name, additional_columns, skip_icon=False
):
    op.create_table(
        table_name,
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        *additional_columns,
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column("updated_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        ),
        sa.Column("icon_path", sa.String(), nullable=True)
        if not skip_icon
        else None,
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        sa.text(create_trigger.format(schema="public", table=table_name))
    )
