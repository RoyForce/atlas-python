from asyncio import constants
from app.db.jobs.models import Job
from app.db.users.models import User
from app.db.jobs.schemas import ExtensionMode


def test_get_jobs(client, test_job, superuser_token_headers):
    job = test_job.dict()
    response = client.get("/api/v1/jobs", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == job[arg] for arg in job)


def test_get_jobs_with_query_string(
    client, test_db, test_application_url, superuser_token_headers
):
    for i in range(10):
        job = Job(
            name=f"testName{i}",
            description=f"testDesc{i}",
            application_url_id=test_application_url.id,
        )
        test_db.add(job)
        test_db.commit()
    response = client.get(
        "/api/v1/jobs?_end=10&_start=5&", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert all(
        response.json()[i]["name"] == f"testName{i+5}" for i in range(5)
    )


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


def test_if_user_can_access_job(
    client, test_job, test_user, test_db, extension_token_headers
):
    """_summary_ : Test if user can access job
    1. Disallow user without extension token
    2. Allow user with extension token
    3. Allow user with extension token and extension mode is set to executor
    4. Disallow user with extension token and extension mode is set to designer
    5. Allow user with extension token and extension mode is set to designer and user is designer
    6. Disallow user if job is locked by another designer

    """

    end_point = f"/api/v1/jobs/steps/{test_job.id}"
    payload = {
        "user_id": test_user.id,
        "mode": ExtensionMode.EXECUTOR,
    }
    response = client.get(end_point, params=payload)
    assert response.status_code == 403

    response = client.get(
        end_point,
        params=payload,
        headers=extension_token_headers,
    )
    assert response.status_code == 200

    payload["mode"] = ExtensionMode.DESIGNER
    response = client.get(
        end_point,
        params=payload,
        headers=extension_token_headers,
    )
    assert response.status_code == 403

    test_user.is_designer = True
    test_db.commit()
    response = client.get(
        end_point,
        params=payload,
        headers=extension_token_headers,
    )
    assert response.status_code == 200

    test_job.is_locked = True
    test_db.commit()
    response = client.get(
        end_point,
        params=payload,
        headers=extension_token_headers,
    )
    assert response.status_code == 403


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
