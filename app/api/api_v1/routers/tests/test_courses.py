from app.db import courses
from app.db.courses.models import Course
import json
from fastapi.encoders import jsonable_encoder


def test_get_courses(client, test_course, superuser_token_headers):
    course = test_course.dict()
    response = client.get("/api/v1/courses", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == course[arg] for arg in course)


def test_delete_course(client, test_course, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/courses/{test_course.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Course).all() == []


# def test_get_course(
#     client,
#     test_course,
#     superuser_token_headers,
# ):
# response = client.get(
#     f"/api/v1/courses/{test_course.id}", headers=superuser_token_headers
# )
# assert response.status_code == 200
# assert response.json() == {
#         "id": test_course.id,
#         "name": test_course.name,
#         "description": test_course.description,
#         "duration": test_course.duration,
#         "enroll_required": test_course.enroll_required,
#         "passing_percentage": test_course.passing_percentage,
#         }
# -----------
# course = test_course.dict()
# response = client.get(
#     f"/api/v1/courses/{test_course.id}", headers=superuser_token_headers
# )
# assert response.status_code == 200
# assert all(response.json()[0][arg] == course[arg] for arg in course)


def test_create_course_with_items(client, test_course, superuser_token_headers):

    items = {
        "course_id": 1,
        "item_type": "SECTION",
        "item_title": "title string",
        "item_id": 0,
        "item_order": 1,
    }

    items_json = json.dumps(items, indent=4)

    course = {
        # "id": test_course.id,
        "name": "test name",
        "description": "test desc",
        "duration": 1,
        "enroll_required": True,
        "passing_percentage": 1,
        "items": [items_json],
    }
    response = client.post(
        "/api/v1/courses", json=course, headers=superuser_token_headers
    )
    assert response.status_code == 200
    # assert response.json()["items"][0] == items


def test_edit_course(client, test_course, superuser_token_headers):
    update_course = {
        "name": "test name",
        "description": "test desc",
        "duration": 1,
        "enroll_required": True,
        "passing_percentage": 1,
    }

    response = client.put(
        f"/api/v1/courses/{test_course.id}",
        json=update_course,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_course[arg] for arg in update_course
    )

    items = {
        "course_id": 1,
        "item_id": 1,
        "item_order": 0,
        "item_type": "LESSON",
        "item_title": "LE one",
    }

    # items_json = json.dumps(items, indent = 4)
    items_json = jsonable_encoder(items)
    response = client.put(
        f"/api/v1/courses/{test_course.id}",
        # json={"items": items_json},
        json={"items": [items_json]},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    # assert response.json()["items"][0] == items_json
