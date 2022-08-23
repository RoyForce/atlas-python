from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.roles.crud import (
    get_roles,
    get_role,
    create_role,
    delete_role,
    edit_role,
)
from app.db.roles.schemas import RoleCreate, RoleEdit, Role, RoleOut
from app.core.auth import get_current_active_superuser

roles_router = r = APIRouter()


@r.get(
    "/roles",
    response_model=t.List[Role],
    response_model_exclude_none=True,
)
async def roles_list(
    response: Response,
    db=Depends(get_db),
    current_role=Depends(get_current_active_superuser),
):
    """
    Get all roles
    """
    roles = get_roles(db)
    response.headers["Content-Range"] = f"0-9/{len(roles)}"
    return roles


@r.get(
    "/roles/{role_id}",
    response_model=Role,
    response_model_exclude_none=True,
)
async def role_details(
    request: Request,
    role_id: int,
    db=Depends(get_db),
    current_role=Depends(get_current_active_superuser),
):
    """
    Get any role details
    """
    role = get_role(db, role_id)
    return role


@r.post("/roles", response_model=Role, response_model_exclude_none=True)
async def role_create(
    request: Request,
    role: RoleCreate,
    db=Depends(get_db),
    current_role=Depends(get_current_active_superuser),
):
    """
    Create a new role
    """
    return create_role(db, role)


@r.put(
    "/roles/{role_id}", response_model=Role, response_model_exclude_none=True
)
async def role_edit(
    request: Request,
    role_id: int,
    role: RoleEdit,
    db=Depends(get_db),
    current_role=Depends(get_current_active_superuser),
):
    """
    Update existing role
    """
    return edit_role(db, role_id, role)


@r.delete(
    "/roles/{role_id}", response_model=Role, response_model_exclude_none=True
)
async def role_delete(
    request: Request,
    role_id: int,
    db=Depends(get_db),
    current_role=Depends(get_current_active_superuser),
):
    """
    Delete existing role
    """
    return delete_role(db, role_id)
