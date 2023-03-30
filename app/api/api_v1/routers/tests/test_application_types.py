def test_get_application_url_types(
    client, test_application_type, superuser_token_headers
):
    response = client.get(
        "/api/v1/application-types", headers=superuser_token_headers
    )
    assert response.status_code == 200
    app_type = response.json()[0]
    assert app_type["id"] == test_application_type.id
    assert app_type["name"] == test_application_type.name
    assert app_type["description"] == test_application_type.description


def test_get_application_url_type(
    client,
    test_application_type,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/application-types/{test_application_type.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_application_type.id
    assert response.json()["name"] == test_application_type.name
    assert response.json()["description"] == test_application_type.description
