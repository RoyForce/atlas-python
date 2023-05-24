from enum import Enum


class SourceApp(str, Enum):
    JIRA_ALIGN = "JIRA-ALIGN"


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
