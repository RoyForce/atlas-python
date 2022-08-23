from app.db.roles.models import Role


def test_get_roles(client, test_role, superuser_token_headers):
    response = client.get("/api/v1/roles", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_role.id,
            "name": test_role.name,
        }
    ]


def test_delete_user(client, test_role, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/roles/{test_role.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Role).all() == []


def test_delete_user_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/roles/4321", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_user(client, test_role, superuser_token_headers):
    new_role = {"name": "Manager"}

    response = client.put(
        f"/api/v1/roles/{test_role.id}",
        json=new_role,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_role["id"] = test_role.id
    assert response.json() == new_role


def test_edit_role_not_found(client, test_db, superuser_token_headers):
    new_role = {"name": "Manager"}
    response = client.put(
        "/api/v1/roles/1234", json=new_role, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_role(
    client,
    test_role,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/roles/{test_role.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {"id": test_role.id, "name": test_role.name}


def test_role_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/roles/123", headers=superuser_token_headers)
    assert response.status_code == 404
