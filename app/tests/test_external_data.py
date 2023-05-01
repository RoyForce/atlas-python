from app.db.external_data import engine
from app.db.enums import AppType, ResourceType
from app.db.users import models


def test_fetch_external_data(
    client, test_db, superuser_token_headers, test_user
):
    user_data = [
        {
            "firstName": "UserFname",
            "lastName": "UserLastname",
            "email": "usertestemail@gmail.com",
            "status": "Active",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, user_data, AppType.JIRA_ALIGN.value, ResourceType.USER.value
    )

    user = (
        test_db.query(models.User)
        .filter(models.User.email == user_data[0]["email"])
        .first()
    )

    assert user_data[0]["email"] == user.email

    user_data = [
        {
            "firstName": "UpdatedFname",
            "lastName": "UserLastname",
            "email": "usertestemail@gmail.com",
            "status": "Active",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, user_data, AppType.JIRA_ALIGN.value, ResourceType.USER.value
    )

    user = (
        test_db.query(models.User)
        .filter(models.User.email == user_data[0]["email"])
        .first()
    )
    assert user_data[0]["firstName"] == user.first_name
