from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
import typing as t
import requests
from app.db.external_data import engine
from app.core import security

from app.db.enums import SourceApp, ResourceType, ResourceUrl


BEARER_TOKEN = "user:1229|PB[uuqXnMlJj9yV\j_nHZeEdszNanH=Hpm4O%Daw"
JA_BASE_URL = "https://cprime.jiraalign.com/rest/align/api/2"


def fetch_data_api(db: Session) -> str:
    app_types = []
    for app_type in SourceApp:
        app_types.append(app_type.value)

    fetch_resource = []
    for resource in ResourceType:
        fetch_resource.append(resource.value)

    for app_type in app_types:
        for resource in fetch_resource:
            if app_type == SourceApp.JIRA_ALIGN.value:
                session = requests.Session()
                session.headers.update(
                    {"Authorization": f"Bearer {BEARER_TOKEN}"}
                )
                path = ResourceUrl[ResourceType[resource].name].value
                url = f"{JA_BASE_URL}/{path}"
                params = {"$skip": 0}
                data = []

                while True:
                    response = session.get(url, params=params)
                    response.raise_for_status()
                    page = response.json()

                    data += page
                    if len(page) != 100:
                        break
                    params["$skip"] += 100

                response = engine.create_update_external_data(
                    db, data, app_type, resource
                )
    return f"Data fetched successfully"


def validate_external_api_token(request: Request):
    if f"Bearer {security.EXTERNAL_API_TOKEN}" != request.headers.get(
        "Authorization"
    ):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, detail="Invalid API token."
        )
