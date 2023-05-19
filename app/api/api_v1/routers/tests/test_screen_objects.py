from app.db.screen_objects.models import ScreenObject


def test_screen_object_crud(
    client, test_screen, test_db, superuser_token_headers
):
    # Test create screen object
    screen_object = {
        "name": "Screen Object",
        "description": "desc",
        "screen_id": test_screen.id,
        "properties": {"selector": "body"},
    }
    response = client.post(
        "/api/v1/screen-objects",
        json=screen_object,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == screen_object[arg] for arg in screen_object
    )

    # Test get all screen object
    response = client.get(
        "/api/v1/screen-objects", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == screen_object["name"]

    # Edit screen object
    screen_object_id = response.json()[0]["id"]
    edit_screen_object = {
        "name": "New Screen Object",
        "description": "New desc",
    }
    response = client.put(
        f"/api/v1/screen-objects/{screen_object_id}",
        json=edit_screen_object,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(
        response.json()[arg] == edit_screen_object[arg]
        for arg in edit_screen_object
    )

    # Test screen has objects property
    response = client.get(
        f"/api/v1/screens/{test_screen.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert len(response.json()["objects"]) == 1

    # Delete screen object
    response = client.delete(
        f"/api/v1/screen-objects/{screen_object_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(ScreenObject).all() == []
