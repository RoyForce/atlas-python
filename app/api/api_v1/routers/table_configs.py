from fastapi import APIRouter, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.table_configs.crud import (
    get_table_configs,
    get_table_config,
    create_table_config,
    delete_table_config,
    edit_table_config,
)
from app.db.table_configs.schemas import (
    TableConfigCreate,
    TableConfigEdit,
    TableConfig,
    TableConfigOut,
)
from app.core.auth import get_current_active_superuser

table_config_router = r = APIRouter()


@r.get(
    "/table-configs",
    response_model=t.List[TableConfig],
    response_model_exclude_none=True,
)
async def table_configs_list(
    response: Response,
    db=Depends(get_db),
):
    """
    Get all TableConfigs
    """
    table_configs = get_table_configs(db)
    response.headers["Content-Range"] = f"0-9/{len(table_configs)}"
    return table_configs


@r.get(
    "/table-config/{id}",
    response_model=TableConfig,
    response_model_exclude_none=True,
)
async def table_config_details(
    id: int,
    db=Depends(get_db),
):
    """
    Get any table config details
    """
    table_configs = get_table_config(db, id)
    return table_configs


@r.post(
    "/table-config",
    response_model=TableConfigOut,
    response_model_exclude_none=True,
)
async def table_config_create(
    table_config: TableConfigCreate,
    db=Depends(get_db),
):
    """
    Create a new table_config
    """
    return create_table_config(db, table_config)


@r.put(
    "/table-configs/{id}",
    response_model=TableConfig,
    response_model_exclude_none=True,
)
async def table_configs_edit(
    id: int,
    table_configs: TableConfigEdit,
    db=Depends(get_db),
):
    """
    Update existing TableConfig
    """
    return edit_table_config(db, id, table_configs)


@r.delete(
    "/table-configs/{id}",
    response_model=TableConfig,
    response_model_exclude_none=True,
)
async def table_config_delete(
    id: int,
    db=Depends(get_db),
):
    """
    Delete existing table_configs
    """
    return delete_table_config(db, id)
