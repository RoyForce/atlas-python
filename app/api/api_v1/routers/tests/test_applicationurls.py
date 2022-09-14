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
