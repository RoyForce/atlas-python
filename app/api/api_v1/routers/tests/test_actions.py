from app.db.actions.models import Action


def test_get_actions(client, test_action, superuser_token_headers):
    action = test_action.dict()
    response = client.get("/api/v1/actions", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(
        response.json()[0][arg] == action[arg]
        for arg in action
        if arg != "page_content"
    )


def test_delete_action(client, test_action, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/actions/{test_action.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Action).all() == []


def test_get_action(
    client,
    test_action,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/actions/{test_action.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    action = test_action.dict()
    assert all(response.json()[arg] == action[arg] for arg in action)


def test_edit_action(client, test_action, superuser_token_headers):
    update_action = {
        "id": test_action.id,
        "name": "test name",
        "description": "test desc",
        "action_type": "COURSE",
    }

    response = client.put(
        f"/api/v1/actions/{test_action.id}",
        json=update_action,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_action[arg] for arg in update_action
    )
