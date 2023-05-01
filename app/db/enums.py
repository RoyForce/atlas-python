from enum import Enum


class AppType(str, Enum):
    JIRA_ALIGN = "Jira Align"


class ResourceType(str, Enum):
    USER = "USER"
    ROLE = "ROLE"
    PORTFOLIO = "PORTFOLIO"
    PROGRAM = "PROGRAM"
    TEAMS = "TEAMS"
    ORG = "ORG"
    SPRINT = "SPRINT"


class ResourceTypeUrl(str, Enum):
    USER = "User"
    PORTFOLIO_URL = "Portfolio"
    PROGRAM_URL = "Program"
    TEAMS_URL = "Teams"
