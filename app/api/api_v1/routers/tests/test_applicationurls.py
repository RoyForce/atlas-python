from app.db.applicationurls.models import ApplicationUrl


def test_get_applicationurls(
    client, test_applicationurl, superuser_token_headers
):
    response = client.get(
        "/api/v1/application-urls", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_applicationurl.id,
            "name": test_applicationurl.name,
            "url": test_applicationurl.url,
        }
    ]


def test_delete_applicationurl(
    client, test_applicationurl, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/application-urls/{test_applicationurl.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(ApplicationUrl).all() == []


def test_delete_applicationurl_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/application-urls/4321", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_applicationurl(
    client, test_applicationurl, superuser_token_headers
):
    new_applicationurl = {"name": "View Buton", "url": "viewbutton.com"}

    response = client.put(
        f"/api/v1/application-urls/{test_applicationurl.id}",
        json=new_applicationurl,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_applicationurl["id"] = test_applicationurl.id
    assert response.json() == new_applicationurl


def test_edit_applicationurl_not_found(
    client, test_db, superuser_token_headers
):
    new_applicationurl = {"name": "View Buton", "url": "viewbutton.com"}
    response = client.put(
        "/api/v1/application-urls/1234",
        json=new_applicationurl,
        headers=superuser_token_headers,
    )
    assert response.status_code == 404


def test_get_applicationurl(
    client,
    test_applicationurl,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/application-urls/{test_applicationurl.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": test_applicationurl.id,
        "name": test_applicationurl.name,
        "url": test_applicationurl.url,
    }


def test_applicationurl_not_found(client, superuser_token_headers):
    response = client.get(
        "/api/v1/application-urls/123", headers=superuser_token_headers
    )
    assert response.status_code == 404
