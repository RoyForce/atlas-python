from fastapi import HTTPException, status

from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import delete
from sqlalchemy.orm.attributes import flag_modified

from app.db.users import models as UserModel
from app.db.enums import ResourceType
from app.db.roles import models as RoleModel
from app.db.teams import models as TeamModel
from app.db.portfolios import models as PortfolioModel
from app.db.programs import models as ProgramModel
from app.db.releases import models as ReleaseModel
from app.db.sprints import models as SprintModel
from app.db.core import (
    get_item_by_source_id,
)


def create_update_external_data(db: Session, raw_data, type):
    if len(raw_data) > 0:
        if type == ResourceType.USER.value:
            users_ids = process_user_data(db, raw_data)
        if type == ResourceType.ROLE.value:
            role_ids = process_role_data(db, raw_data)
            soft_delete(db, RoleModel.Role, role_ids)
        if type == ResourceType.TEAM.value:
            team_ids = process_teams_data(db, raw_data)
            soft_delete(db, TeamModel.Team, team_ids)
        if type == ResourceType.PORTFOLIO.value:
            portfolio_ids = process_portfolios_data(db, raw_data)
            soft_delete(db, PortfolioModel.Portfolio, portfolio_ids)
        if type == ResourceType.PROGRAM.value:
            program_ids = process_programs_data(db, raw_data)
            soft_delete(db, ProgramModel.Program, program_ids)
        if type == ResourceType.RELEASE.value:
            release_ids = process_releases_data(db, raw_data)
            soft_delete(db, ReleaseModel.Release, release_ids)
        if type == ResourceType.SPRINT.value:
            sprint_ids = process_sprints_data(db, raw_data)
            soft_delete(db, SprintModel.Sprint, sprint_ids)
        if type == ResourceType.TEAMPRO.value:
            process_teams_data_update_program(db, raw_data)
    return True


