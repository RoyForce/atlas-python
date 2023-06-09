from app.db.agilityPlans.models import AgilityPlan


def test_get_agilityPlans(client, test_agilityPlan, superuser_token_headers):
    agilityPlan = test_agilityPlan.dict()
    response = client.get(
        "/api/v1/agilityPlans", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert all(
        response.json()[0][arg] == agilityPlan[arg]
        for arg in agilityPlan
        if arg != "page_content"
    )


def test_delete_agilityPlan(
    client, test_agilityPlan, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/agilityPlans/{test_agilityPlan.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(AgilityPlan).all() == []


def test_get_agilityPlan(
    client,
    test_agilityPlan,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/agilityPlans/{test_agilityPlan.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    agilityPlan = test_agilityPlan.dict()
    assert all(response.json()[arg] == agilityPlan[arg] for arg in agilityPlan)


def test_edit_agilityPlan(client, test_agilityPlan, superuser_token_headers):
    update_agilityPlan = {
        "id": test_agilityPlan.id,
        "name": "test name",
        "description": "test desc",
        "agilityPlan_type": "COURSE",
    }

    response = client.put(
        f"/api/v1/agilityPlans/{test_agilityPlan.id}",
        json=update_agilityPlan,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_agilityPlan[arg]
        for arg in update_agilityPlan
    )
