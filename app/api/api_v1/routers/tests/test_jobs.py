from asyncio import constants
from app.db.jobs.models import Job


def test_get_jobs(client, test_job, superuser_token_headers):
    response = client.get("/api/v1/jobs", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_job.id,
            "name": test_job.name,
            "description": test_job.description,
            "application_url": test_job.application_url.as_json(),
            "roles": test_job.roles,
        }
    ]


def test_delete_job(client, test_job, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/jobs/{test_job.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Job).all() == []


def test_edit_job(
    client, test_job, test_role, test_applicationurl, superuser_token_headers
):
    new_job = {
        "name": "New jobs",
        "description": "New desc",
        "application_url_id": test_applicationurl.id,
    }

    response = client.put(
        f"/api/v1/jobs/{test_job.id}",
        json=new_job,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["name"] == new_job["name"]
    assert response.json()["description"] == new_job["description"]

    # Edit job with roles
    role = test_role.as_json()
    response = client.put(
        f"/api/v1/jobs/{test_job.id}",
        json={"role_ids": [role["id"]]},
        headers=superuser_token_headers,
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json()["roles"][0] == role


# ------------------test job role mapping-----------------------


def test_create_job_with_role(
    client, test_role, test_applicationurl, superuser_token_headers
):
    role = test_role.as_json()
    job = {
        "name": "New jobs",
        "description": "New desc",
        "application_url_id": test_applicationurl.id,
        "role_ids": [role["id"]],
    }
    response = client.post(
        "/api/v1/jobs", json=job, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["roles"][0] == role
