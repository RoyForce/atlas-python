from fastapi import APIRouter, Request, Depends, Response, encoders
import typing as t

from app.db.session import get_db
from app.db.application_urls.crud import (
    get_application_urls,
    get_application_url,
    create_application_url,
    delete_application_url,
    edit_application_url,
)
from app.db.application_urls.schemas import (
    ApplicationUrlCreate,
    ApplicationUrlEdit,
    ApplicationUrl,
    ApplicationUrlOut,
)
from app.core.auth import get_current_active_superuser

application_urls_router = r = APIRouter()


@r.get(
    "/application-urls",
    response_model=t.List[ApplicationUrl],
    response_model_exclude_none=True,
)
async def application_urls_list(
    response: Response,
    db=Depends(get_db),
    current_application_url=Depends(get_current_active_superuser),
):
    """
    Get all application_urls
    """
    application_urls = get_application_urls(db)
    response.headers["Content-Range"] = f"0-9/{len(application_urls)}"
    return application_urls


@r.get(
    "/application-urls/{application_url_id}",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def application_urls_details(
    request: Request,
    application_url_id: int,
    db=Depends(get_db),
    current_application_url=Depends(get_current_active_superuser),
):
    """
    Get any application-url details
    """
    application_url = get_application_url(db, application_url_id)
    return application_url


@r.post(
    "/application-urls",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def application_urls_create(
    request: Request,
    application_url: ApplicationUrlCreate,
    db=Depends(get_db),
    current_application_url=Depends(get_current_active_superuser),
):
    """
    Create a new application-url
    """
    return create_application_url(db, application_url)


@r.put(
    "/application-urls/{application_url_id}",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def application_urls_edit(
    request: Request,
    application_url_id: int,
    application_url: ApplicationUrlEdit,
    db=Depends(get_db),
    current_application_url=Depends(get_current_active_superuser),
):
    """
    Update existing application-url
    """
    return edit_application_url(db, application_url_id, application_url)


@r.delete(
    "/application-urls/{application_url_id}",
    response_model=ApplicationUrl,
    response_model_exclude_none=True,
)
async def application_urls_delete(
    request: Request,
    application_url_id: int,
    db=Depends(get_db),
    current_application_url=Depends(get_current_active_superuser),
):
    """
    Delete existing application_url
    """
    return delete_application_url(db, application_url_id)
