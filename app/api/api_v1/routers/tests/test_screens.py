from app.db.screens.models import Screen


def test_get_screens(client, test_screen, superuser_token_headers):
    screen = test_screen.dict()
    response = client.get("/api/v1/screens", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == screen[arg] for arg in screen)


def test_delete_screen(client, test_screen, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/screens/{test_screen.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Screen).all() == []


def test_edit_screen(client, test_screen, test_job, superuser_token_headers):
    new_screen = {
        "name": "New Screen",
        "description": "New desc",
    }

    response = client.put(
        f"/api/v1/screens/{test_screen.id}",
        json=new_screen,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == new_screen[arg] for arg in new_screen)

    # Edit screen with jobs
    job = test_job.dict()
    response = client.put(
        f"/api/v1/screens/{test_screen.id}",
        json={"job_ids": [job["id"]]},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["job_ids"] == [job["id"]]


def test_create_screen_with_job_and_delete_mapping(
    client, test_job, superuser_token_headers
):
    job = test_job.dict()
    screen = {
        "name": "New Screen",
        "description": "New desc",
        "job_ids": [job["id"]],
    }
    response = client.post(
        "/api/v1/screens", json=screen, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["job_ids"][0] == job["id"]
