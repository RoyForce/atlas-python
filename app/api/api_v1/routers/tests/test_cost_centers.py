from app.db.cost_centers.models import CostCenter


def test_get_cost_centers(client, test_cost_center, superuser_token_headers):
    cost_center = test_cost_center.dict()
    response = client.get(
        "/api/v1/cost_centers", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert all(
        response.json()[0][arg] == cost_center[arg] for arg in cost_center
    )


def test_delete_cost_center(
    client, test_cost_center, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/cost_centers/{test_cost_center.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(CostCenter).all() == []


def test_get_cost_center(
    client,
    test_cost_center,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/cost_centers/{test_cost_center.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    cost_center = test_cost_center.dict()
    assert all(response.json()[arg] == cost_center[arg] for arg in cost_center)


def test_edit_cost_center(client, test_cost_center, superuser_token_headers):
    update_cost_center = {
        "id": test_cost_center.id,
        "name": "test cost_center name",
        "hr_rate": 1,
    }

    response = client.put(
        f"/api/v1/cost_centers/{test_cost_center.id}",
        json=update_cost_center,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_cost_center[arg]
        for arg in update_cost_center
    )
