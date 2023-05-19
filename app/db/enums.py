from enum import Enum


class Source(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class SourceApp(str, Enum):
    JIRA_ALIGN = "JIRA-ALIGN"
    JIRA = "JIRA"


class ResourceType(str, Enum):
    TEAM = "TEAM"
    USER = "USER"
    PORTFOLIO = "PORTFOLIO"
    PROGRAM = "PROGRAM"
    SPRINT = "SPRINT"


class ResourceUrl(str, Enum):
    USER = "Users?expand=true"
    PORTFOLIO = "Portfolios"
    PROGRAM = "Programs"
    TEAM = "Teams"
    SPRINT = "Iterations"
