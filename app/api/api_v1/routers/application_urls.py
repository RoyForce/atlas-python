from fastapi import APIRouter, Depends, Response, Request
import typing as t

from app.db.session import get_db
from app.db.application_urls import models
from app.db.core import (
    get_lists,
    get_item,
    create_item,
    delete_item,
    edit_item,
)

from app.db.application_urls.schemas import (
    ApplicationUrlEdit,
    ApplicationUrlOut,
)
from app.core.auth import get_current_active_user

application_urls_router = r = APIRouter()


@r.get(
    "/application-urls",
    response_model=t.List[ApplicationUrlOut],
)
async def application_urls_list(
    request: Request,
    response: Response,
    db=Depends(get_db),
):
    """
    Get all application_urls
    """
    application_urls = get_lists(
        db, models.ApplicationUrl, request.query_params
    )
    response.headers["Content-Range"] = f"0-9/{len(application_urls)}"
    return application_urls


@r.get(
    "/application-urls/{application_url_id}",
    response_model=ApplicationUrlOut,
)
async def application_urls_details(
    application_url_id: int,
    db=Depends(get_db),
):
    """
    Get any application-url details
    """
    return get_item(db, models.ApplicationUrl, application_url_id)


@r.post(
    "/application-urls",
    response_model=ApplicationUrlOut,
)
async def application_urls_create(
    application_url: ApplicationUrlEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Create a new application-url
    """
    application_url.created_by = current_user.id
    return create_item(db, models.ApplicationUrl, application_url)


@r.put(
    "/application-urls/{application_url_id}",
    response_model=ApplicationUrlOut,
)
async def application_urls_edit(
    application_url_id: int,
    application_url: ApplicationUrlEdit,
    db=Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update existing application-url
    """
    application_url.updated_by = current_user.id
    return edit_item(
        db, models.ApplicationUrl, application_url_id, application_url
    )


@r.delete(
    "/application-urls/{application_url_id}",
    response_model=ApplicationUrlOut,
)
async def application_urls_delete(
    application_url_id: int,
    db=Depends(get_db),
):
    """
    Delete existing application_url
    """
    return delete_item(db, models.ApplicationUrl, application_url_id)
