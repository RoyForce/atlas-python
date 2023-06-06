from app.db.results.models import Result


def test_result_crud(client, test_objective, test_db, superuser_token_headers):
    # Test create result object
    result = {"value": 1, "objective_id": test_objective.id}
    response = client.post(
        "/api/v1/results",
        json=result,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == result[arg] for arg in result)

    # Edit result
    result_id = response.json()["id"]
    edit_result = {"value": 5, "objective_id": test_objective.id}
    response = client.put(
        f"/api/v1/results/{result_id}",
        json=edit_result,
        headers=superuser_token_headers,
    )

    assert response.status_code == 200
    assert all(response.json()[arg] == edit_result[arg] for arg in edit_result)

    # Delete result
    response = client.delete(
        f"/api/v1/results/{result_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(Result).all() == []
