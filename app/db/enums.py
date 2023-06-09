from enum import Enum


class SourceApp(str, Enum):
    JIRA_ALIGN = "JIRA-ALIGN"


class ActionType(str, Enum):
    COURSE = "COURSE"
    ASSESSMENT = "ASSESSMENT"
    MENTORING = "MENTORING"


class ResourceType(str, Enum):
    TEAM = "TEAM"
    ROLE = "ROLE"
    USER = "USER"
    PORTFOLIO = "PORTFOLIO"
    PROGRAM = "PROGRAM"
    SPRINT = "SPRINT"
    TEAMPRO = "TEAMPRO"


class ResourceUrl(str, Enum):
    USER = "Users?expand=true"
    ROLE = "systemroles"
    PORTFOLIO = "Portfolios"
    PROGRAM = "Programs"
    TEAM = "Teams"
    SPRINT = "Iterations"
    TEAMPRO = "Teams"


class OrganizationType(str, Enum):
    """
    NOTE: Remember to update the "organization_type_enum" enum in the database as well
    if you add a new organization type here. Ref: app/alembic/versions/9e07696e059f_create_play_table.py
    """

    PORTFOLIO = "PORTFOLIO"
    PROGRAM = "PROGRAM"
    TEAM = "TEAM"


class MetricsType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    DOLLARS = "DOLLARS"
    UNITS = "UNITS"
