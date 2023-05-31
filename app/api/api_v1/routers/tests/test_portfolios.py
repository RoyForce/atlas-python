from app.db.portfolios.models import Portfolio


def test_get_portfolios(client, test_portfolio, superuser_token_headers):
    portfolio = test_portfolio.dict()
    response = client.get(
        "/api/v1/portfolios", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert all(response.json()[0][arg] == portfolio[arg] for arg in portfolio)


def test_delete_portfolio(
    client, test_portfolio, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/portfolios/{test_portfolio.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_portfolio.id
    assert response.json()["is_deleted"] == True


def test_get_portfolio(
    client,
    test_portfolio,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/portfolios/{test_portfolio.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    portfolio = test_portfolio.dict()
    assert all(response.json()[arg] == portfolio[arg] for arg in portfolio)


def test_edit_portfolio(
    client, test_portfolio, test_team, superuser_token_headers
):
    update_portfolio = {
        "id": test_portfolio.id,
        "name": "test name",
        "description": "test desc",
        "team_id": test_team.id,
    }

    response = client.put(
        f"/api/v1/portfolios/{test_portfolio.id}",
        json=update_portfolio,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_portfolio[arg]
        for arg in update_portfolio
    )
