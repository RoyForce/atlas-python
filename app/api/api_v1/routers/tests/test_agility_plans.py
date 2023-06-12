from app.db.agility_plans.models import AgilityPlan


def test_get_agility_plans(client, test_agility_plan, superuser_token_headers):
    agility_plan = test_agility_plan.dict()
    response = client.get(
        "/api/v1/agility-plans", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert all(
        response.json()[0][arg] == agility_plan[arg]
        for arg in agility_plan
        if arg != "page_content"
    )


def test_delete_agility_plan(
    client, test_agility_plan, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/agility-plans/{test_agility_plan.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert test_db.query(AgilityPlan).all() == []


def test_get_agility_plan(
    client,
    test_agility_plan,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/agility-plans/{test_agility_plan.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    agility_plan = test_agility_plan.dict()
    assert all(
        response.json()[arg] == agility_plan[arg] for arg in agility_plan
    )


def test_edit_agility_plan(client, test_agility_plan, superuser_token_headers):
    update_agility_plan = {
        "id": test_agility_plan.id,
        "name": "test name",
        "description": "test desc",
        "agility_plan_type": "COURSE",
    }

    response = client.put(
        f"/api/v1/agility-plans/{test_agility_plan.id}",
        json=update_agility_plan,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_agility_plan[arg]
        for arg in update_agility_plan
    )
