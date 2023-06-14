from app.db.jobs.models import Job


def test_get_jobs(client, test_job, superuser_token_headers):
    job = test_job.dict()
    response = client.get("/api/v1/jobs", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == job[arg] for arg in job)


"""
Enable this test when the query string is implemented
"""
# def test_get_jobs_with_query_string(
#     client, test_db, test_application_url, superuser_token_headers
# ):
#     for i in range(10):
#         job = Job(
#             name=f"testName{i}",
#             description=f"testDesc{i}",
#             application_url_id=test_application_url.id,
#         )
#         test_db.add(job)
#         test_db.commit()
#     response = client.get(
#         "/api/v1/jobs?_end=10&_start=5&", headers=superuser_token_headers
#     )
#     assert response.status_code == 200
#     assert len(response.json()) == 5
#     assert all(
#         response.json()[i]["name"] == f"testName{i+5}" for i in range(5)
#     )


def test_delete_job(client, test_job, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/jobs/{test_job.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Job).all() == []


def test_edit_job(
    client, test_job, test_role, test_application_url, superuser_token_headers
):
    new_job = {
        "name": "New jobs",
        "description": "New desc",
        "application_url_id": test_application_url.id,
        "is_template": False,
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
    role = test_role.dict()
    response = client.put(
        f"/api/v1/jobs/{test_job.id}",
        json={"role_ids": [role["id"]]},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["roles"][0]["id"] == role["id"]


def test_create_job_with_role(
    client, test_role, test_application_url, superuser_token_headers
):
    role = test_role.dict()
    job = {
        "name": "New jobs",
        "description": "New desc",
        "application_url_id": test_application_url.id,
        "role_ids": [role["id"]],
        "is_template": False,
    }
    response = client.post(
        "/api/v1/jobs", json=job, headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["roles"][0]["id"] == role["id"]


def test_edit_job_can_accept_json_steps_value(
    client, test_job, superuser_token_headers
):
    payload = {
        "steps": {
            "steps": [],
            "defaultAdvancedSetting": {
                "waitForObject": 1.5,
                "intervalBetweenAttempts": 1.5,
                "numberOfAttempts": 1,
                "overlayIntensity": 10,
            },
        },
    }

    response = client.put(
        f"/api/v1/jobs/{test_job.id}",
        json=payload,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["steps"] == payload["steps"]


def test_update_screen_ids_and_use_case_ids_from_job(
    client,
    test_job,
    test_screen,
    test_use_case,
    superuser_token_headers,
):
    new_job = {
        "screen_ids": [test_screen.id],
        "use_case_ids": [test_use_case.id],
    }
    response = client.put(
        f"/api/v1/jobs/{test_job.id}",
        json=new_job,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert response.json()["id"] == test_job.id
    assert response.json()["screen_ids"] == new_job["screen_ids"]
    assert response.json()["use_case_ids"] == new_job["use_case_ids"]

    response = client.delete(
        f"/api/v1/jobs/{test_job.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200

    response = client.get(
        f"/api/v1/use-cases/{test_use_case.id}",
        headers=superuser_token_headers,
    )
    use_case = response.json()
    assert not test_job.id in use_case["job_ids"]

    response = client.get(
        f"/api/v1/screens/{test_screen.id}", headers=superuser_token_headers
    )
    screen = response.json()
    assert not test_job.id in screen["job_ids"]
