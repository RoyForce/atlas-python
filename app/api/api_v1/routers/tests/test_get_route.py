def test_sorting(client, test_course, superuser_token_headers):
    # sort by relationship
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=application_url&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by relationship with dot notation
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=application_url.name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by attribute
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by invalid attribute
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=invalid_name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by invalid relationship attribute
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=application_url.invalid_name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by invalid relationship
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=invalid_name.name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by invalid relationship and attribute
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=invalid_name.invalid_name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200

    # sort by multiple dot notation
    response = client.get(
        "/api/v1/jobs?_order=asc&_sort=application_url.name.invalid_name&",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
