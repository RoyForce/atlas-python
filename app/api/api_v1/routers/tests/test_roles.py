from app.db.roles.models import Role


def test_get_roles(client, test_role, superuser_token_headers):
    response = client.get("/api/v1/roles", headers=superuser_token_headers)
    assert response.status_code == 200
    role = test_role.dict()
    assert all(response.json()[0][arg] == role[arg] for arg in role)


def test_create_role(client, superuser_token_headers):
    new_role = {"name": "Manager"}
    response = client.post(
        f"/api/v1/roles",
        json=new_role,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == new_role["name"]


def test_delete_role(client, test_role, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/roles/{test_role.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Role).all() == []


def test_edit_role(client, test_role, superuser_token_headers):
    new_role = {"name": "Manager"}
    response = client.put(
        f"/api/v1/roles/{test_role.id}",
        json=new_role,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_role.id
    assert response.json()["name"] == new_role["name"]


def test_get_role(
    client,
    test_role,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/roles/{test_role.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_role.id
    assert response.json()["name"] == test_role.name


def test_update_job_ids_playbook_ids_and_use_case_ids_from_role(
    client,
    test_role,
    test_job,
    test_playbook,
    test_use_case,
    superuser_token_headers,
):
    new_role = {
        "job_ids": [test_job.id],
        "playbook_ids": [test_playbook.id],
        "use_case_ids": [test_use_case.id],
    }
    response = client.put(
        f"/api/v1/roles/{test_role.id}",
        json=new_role,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == test_role.id
    assert response.json()["job_ids"] == new_role["job_ids"]
    assert response.json()["playbook_ids"] == new_role["playbook_ids"]
    assert response.json()["use_case_ids"] == new_role["use_case_ids"]
