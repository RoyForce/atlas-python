from app.db.objectives.models import Objective


def test_objective_crud(client, test_db, superuser_token_headers):
    # Test create objective object
    objective = {
        "name": "Objective 1",
        "description": "desc",
        "start_value": 1,
        "target_value": 2,
        "metrics_type": "UNITS",
    }
    response = client.post(
        "/api/v1/objectives",
        json=objective,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == objective[arg] for arg in objective)

    # Test get all objective object
    response = client.get(
        "/api/v1/objectives", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == objective["name"]

    # Edit objective object
    objective_id = response.json()[0]["id"]
    edit_objective = {
        "name": "Updated Objective",
        "description": "Updated Objective",
        "start_value": 1,
        "target_value": 2,
        "metrics_type": "UNITS",
    }
    response = client.put(
        f"/api/v1/objectives/{objective_id}",
        json=edit_objective,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(
        response.json()[arg] == edit_objective[arg] for arg in edit_objective
    )

    # Delete objective object
    response = client.delete(
        f"/api/v1/objectives/{objective_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Objective).all() == []
