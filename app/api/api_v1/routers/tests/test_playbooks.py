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


def test_playbooks_list_route_work_with_sort_param(
    client, test_db, superuser_token_headers
):
    # Delete all playbooks
    test_db.query(Playbook).delete()
    test_db.commit()

    # Create 4 playbooks
    for i in range(1, 5):
        response = client.post(
            "/api/v1/playbooks",
            json={"name": "New playbook" + str(i), "description": "test"},
            headers=superuser_token_headers,
        )
        assert response.status_code == 200

    # Sort by name desc
    response = client.get(
        "/api/v1/playbooks?_order=desc&_sort=name",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # Check if the playbooks are sorted by name desc
    assert all(
        response.json()[i]["name"] > response.json()[i + 1]["name"]
        for i in range(3)
    )

    # Sort by name asc
    response = client.get(
        "/api/v1/playbooks?_order=asc&_sort=name",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # Check if the playbooks are sorted by name asc
    assert all(
        response.json()[i]["name"] < response.json()[i + 1]["name"]
        for i in range(3)
    )
