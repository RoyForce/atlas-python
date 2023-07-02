from app.db.external_data import engine
from app.db.enums import ResourceType
from app.db.users import models as userModels
from app.db.roles import models as roleModels
from app.db.teams import models as teamModel
from app.db.portfolios import models as PortfolioModel
from app.db.programs import models as ProgramModel


def test_fetch_external_data(
    client, test_db, superuser_token_headers, test_user
):
    user_data = [
        {
            "id": 1,
            "firstName": "UserFname",
            "lastName": "UserLastname",
            "email": "usertestemail@gmail.com",
            "status": "Active",
            "roleId": 1,
            "costCenterId": 1,
            "lastUpdatedDate": "2022-04-09T18:49:48Z",
            "teams": [],
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, user_data, ResourceType.USER.value
    )

    user = (
        test_db.query(userModels.User)
        .filter(userModels.User.email == user_data[0]["email"])
        .first()
    )
    assert user_data[0]["email"] == user.email

    user_data = [
        {
            "id": 1,
            "firstName": "UpdatedFname",
            "lastName": "UserLastname",
            "email": "usertestemail@gmail.com",
            "status": "Active",
            "lastUpdatedDate": "2022-04-10T18:49:48Z",
            "roleId": 1,
            "costCenterId": 1,
            "teams": [],
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, user_data, ResourceType.USER.value
    )

    user = (
        test_db.query(userModels.User)
        .filter(userModels.User.email == user_data[0]["email"])
        .first()
    )

    assert user_data[0]["firstName"] == user.first_name

    role_data = [
        {
            "id": 1,
            "name": "Team Member",
            "description": "role desc",
            "createDate": "2022-04-09T18:49:48Z",
            "updateDate": "2022-04-09T18:49:48Z",
        },
        {
            "id": 2,
            "name": "Team Leads",
            "description": "test",
            "createDate": "2022-04-09T18:49:48Z",
            "updateDate": "2022-04-09T18:49:48Z",
        },
    ]
    response_role = engine.create_update_external_data(
        test_db, role_data, ResourceType.ROLE.value
    )
    role = (
        test_db.query(roleModels.Role)
        .filter(roleModels.Role.source_id == role_data[0]["id"])
        .first()
    )

    assert role_data[0]["name"] == role.name

    role_data = [
        {
            "id": 1,
            "name": "Updated Team Member",
            "description": "role desc",
            "createDate": "2022-04-09T18:49:48Z",
            "updateDate": "2022-05-09T18:49:48Z",
        },
        {
            "id": 2,
            "name": "updated Team Leads",
            "description": "test",
            "createDate": "2022-04-09T18:49:48Z",
            "updateDate": "2022-05-09T18:49:48Z",
        },
    ]
    response_role = engine.create_update_external_data(
        test_db, role_data, ResourceType.ROLE.value
    )
    role = (
        test_db.query(roleModels.Role)
        .filter(roleModels.Role.source_id == role_data[0]["id"])
        .first()
    )
    assert role_data[0]["name"] == role.name


def test_teams_external_data(
    client, test_db, superuser_token_headers, test_user
):
    team_data = [
        {
            "id": 1,
            "name": "Team1",
            "description": "Jira align team desc",
            "programId": None,
            "type": 1,
            "sprintPrefix": "JA-TOT",
            "shortName": "TOT-team1",
            "isActive": True,
            "isKanbanTeam": False,
            "lastUpdatedDate": "2022-01-09T18:49:48Z",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, team_data, ResourceType.TEAM.value
    )

    team = (
        test_db.query(teamModel.Team)
        .filter(teamModel.Team.source_id == team_data[0]["id"])
        .first()
    )

    assert team_data[0]["id"] == team.source_id
    assert team_data[0]["name"] == team.name

    team_data = [
        {
            "id": 1,
            "name": "updatedTeamName",
            "description": "Jira align team desc",
            "programId": None,
            "type": 1,
            "sprintPrefix": "JA-PORT",
            "shortName": "TOT-team2",
            # "isActive": True,
            "isKanbanTeam": True,
            "lastUpdatedDate": "2022-05-09T18:49:48Z",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, team_data, ResourceType.TEAM.value
    )

    team = (
        test_db.query(teamModel.Team)
        .filter(teamModel.Team.source_id == team_data[0]["id"])
        .first()
    )

    assert team_data[0]["name"] == team.name


def test_portfolios_external_data(
    client, test_db, superuser_token_headers, test_user
):
    portfolio_data = [
        {
            "id": 1,
            "title": "Portfolio",
            "description": "Jira align Portfolio desc",
            "teamId": 1,
            "isActive": 1,
            "lastUpdatedDate": "2022-05-09T18:49:48Z",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, portfolio_data, ResourceType.PORTFOLIO.value
    )

    portfolio = (
        test_db.query(PortfolioModel.Portfolio)
        .filter(PortfolioModel.Portfolio.source_id == portfolio_data[0]["id"])
        .first()
    )
    assert portfolio_data[0]["id"] == portfolio.source_id
    assert portfolio_data[0]["title"] == portfolio.name

    portfolio_data = [
        {
            "id": 1,
            "title": "Updated Portfolio",
            "description": "Jira align Portfolio desc updated",
            "teamId": 1,
            "isActive": 1,
            "lastUpdatedDate": "2022-05-19T18:49:48Z",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, portfolio_data, ResourceType.PORTFOLIO.value
    )

    portfolio = (
        test_db.query(PortfolioModel.Portfolio)
        .filter(PortfolioModel.Portfolio.source_id == portfolio_data[0]["id"])
        .first()
    )
    assert portfolio_data[0]["title"] == portfolio.name


def test_programs_external_data(
    client,
    test_db,
    test_team,
    test_portfolio,
    superuser_token_headers,
    test_user,
):
    program_data = [
        {
            "id": 1,
            "title": "Program",
            "teamDescription": "Program desc",
            "portfolioId": test_portfolio.id,
            "teamId": test_team.id,
            "lastUpdatedDate": "2022-05-19T18:49:48Z",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, program_data, ResourceType.PROGRAM.value
    )

    program = (
        test_db.query(ProgramModel.Program)
        .filter(ProgramModel.Program.source_id == program_data[0]["id"])
        .first()
    )
    assert program_data[0]["id"] == program.source_id
    assert program_data[0]["title"] == program.name

    program_data = [
        {
            "id": 1,
            "title": "Updated Program",
            "teamDescription": "Program desc",
            "portfolioId": test_portfolio.id,
            "teamId": test_team.id,
            "lastUpdatedDate": "2022-06-19T18:49:48Z",
        }
    ]
    response1 = engine.create_update_external_data(
        test_db, program_data, ResourceType.PROGRAM.value
    )

    program = (
        test_db.query(ProgramModel.Program)
        .filter(ProgramModel.Program.source_id == program_data[0]["id"])
        .first()
    )
    assert program_data[0]["title"] == program.name
