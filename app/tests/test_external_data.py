from app.db.external_data import engine
from app.db.enums import Source, SourceApp, ResourceType
from app.db.users import models as userModels


def test_fetch_external_data(
    client, test_db, superuser_token_headers, test_user
):
    user_data = [
        {
            "id": 1,
            "firstName": "UserFname",
            "lastName": "UserLastname",
            "email": "usertestemail@gmail.com",
            "status": "Active",
            "lastUpdatedDate": "2022-04-09T18:49:48Z",
            "role": {
                "id": 28,
                "name": "RTE - demo",
                "description": "Desc RTE - demo",
                "createDate": "2022-04-09T18:49:48Z",
                "updateDate": "2022-04-21T17:57:48Z",
            },
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, user_data, SourceApp.JIRA_ALIGN.value, ResourceType.USER.value
    )

    user = (
        test_db.query(userModels.User)
        .filter(userModels.User.email == user_data[0]["email"])
        .first()
    )
    assert user_data[0]["email"] == user.email

    user_data = [
        {
            "id": 1,
            "firstName": "UpdatedFname",
            "lastName": "UserLastname",
            "email": "usertestemail@gmail.com",
            "status": "Active",
            "lastUpdatedDate": "2022-04-10T18:49:48Z",
            "role": {
                "id": 3,
                "name": "RTE - updated demo",
                "description": "Desc RTE - updated demo",
                "createDate": "2022-04-09T18:49:48Z",
                "updateDate": "2022-04-21T17:57:48Z",
            },
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, user_data, SourceApp.JIRA_ALIGN.value, ResourceType.USER.value
    )

    user = (
        test_db.query(userModels.User)
        .filter(userModels.User.email == user_data[0]["email"])
        .first()
    )

    assert user_data[0]["firstName"] == user.first_name
