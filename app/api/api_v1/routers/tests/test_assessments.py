from app.db.assessments.models import Assessment


def test_assessment_crud(client, test_db, superuser_token_headers):
    # Test create assessment object
    assessment = {"name": "Assessment 1", "description": "desc"}
    response = client.post(
        "/api/v1/assessments",
        json=assessment,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == assessment[arg] for arg in assessment)

    # Test get all assessment object
    response = client.get(
        "/api/v1/assessments", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == assessment["name"]

    # Edit assessment object
    assessment_id = response.json()[0]["id"]
    edit_assessment = {
        "name": "Updated Assessment",
        "description": "Updated Assessment",
    }
    response = client.put(
        f"/api/v1/assessments/{assessment_id}",
        json=edit_assessment,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(
        response.json()[arg] == edit_assessment[arg] for arg in edit_assessment
    )

    # Delete assessment object
    response = client.delete(
        f"/api/v1/assessments/{assessment_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Assessment).all() == []
