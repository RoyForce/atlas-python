from app.db.dimensions.models import Dimension


def test_dimension_crud(
    client, test_assessment, test_db, superuser_token_headers
):
    # Test create dimension object
    dimension = {
        "name": "TestDimension",
        "description": "desc",
        "assessment_id": test_assessment.id,
        "baseline_value": 1,
        "ideal_value": 1,
    }
    response = client.post(
        "/api/v1/dimensions",
        json=dimension,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == dimension[arg] for arg in dimension)

    # Test get all dimension object
    response = client.get(
        "/api/v1/dimensions", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == dimension["name"]

    # Edit dimension object
    dimension_id = response.json()[0]["id"]
    edit_dimension = {
        "name": "Updated Dimension",
        "description": "Updated Dimension",
        "assessment_id": test_assessment.id,
        "baseline_value": 2,
        "ideal_value": 3,
    }
    response = client.put(
        f"/api/v1/dimensions/{dimension_id}",
        json=edit_dimension,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(
        response.json()[arg] == edit_dimension[arg] for arg in edit_dimension
    )

    # Delete dimension object
    response = client.delete(
        f"/api/v1/dimensions/{dimension_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Dimension).all() == []
