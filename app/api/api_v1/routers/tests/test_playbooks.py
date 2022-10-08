from app.db.playbooks.models import Playbook


def test_get_playbooks(client, test_playbook, superuser_token_headers):
    playbook = test_playbook.dict()
    response = client.get("/api/v1/playbooks", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == playbook[arg] for arg in playbook)


def test_delete_playbook(
    client, test_playbook, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/playbooks/{test_playbook.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Playbook).all() == []


def test_edit_playbook(
    client, test_playbook, test_role, superuser_token_headers
):
    new_playbook = {
        "name": "New playbooks",
        "description": "New desc",
        "page_content": "test page content",
    }

    response = client.put(
        f"/api/v1/playbooks/{test_playbook.id}",
        json=new_playbook,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == new_playbook[arg] for arg in new_playbook
    )

    # Edit playbook with roles
    role = test_role.dict()
    response = client.put(
        f"/api/v1/playbooks/{test_playbook.id}",
        json={"role_ids": [role["id"]]},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["roles"][0] == role


# ------------------test playbook role mapping-----------------------


def test_create_playbook_with_role(client, test_role, superuser_token_headers):
    role = test_role.dict()
    playbook = {
        "name": "New playbook",
        "description": "New desc",
        "page_content": "New Page content",
        "role_ids": [role["id"]],
    }
    response = client.post(
        "/api/v1/playbooks", json=playbook, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["roles"][0] == role
