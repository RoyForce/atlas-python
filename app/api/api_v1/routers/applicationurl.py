from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.applicationurls.crud import (
    get_applicationurls,
    get_applicationurl,
    create_applicationurl,
    delete_applicationurl,
    edit_applicationurl,
)
from app.db.applicationurls.schemas import (
    ApplicationUrlCreate,
    ApplicationUrlEdit,
    ApplicationUrl,
    ApplicationUrlOut,
)
from app.core.auth import get_current_active_superuser

applicationurls_router = r = APIRouter()


@r.get(
    "/application-urls",
    response_model=t.List[ApplicationUrl],
    response_model_exclude_none=True,
)
async def applicationurls_list(
    response: Response,
    db=Depends(get_db),
    current_applicationurl=Depends(get_current_active_superuser),
):
    """
    Get all applicationurls
    """
    applicationurls = get_applicationurls(db)
    response.headers["Content-Range"] = f"0-9/{len(applicationurls)}"
    return applicationurls


@r.get(
    "/application-urls/{applicationurl_id}",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def application_urls_details(
    request: Request,
    applicationurl_id: int,
    db=Depends(get_db),
    current_applicationurl=Depends(get_current_active_superuser),
):
    """
    Get any application-url details
    """
    applicationurl = get_applicationurl(db, applicationurl_id)
    return applicationurl


@r.post(
    "/application-urls",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def applicationurls_create(
    request: Request,
    applicationurl: ApplicationUrlCreate,
    db=Depends(get_db),
    current_applicationurl=Depends(get_current_active_superuser),
):
    """
    Create a new application-url
    """
    return create_applicationurl(db, applicationurl)


@r.put(
    "/application-urls/{applicationurl_id}",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def applicationurls_edit(
    request: Request,
    applicationurl_id: int,
    applicationurl: ApplicationUrlEdit,
    db=Depends(get_db),
    current_applicationurl=Depends(get_current_active_superuser),
):
    """
    Update existing application-url
    """
    return edit_applicationurl(db, applicationurl_id, applicationurl)


@r.delete(
    "/application-urls/{applicationurl_id}",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def applicationurls_delete(
    request: Request,
    applicationurl_id: int,
    db=Depends(get_db),
    current_applicationurl=Depends(get_current_active_superuser),
):
    """
    Delete existing applicationurl
    """
    return delete_applicationurl(db, applicationurl_id)
