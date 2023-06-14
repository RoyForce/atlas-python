from app.db.job_snippets.models import JobSnippet

job_snippet_route = "/api/v1/job-snippets"


def test_job_snippet_crud(client, test_db, superuser_token_headers):
    # Test create job snippet
    job_snippet = {
        "name": "Job Snippet 1",
        "description": "desc",
        "steps": {"selector": "body"},
    }
    response = client.post(
        job_snippet_route,
        json=job_snippet,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == job_snippet[arg] for arg in job_snippet)

    # Test get all job snippets
    response = client.get(job_snippet_route, headers=superuser_token_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == job_snippet["name"]

    # Edit job snippet
    job_snippet_id = response.json()[0]["id"]
    edit_job_snippet = {
        "name": "New Job Snippet",
        "description": "New desc",
    }
    response = client.put(
        f"{job_snippet_route}/{job_snippet_id}",
        json=edit_job_snippet,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(
        response.json()[arg] == edit_job_snippet[arg]
        for arg in edit_job_snippet
    )

    # Delete job snippet
    response = client.delete(
        f"{job_snippet_route}/{job_snippet_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(JobSnippet).all() == []
