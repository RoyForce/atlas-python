from app.db.lessons.models import Lesson


def test_get_lessons(client, test_lesson, superuser_token_headers):
    lesson = test_lesson.dict()
    response = client.get("/api/v1/lessons", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == lesson[arg] for arg in lesson)


def test_delete_lesson(client, test_lesson, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/lessons/{test_lesson.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Lesson).all() == []


def test_get_lesson(
    client,
    test_lesson,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/lessons/{test_lesson.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    lesson = test_lesson.dict()
    assert all(response.json()[arg] == lesson[arg] for arg in lesson)


def test_edit_lesson(client, test_lesson, superuser_token_headers):
    update_lesson = {
        "id": test_lesson.id,
        "name": "test name",
        "description": "test desc",
        "duration": 1,
        "page_content": "page_content",
    }

    response = client.put(
        f"/api/v1/lessons/{test_lesson.id}",
        json=update_lesson,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_lesson[arg] for arg in update_lesson
    )
