from app.core.auth import get_current_active_user
from fastapi import APIRouter, Request, Depends, Response
import typing as t

from app.db.session import get_db
from app.db.roles import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)
from app.db.roles.crud import delete_role_mapping
from app.db.roles.schemas import RoleCreate, RoleEdit, Role

roles_router = r = APIRouter()


@r.get(
    "/roles",
    response_model=t.List[Role],
    response_model_exclude_none=True,
)
async def roles_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get all roles
    """
    roles = get_lists(db, models.Role, request.query_params)
    response.headers["Content-Range"] = f"0-9/{len(roles)}"
    return roles


@r.get(
    "/roles/{role_id}",
    response_model=Role,
    response_model_exclude_none=True,
)
async def role_details(
    role_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Get any role details
    """
    return get_item(db, models.Role, role_id)


@r.post("/roles", response_model=Role, response_model_exclude_none=True)
async def role_create(
    role: RoleCreate,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Create a new role
    """
    return create_item(db, models.Role, role)


@r.put(
    "/roles/{role_id}", response_model=Role, response_model_exclude_none=True
)
async def role_edit(
    role_id: int,
    role: RoleEdit,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Update existing role
    """
    return edit_item(db, models.Role, role_id, role)


@r.delete(
    "/roles/{role_id}", response_model=Role, response_model_exclude_none=True
)
async def role_delete(
    role_id: int,
    db=Depends(get_db),
    current_playbooks=Depends(get_current_active_user),
):
    """
    Delete existing role
    """
    delete_role_mapping(db, role_id)
    return delete_item(db, models.Role, role_id)
