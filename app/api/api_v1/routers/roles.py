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
    soft_delete_item,
)
from app.db.roles.crud import delete_all_role_mappings, update_role_mappings
from app.db.roles.schemas import RoleCreate, RoleEdit, Role
from app.core.auth import get_current_active_user

roles_router = r = APIRouter()


@r.get(
    "/roles",
    response_model=t.List[Role],
)
async def roles_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
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
)
async def role_details(
    role_id: int,
    db=Depends(get_db),
):
    """
    Get any role details
    """
    return get_item(db, models.Role, role_id)


@r.post("/roles", response_model=Role)
async def role_create(
    role: RoleCreate,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new role
    """
    role.created_by = current_user.id
    new_role = create_item(db, models.Role, role)
    update_role_mappings(db, new_role.id, role)
    return new_role


@r.put("/roles/{role_id}", response_model=Role)
async def role_edit(
    role_id: int,
    role: RoleEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing role
    """
    role.updated_by = current_user.id
    update_role_mappings(db, role_id, role)
    return edit_item(db, models.Role, role_id, role)


@r.delete("/roles/{role_id}", response_model=Role)
async def role_delete(
    role_id: int,
    db=Depends(get_db),
):
    """
    Delete existing role
    """
    # delete_all_role_mappings(db, role_id)
    return soft_delete_item(db, models.Role, role_id)
