from app.db.roles.models import Role


def test_get_roles(client, test_role, superuser_token_headers):
    response = client.get("/api/v1/roles", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_role.id,
            "name": test_role.name,
            "description": test_role.description,
        }
    ]


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
    assert response.json() == {
        "id": test_role.id,
        "name": test_role.name,
        "description": test_role.description,
    }
