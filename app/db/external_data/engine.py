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


def create_update_external_data(db: Session, raw_data, type):
    if len(raw_data) > 0:
        if type == ResourceType.USER.value:
            process_user_data(db, raw_data)
        if type == ResourceType.ROLE.value:
            process_role_data(db, raw_data)
        if type == ResourceType.TEAM.value:
            process_teams_data(db, raw_data)
        if type == ResourceType.PORTFOLIO.value:
            process_portfolios_data(db, raw_data)
        if type == ResourceType.PROGRAM.value:
            process_programs_data(db, raw_data)
        if type == ResourceType.TEAMPRO.value:
            process_teams_data_update_program(db, raw_data)
    return True


def process_user_data(db: Session, raw_data):
    for user in raw_data:
        if user["status"] == "Active":
            if user["roleId"] is not None:
                db_role = (
                    db.query(RoleModel.Role)
                    .filter(RoleModel.Role.source_id == user["roleId"])
                    .first()
                )
            roleId = None
            if db_role is not None:
                roleId = db_role.id
            db_user = get_source_user(db, user["id"])
            if db_user is None:
                db_user = UserModel.User(
                    first_name=user["firstName"],
                    last_name=user["lastName"],
                    email=user["email"],
                    is_active=True,
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
                    db_last_update = datetime.strptime(
                        db_user.source_update_at.strftime(
                            "%Y-%m-%dT%H:%M:%SZ"
                        ),
                        "%Y-%m-%dT%H:%M:%SZ",
                    )
                    source_last_update = datetime.strptime(
                        user["lastUpdatedDate"], "%Y-%m-%dT%H:%M:%SZ"
                    )
                    if db_last_update < source_last_update:
                        update_data = dict(exclude_unset=True)
                        update_data["first_name"] = user["firstName"]
                        update_data["last_name"] = user["lastName"]
                        update_data["source_update_at"] = user[
                            "lastUpdatedDate"
                        ]
                        update_data["cost_center_id"] = user["costCenterId"]
                        for key, value in update_data.items():
                            setattr(db_user, key, value)

                        db.add(db_user)
                        db.commit()
                        db.refresh(db_user)
        if "teams" in user and len(user) > 0:
            update_user_team_mapping(db, db_user.id, user["teams"])
    return True


def get_source_user(db: Session, source_id: int):
    return (
        db.query(UserModel.User)
        .filter(UserModel.User.source_id == source_id)
        .first()
    )


def process_role_data(db: Session, raw_data: int):
    for role_data in raw_data:
        db_role = (
            db.query(RoleModel.Role)
            .filter(RoleModel.Role.source_id == role_data["id"])
            .first()
        )
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
                db_last_update = datetime.strptime(
                    db_role.source_update_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                source_last_update = datetime.strptime(
                    role_data["updateDate"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if db_last_update < source_last_update:
                    update_data = dict(exclude_unset=True)
                    update_data["name"] = role_data["name"]
                    update_data["description"] = role_data["description"]
                    update_data["source_update_at"] = role_data["updateDate"]
                    for key, value in update_data.items():
                        setattr(db_role, key, value)

                    db.add(db_role)
                    db.commit()
                    db.refresh(db_role)
    return True


def process_teams_data(db: Session, raw_data):
    for team in raw_data:
        programId = None
        if team["programId"] is not None:
            db_program = (
                db.query(ProgramModel.Program)
                .filter(ProgramModel.Program.source_id == team["programId"])
                .first()
            )
            if db_program is not None:
                programId = db_program.id
                print("-------")
                print(programId)

        print("---ssss----")
        print(programId)
        db_team = (
            db.query(TeamModel.Team)
            .filter(TeamModel.Team.source_id == team["id"])
            .first()
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
            )
            db.add(db_team)
            db.commit()
            db.refresh(db_team)
        else:
            if team["lastUpdatedDate"] != None:
                db_last_update = datetime.strptime(
                    db_team.source_update_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                source_last_update = datetime.strptime(
                    team["lastUpdatedDate"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if db_last_update < source_last_update:
                    update_data = dict(exclude_unset=True)
                    update_data["name"] = team["name"]
                    update_data["type"] = team["type"]
                    update_data["program_id"] = programId
                    update_data["description"] = team["description"]
                    update_data["sprint_prefix"] = team["sprintPrefix"]
                    update_data["short_name"] = team["shortName"]
                    update_data["source_update_at"] = team["lastUpdatedDate"]
                    for key, value in update_data.items():
                        setattr(db_team, key, value)

                    db.add(db_team)
                    db.commit()
                    db.refresh(db_team)

    return True


def process_portfolios_data(db: Session, raw_data):
    for portfolio in raw_data:
        teamId = None
        if portfolio["teamId"] is not None:
            db_team = (
                db.query(TeamModel.Team)
                .filter(TeamModel.Team.source_id == portfolio["teamId"])
                .first()
            )
            if db_team is not None:
                teamId = db_team.id

        db_portfolio = (
            db.query(PortfolioModel.Portfolio)
            .filter(PortfolioModel.Portfolio.id == portfolio["id"])
            .first()
        )
        if db_portfolio is None:
            db_portfolio = PortfolioModel.Portfolio(
                title=portfolio["title"],
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
                db_last_update = datetime.strptime(
                    db_portfolio.source_update_at.strftime(
                        "%Y-%m-%dT%H:%M:%SZ"
                    ),
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                source_last_update = datetime.strptime(
                    portfolio["lastUpdatedDate"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if db_last_update < source_last_update:
                    update_data = dict(exclude_unset=True)
                    update_data["title"] = portfolio["title"]
                    update_data["description"] = portfolio["description"]
                    update_data["team_id"] = teamId
                    update_data["is_active"] = portfolio["isActive"]
                    update_data["source_update_at"] = portfolio[
                        "lastUpdatedDate"
                    ]
                    for key, value in update_data.items():
                        setattr(db_portfolio, key, value)

                    db.add(db_portfolio)
                    db.commit()
                    db.refresh(db_portfolio)
    return True


def process_programs_data(db: Session, data):
    for program in data:
        team_id = None
        team_id = program["teamId"]
        if program["teamId"] == -1:
            team_id = None
        else:
            if program["teamId"] is not None:
                db_team = (
                    db.query(TeamModel.Team)
                    .filter(TeamModel.Team.source_id == program["teamId"])
                    .first()
                )
                if db_team is not None:
                    team_id = db_team.id
        db_program = (
            db.query(ProgramModel.Program)
            .filter(ProgramModel.Program.source_id == program["id"])
            .first()
        )
        db_portfolio = (
            db.query(PortfolioModel.Portfolio)
            .filter(
                PortfolioModel.Portfolio.source_id == program["portfolioId"]
            )
            .first()
        )
        portfolio_id = None
        if db_portfolio is not None:
            portfolio_id = db_portfolio.id
        if db_program is None:
            db_program = ProgramModel.Program(
                title=program["title"],
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
                db_last_update = datetime.strptime(
                    db_program.source_update_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "%Y-%m-%dT%H:%M:%SZ",
                )
                source_last_update = datetime.strptime(
                    program["lastUpdatedDate"], "%Y-%m-%dT%H:%M:%SZ"
                )
                if db_last_update < source_last_update:
                    update_data = dict(exclude_unset=True)
                    update_data["title"] = program["title"]
                    update_data["portfolio_id"] = portfolio_id
                    update_data["team_id"] = team_id
                    update_data["source_update_at"] = program[
                        "lastUpdatedDate"
                    ]
                    for key, value in update_data.items():
                        setattr(db_program, key, value)

                    db.add(db_program)
                    db.commit()
                    db.refresh(db_program)
    return True


def update_user_team_mapping(db: Session, user_id, teams):
    for team in teams:
        db_team = (
            db.query(TeamModel.Team)
            .filter(TeamModel.Team.source_id == team["teamId"])
            .first()
        )
        if db_team.user_ids is not None:
            if user_id not in db_team.user_ids:
                db_team.user_ids.append(user_id)
                flag_modified(db_team, "user_ids")
                db.merge(db_team)
                db.flush()
                db.commit()
        else:
            update_data = dict(exclude_unset=True)
            update_data["user_ids"] = (user_id,)
            update_data["description"] = ("sssssssss",)
            for key, value in update_data.items():
                setattr(db_team, key, value)
            db.add(db_team)
            db.commit()
            db.refresh(db_team)


def process_teams_data_update_program(db: Session, raw_data):
    for team in raw_data:
        programId = None
        if team["programId"] is not None:
            db_program = (
                db.query(ProgramModel.Program)
                .filter(ProgramModel.Program.source_id == team["programId"])
                .first()
            )
            if db_program is not None:
                programId = db_program.id
                print("-------")
                print(programId)

        print("---ssss----")
        print(programId)
        db_team = (
            db.query(TeamModel.Team)
            .filter(TeamModel.Team.source_id == team["id"])
            .first()
        )
        if db_team is not None:
            update_data = dict(exclude_unset=True)
            update_data["program_id"] = programId
            for key, value in update_data.items():
                setattr(db_team, key, value)

            db.add(db_team)
            db.commit()
            db.refresh(db_team)
    return True
