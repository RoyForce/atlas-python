from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.db.users import models as userModel
from app.db.users.crud import get_user_by_email

from app.db.application_types import models as AppTypeModels
from app.db.application_types import schemas as AppTypeSchemas

from app.db.enums import AppType, ResourceType, ResourceTypeUrl


def create_update_external_data(db: Session, raw_data, app_type_id_str, type):
    if len(raw_data) > 0:
        if app_type_id_str == AppType.JIRA_ALIGN.value:
            db_app_type = get_app_type(db, AppType.JIRA_ALIGN.value)
            app_type_id = None
            if db_app_type is not None:
                app_type_id = db_app_type.id
            if type == ResourceType.USER.value:
                return process_user_data(db, raw_data, app_type_id)


def get_app_type(
    db: Session, app_name: str
) -> AppTypeSchemas.ApplicationTypeBase:
    return (
        db.query(AppTypeModels.ApplicationType)
        .filter(AppTypeModels.ApplicationType.name == app_name)
        .first()
    )


def process_user_data(db: Session, raw_data, app_type_id):
    for user in raw_data:
        if user["status"] == "Active":
            db_user = get_user_by_email(db, user["email"])
            if db_user is None:
                db_user = userModel.User(
                    first_name=user["firstName"],
                    last_name=user["lastName"],
                    email=user["email"],
                    is_active=True,
                    role_id=1,
                    is_designer=False,
                    is_superuser=False,
                    app_type_id=app_type_id,
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
            else:
                update_data = dict(exclude_unset=True)
                update_data["first_name"] = (user["firstName"],)
                update_data["last_name"] = (user["lastName"],)
                for key, value in update_data.items():
                    setattr(db_user, key, value)

                db.add(db_user)
                db.commit()
                db.refresh(db_user)
    return True
