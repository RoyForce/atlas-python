from app.db.programs.models import Program


def test_get_programs(client, test_program, superuser_token_headers):
    program = test_program.dict()
    response = client.get("/api/v1/programs", headers=superuser_token_headers)
    assert response.status_code == 200
    assert all(response.json()[0][arg] == program[arg] for arg in program)


def test_delete_program(
    client, test_program, test_db, superuser_token_headers
):
    response = client.delete(
        f"/api/v1/programs/{test_program.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(Program).all() == []


def test_get_program(
    client,
    test_program,
    superuser_token_headers,
):
    response = client.get(
        f"/api/v1/programs/{test_program.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    program = test_program.dict()
    assert all(response.json()[arg] == program[arg] for arg in program)


def test_edit_program(
    client, test_program, test_portfolio, test_team, superuser_token_headers
):
    update_program = {
        "id": test_program.id,
        "name": "test program name",
        "description": "test program description",
        "portfolio_id": test_portfolio.id,
        "team_id": test_team.id,
    }

    response = client.put(
        f"/api/v1/programs/{test_program.id}",
        json=update_program,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert all(
        response.json()[arg] == update_program[arg] for arg in update_program
    )
