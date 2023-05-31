from app.db.teams.models import Team


def test_get_teams(client, test_team, superuser_token_headers):
    team = test_team.dict()
    response = client.get("/api/v1/teams", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == team[arg] for arg in team)


def test_delete_team(client, test_team, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/teams/{test_team.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json()["id"] == test_team.id
    assert response.json()["is_deleted"] == True


def test_get_team(
    client,
    test_team,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/teams/{test_team.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    team = test_team.dict()
    assert all(response.json()[arg] == team[arg] for arg in team)


def test_edit_team(client, test_team, test_program, superuser_token_headers):
    update_team = {
        "id": test_team.id,
        "name": "test team name",
        "program_id": test_program.id,
        "type": 1,
    }

    response = client.put(
        f"/api/v1/teams/{test_team.id}",
        json=update_team,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(response.json()[arg] == update_team[arg] for arg in update_team)
