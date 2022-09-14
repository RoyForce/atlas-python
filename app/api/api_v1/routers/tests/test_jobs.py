from app.db.jobs.models import Jobs


def test_get_jobs(client, test_job, superuser_token_headers):
    response = client.get("/api/v1/jobs", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": test_job.id,
            "name": test_job.name,
            "description": test_job.description,
            "application_url_id": test_job.application_url_id,
        }
    ]


def test_delete_job(client, test_job, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/jobs/{test_job.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Jobs).all() == []


def test_edit_job(client, test_job, superuser_token_headers):
    new_job = {
        "name": "New jobs",
        "description": "New desc",
        "application_url_id": 1,
    }

    response = client.put(
        f"/api/v1/jobs/{test_job.id}",
        json=new_job,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_job["id"] = test_job.id
    assert response.json() == new_job
