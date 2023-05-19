from fastapi import HTTPException, status

from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import delete
from sqlalchemy.orm.attributes import flag_modified

from app.db.users import models as UserModel
from app.db.enums import Source, SourceApp, ResourceType
from app.db.roles import models as RoleModel


def create_update_external_data(db: Session, raw_data, source_app, type):
    if len(raw_data) > 0:
        if source_app == SourceApp.JIRA_ALIGN.value:
            if type == ResourceType.USER.value:
                process_user_data(db, raw_data, source_app)
    return True


def process_user_data(db: Session, raw_data, source_app):
    for user in raw_data:
        if user["status"] == "Active":
            if "role" in user:
                db_role_id = process_role_data(db, user["role"], source_app)
            db_user = get_source_user(db, user["id"], source_app)
            if db_user is None:
                db_user = UserModel.User(
                    first_name=user["firstName"],
                    last_name=user["lastName"],
                    email=user["email"],
                    is_active=True,
                    role_id=db_role_id,
                    is_designer=False,
                    is_superuser=False,
                    source=Source.EXTERNAL.value,
                    source_app=source_app,
                    source_id=user["id"],
                    source_update_date=user["lastUpdatedDate"],
                )
                db.add(db_user)
                db.commit()
                db.refresh(db_user)
            else:
                if user["lastUpdatedDate"] != None:
                    db_last_update = datetime.strptime(
                        db_user.source_update_date.strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "%Y-%m-%dT%H:%M:%SZ",
                    )
                    source_last_update = datetime.strptime(
                        user["lastUpdatedDate"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    if db_last_update < source_last_update:
                        update_data = dict(exclude_unset=True)
                        update_data["first_name"] = (user["firstName"],)
                        update_data["last_name"] = (user["lastName"],)
                        update_data["source_update_date"] = (
                            user["lastUpdatedDate"],
                        )
                        for key, value in update_data.items():
                            setattr(db_user, key, value)

                        db.add(db_user)
                        db.commit()
                        db.refresh(db_user)
    return True


def get_source_user(db: Session, source_id: int, source_app: str):
    return (
        db.query(UserModel.User)
        .filter(UserModel.User.source_app == source_app)
        .filter(UserModel.User.source_id == source_id)
        .first()
    )


def process_role_data(db: Session, role_data: int, source_app: str):
    db_role = (
        db.query(RoleModel.Role)
        .filter(RoleModel.Role.source_app == source_app)
        .filter(RoleModel.Role.source_id == role_data["id"])
        .first()
    )
    roleId = ""
    if db_role is None:
        print(role_data)
        db_role = RoleModel.Role(
            name=role_data["name"],
            description=role_data["description"],
            source=Source.EXTERNAL.value,
            source_app=source_app,
            source_id=role_data["id"],
            source_update_date=role_data["updateDate"],
        )
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        roleId = db_role.id
    else:
        if role_data["updateDate"] != None:
            db_last_update = datetime.strptime(
                db_role.source_update_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "%Y-%m-%dT%H:%M:%SZ",
            )
            source_last_update = datetime.strptime(
                role_data["updateDate"], "%Y-%m-%dT%H:%M:%SZ"
            )
            if db_last_update < source_last_update:
                update_data = dict(exclude_unset=True)
                update_data["name"] = (role_data["name"],)
                update_data["description"] = (role_data["description"],)
                update_data["source_update_date"] = (role_data["updateDate"],)
                for key, value in update_data.items():
                    setattr(db_role, key, value)

                db.add(db_role)
                db.commit()
                db.refresh(db_role)
        roleId = db_role.id
    return roleId
