from app.db.jobs.schemas import ExtensionMode

ext_jobs_route = "/api/ext/jobs"
ext_job_snippets_route = "/api/ext/job-snippets"


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

    end_point = f"{ext_jobs_route}/{test_job.id}"
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