def process_user_data(db: Session, raw_data):
    user_ids = []
    for user in raw_data:
        status = True if user["status"] == "Active" else False
        del_status = False if user["status"] == "Active" else True
        roleId = None
        if user["roleId"] is not None:
            db_role = get_item_by_source_id(db, RoleModel.Role, user["roleId"])
        roleId = db_role.id if db_role is not None else None
        db_user = get_item_by_source_id(db, UserModel.User, user["id"])
        if db_user is None:
            db_user = UserModel.User(
                first_name=user["firstName"],
                last_name=user["lastName"],
                email=user["email"],
                is_active=status,
                is_deleted=del_status,
                role_id=roleId,
                is_designer=False,
                is_superuser=False,
                source_id=user["id"],
                source_update_at=user["lastUpdatedDate"],
                cost_center_id=user["costCenterId"],
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
        else:
            if user["lastUpdatedDate"] != None:
                db_last_update = formate_date(db_user.source_update_at, "DB")
                source_last_update = formate_date(
                    user["lastUpdatedDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_user.first_name = user["firstName"]
                    db_user.last_name = user["lastName"]
                    db_user.is_active = status
                    db_user.is_deleted = status
                    db_user.source_update_at = user["lastUpdatedDate"]
                    db_user.cost_center_id = user["costCenterId"]
                    db.add(db_user)
                    db.commit()
                    db.refresh(db_user)
        if "teams" in user and len(user) > 0:
            update_user_team_mapping(db, db_user.id, user["teams"])
        user_ids.append(db_user.id)
    return user_ids


def process_role_data(db: Session, raw_data: int):
    role_ids = []
    for role_data in raw_data:
        db_role = get_item_by_source_id(db, RoleModel.Role, role_data["id"])
        if db_role is None:
            db_role = RoleModel.Role(
                name=role_data["name"],
                description=role_data["description"],
                source_id=role_data["id"],
                source_update_at=role_data["updateDate"],
            )
            db.add(db_role)
            db.commit()
            db.refresh(db_role)
        else:
            if role_data["updateDate"] != None:
                db_last_update = formate_date(db_role.source_update_at, "DB")
                source_last_update = formate_date(
                    role_data["updateDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_role.name = role_data["name"]
                    db_role.description = role_data["description"]
                    db_role.source_update_at = role_data["updateDate"]
                    db.add(db_role)
                    db.commit()
                    db.refresh(db_role)
        role_ids.append(db_role.id)
    return role_ids


def process_teams_data(db: Session, raw_data):
    team_ids = []
    for team in raw_data:
        programId = None
        if team["programId"] is not None:
            db_program = get_item_by_source_id(
                db, ProgramModel.Program, team["programId"]
            )
            programId = db_program.id if db_program is not None else None
        db_team = get_item_by_source_id(db, TeamModel.Team, team["id"])
        is_kanban_team = (
            team["isKanbanTeam"] if team["isKanbanTeam"] is not None else False
        )
        if db_team is None:
            db_team = TeamModel.Team(
                name=team["name"],
                program_id=programId,
                description=team["description"],
                sprint_prefix=team["sprintPrefix"],
                short_name=team["shortName"],
                type=team["type"],
                is_active=team["isActive"],
                source_id=team["id"],
                source_update_at=team["lastUpdatedDate"],
                is_kanban_team=is_kanban_team,
            )
            db.add(db_team)
            db.commit()
            db.refresh(db_team)
        else:
            if team["lastUpdatedDate"] != None:
                db_last_update = formate_date(db_team.source_update_at, "DB")
                source_last_update = formate_date(
                    team["lastUpdatedDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_team.name = team["name"]
                    db_team.type = team["type"]
                    db_team.program_id = programId
                    db_team.description = team["description"]
                    db_team.sprint_prefix = team["sprintPrefix"]
                    db_team.short_name = team["shortName"]
                    db_team.source_update_at = team["lastUpdatedDate"]
                    db_team.is_kanban_team = is_kanban_team

                    db.add(db_team)
                    db.commit()
                    db.refresh(db_team)
        team_ids.append(db_team.id)
    return team_ids


def process_portfolios_data(db: Session, raw_data):
    portfolio_ids = []
    for portfolio in raw_data:
        teamId = None
        if portfolio["teamId"] is not None:
            db_team = get_item_by_source_id(
                db, TeamModel.Team, portfolio["teamId"]
            )
            teamId = db_team.id if db_team is not None else None
        db_portfolio = get_item_by_source_id(
            db, PortfolioModel.Portfolio, portfolio["id"]
        )
        if db_portfolio is None:
            db_portfolio = PortfolioModel.Portfolio(
                name=portfolio["title"],
                description=portfolio["description"],
                team_id=teamId,
                is_active=portfolio["isActive"],
                source_id=portfolio["id"],
                source_update_at=portfolio["lastUpdatedDate"],
            )
            db.add(db_portfolio)
            db.commit()
            db.refresh(db_portfolio)
        else:
            if portfolio["lastUpdatedDate"] != None:
                db_last_update = formate_date(
                    db_portfolio.source_update_at, "DB"
                )
                source_last_update = formate_date(
                    portfolio["lastUpdatedDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_portfolio.name = portfolio["title"]
                    db_portfolio.description = portfolio["description"]
                    db_portfolio.team_id = teamId
                    db_portfolio.is_active = portfolio["isActive"]
                    db_portfolio.source_update_at = portfolio[
                        "lastUpdatedDate"
                    ]

                    db.add(db_portfolio)
                    db.commit()
                    db.refresh(db_portfolio)
        portfolio_ids.append(db_portfolio.id)
    return portfolio_ids


def process_programs_data(db: Session, data):
    program_ids = []
    for program in data:
        team_id = program["teamId"]
        if program["teamId"] == -1:
            team_id = None
        else:
            if program["teamId"] is not None:
                db_team = get_item_by_source_id(
                    db, TeamModel.Team, program["teamId"]
                )
                if db_team is not None:
                    team_id = db_team.id

        db_portfolio = get_item_by_source_id(
            db, PortfolioModel.Portfolio, program["portfolioId"]
        )
        portfolio_id = None
        if db_portfolio is not None:
            portfolio_id = db_portfolio.id

        db_program = get_item_by_source_id(
            db, ProgramModel.Program, program["id"]
        )
        if db_program is None:
            db_program = ProgramModel.Program(
                name=program["title"],
                description=program["teamDescription"],
                portfolio_id=portfolio_id,
                team_id=team_id,
                source_id=program["id"],
                source_update_at=program["lastUpdatedDate"],
            )
            db.add(db_program)
            db.commit()
            db.refresh(db_program)
        else:
            if program["lastUpdatedDate"] != None:
                db_last_update = formate_date(
                    db_program.source_update_at, "DB"
                )
                source_last_update = formate_date(
                    program["lastUpdatedDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_program.name = program["title"]
                    db_program.description = program["teamDescription"]
                    db_program.portfolio_id = portfolio_id
                    db_program.team_id = team_id
                    db_program.source_update_at = program["lastUpdatedDate"]

                    db.add(db_program)
                    db.commit()
                    db.refresh(db_program)
        program_ids.append(db_program.id)
    return program_ids


def update_user_team_mapping(db: Session, user_id, teams):
    for team in teams:
        db_team = get_item_by_source_id(db, TeamModel.Team, team["teamId"])
        if db_team.user_ids is not None:
            if user_id not in db_team.user_ids:
                db_team.user_ids.append(user_id)
                flag_modified(db_team, "user_ids")
                db.merge(db_team)
                db.flush()
                db.commit()
        else:
            db_team.user_ids = user_id
            db.add(db_team)
            db.commit()
            db.refresh(db_team)


def process_teams_data_update_program(db: Session, raw_data):
    for team in raw_data:
        programId = None
        if team["programId"] is not None:
            db_program = get_item_by_source_id(
                db, ProgramModel.Program, team["programId"]
            )
            if db_program is not None:
                programId = db_program.id

        db_team = get_item_by_source_id(db, TeamModel.Team, team["id"])
        if db_team is not None:
            db_team.program_id = programId
            db.add(db_team)
            db.commit()
            db.refresh(db_team)
    return True


def soft_delete(db: Session, model, data):
    resp = (
        db.query(model)
        .filter(model.is_deleted.is_(False))
        .filter(model.source_id.isnot(None))
        .filter(model.id.notin_(data))
    )
    for item in resp:
        item.is_deleted = True
        db.add(item)
        db.commit()
        db.refresh(item)


def formate_date(date, type):
    if type == "DB":
        return datetime.strptime(
            date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "%Y-%m-%dT%H:%M:%SZ",
        )
    else:
        return datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")


def process_releases_data(db: Session, data):
    release_ids = []
    for release in data:
        db_portfolio = get_item_by_source_id(
            db, PortfolioModel.Portfolio, release["portfolioId"]
        )
        portfolio_id = None
        if db_portfolio is not None:
            portfolio_id = db_portfolio.id

        user_id = None
        if release["lastUpdatedBy"] is not None:
            db_user = get_item_by_source_id(
                db, UserModel.User, release["lastUpdatedBy"]
            )
            if db_user is not None:
                user_id = db_user.id

        db_release = get_item_by_source_id(
            db, ReleaseModel.Release, release["id"]
        )
        if db_release is None:
            db_release = ReleaseModel.Release(
                name=release["title"],
                short_name=release["shortName"],
                description=release["description"],
                portfolio_id=portfolio_id,
                source_id=release["id"],
                program_ids=release["programIds"],
                source_update_at=release["lastUpdatedDate"],
                start_date=release["startDate"],
                end_date=release["endDate"],
                updated_by=user_id,
            )
            db.add(db_release)
            db.commit()
            db.refresh(db_release)
        else:
            if release["lastUpdatedDate"] != None:
                db_last_update = formate_date(
                    db_release.source_update_at, "DB"
                )
                source_last_update = formate_date(
                    release["lastUpdatedDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_release.name = release["title"]
                    db_release.description = release["description"]
                    db_release.portfolio_id = portfolio_id
                    db_release.program_ids = release["programIds"]
                    db_release.start_date = release["startDate"]
                    db_release.end_date = release["endDate"]
                    db_release.source_update_at = release["lastUpdatedDate"]
                    db_release.short_name = release["shortName"]
                    db_release.updated_by = release["lastUpdatedBy"]

                    db.add(db_release)
                    db.commit()
                    db.refresh(db_release)
        release_ids.append(db_release.id)
    return release_ids


def process_sprints_data(db: Session, data):
    sprint_ids = []
    for sprint in data:
        db_program = get_item_by_source_id(
            db, ProgramModel.Program, sprint["programId"]
        )
        program_id = None
        if db_program is not None:
            program_id = db_program.id

        team_id = None
        if sprint["teamId"] is not None:
            db_team = get_item_by_source_id(
                db, TeamModel.Team, sprint["teamId"]
            )
            if db_team is not None:
                team_id = db_team.id

        release_id = None
        if sprint["releaseId"] is not None:
            db_release = get_item_by_source_id(
                db, ReleaseModel.Release, sprint["releaseId"]
            )
            if db_release is not None:
                release_id = db_release.id
        db_sprint = get_item_by_source_id(db, SprintModel.Sprint, sprint["id"])
        if db_sprint is None:
            db_sprint = SprintModel.Sprint(
                name=sprint["title"],
                short_name=sprint["shortName"],
                description=sprint["description"],
                program_id=program_id,
                team_id=team_id,
                release_id=release_id,
                source_id=sprint["id"],
                source_update_at=sprint["lastUpdatedDate"],
                begin_date=sprint["beginDate"],
                end_date=sprint["endDate"],
                actual_end_date=sprint["actualEndDate"],
            )
            db.add(db_sprint)
            db.commit()
            db.refresh(db_sprint)
        else:
            if sprint["lastUpdatedDate"] != None:
                db_last_update = formate_date(db_sprint.source_update_at, "DB")
                source_last_update = formate_date(
                    sprint["lastUpdatedDate"], "JA"
                )
                if db_last_update < source_last_update:
                    db_sprint.name = sprint["title"]
                    db_sprint.description = sprint["description"]
                    db_sprint.program_id = program_id
                    db_sprint.team_id = team_id
                    db_sprint.release_id = release_id
                    db_sprint.begin_date = sprint["beginDate"]
                    db_sprint.end_date = sprint["endDate"]
                    db_sprint.source_update_at = sprint["lastUpdatedDate"]
                    db_sprint.short_name = sprint["shortName"]

                    db.add(db_sprint)
                    db.commit()
                    db.refresh(db_sprint)
        sprint_ids.append(db_sprint.id)
    return sprint_ids
