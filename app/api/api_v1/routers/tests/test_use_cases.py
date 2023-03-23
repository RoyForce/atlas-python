from app.db.use_cases.models import UseCase


def test_get_use_cases(client, test_use_case, superuser_token_headers):
    use_case = test_use_case.dict()
    response = client.get("/api/v1/use-cases", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == use_case[arg] for arg in use_case)


def test_delete_use_case(
    client, test_use_case, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/use-cases/{test_use_case.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(UseCase).all() == []


def test_edit_use_case(
    client, test_use_case, test_role, test_job, superuser_token_headers
):
    new_use_case = {
        "name": "New use_cases",
        "description": "New desc",
        "table_config": "test conf",
    }

    response = client.put(
        f"/api/v1/use-cases/{test_use_case.id}",
        json=new_use_case,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == new_use_case[arg] for arg in new_use_case
    )

    # Edit use_case with roles
    role = test_role.dict()
    job = test_job.dict()
    response = client.put(
        f"/api/v1/use-cases/{test_use_case.id}",
        json={"role_ids": [role["id"]], "job_ids": [job["id"]]},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["role_ids"] == [role["id"]]
    assert response.json()["job_ids"] == [job["id"]]


def test_create_use_case_with_role_job_and_delete_mapping(
    client, test_role, test_job, superuser_token_headers
):
    role = test_role.dict()
    job = test_job.dict()
    use_case = {
        "name": "New use_case",
        "description": "New desc",
        "table_config": "testConf",
        "role_ids": [role["id"]],
        "job_ids": [job["id"]],
    }
    response = client.post(
        "/api/v1/use-cases", json=use_case, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["role_ids"][0] == role["id"]
    assert response.json()["job_ids"][0] == job["id"]

    response = client.delete(
        f"/api/v1/jobs/{test_job.id}", headers=superuser_token_headers
    )
    response = client.get(
        f"/api/v1/use-cases", headers=superuser_token_headers
    )
    assert response.json()[0]["job_ids"] == []

    response = client.delete(
        f"/api/v1/roles/{test_role.id}", headers=superuser_token_headers
    )
    response = client.get(
        f"/api/v1/use-cases", headers=superuser_token_headers
    )
    assert response.json()[0]["role_ids"] == []
