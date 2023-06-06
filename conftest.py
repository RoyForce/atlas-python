import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient
import typing as t

from app.core import config, security
from app.db.session import Base, get_db
from app.db.users.models import User
from app.db.roles.models import Role
from app.db.jobs.models import Job
from app.db.application_urls.models import ApplicationUrl
from app.db.application_types.models import ApplicationType

from app.db.playbooks.models import Playbook
from app.db.lessons.models import Lesson
from app.db.courses.models import Course
from app.db.use_cases.models import UseCase
from app.db.screens.models import Screen
from app.db.portfolios.models import Portfolio
from app.db.programs.models import Program
from app.db.teams.models import Team
from app.db.cost_centers.models import CostCenter
from app.db.assessments.models import Assessment
from app.db.dimensions.models import Dimension
from app.db.objectives.models import Objective
from app.main import app


def get_test_db_url() -> str:
    return f"{config.SQLALCHEMY_DATABASE_URI}_test"


@pytest.fixture
def test_db():
    """
    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    engine = create_engine(
        get_test_db_url(),
    )

    connection = engine.connect()
    trans = connection.begin()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, "after_transaction_end")
    def restart_savepoint(s, transaction):
        if transaction.nested and not transaction._parent.nested:
            s.expire_all()
            s.begin_nested()

    yield test_session

    # Roll back the parent transaction after the test is complete
    test_session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Create a test database and use it for the whole test session.
    """

    test_db_url = get_test_db_url()

    # Create the test database
    assert not database_exists(
        test_db_url
    ), "Test database already exists. Aborting tests."
    create_database(test_db_url)
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(test_db_url)


@pytest.fixture
def client(test_db):
    """
    Get a TestClient instance that reads/write to the test database.
    """

    def get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)


@pytest.fixture
def test_password() -> str:
    return "securepassword"


def get_password_hash() -> str:
    """
    Password hashing can be expensive so a mock will be much faster
    """
    return "supersecrethash"


@pytest.fixture
def test_user(test_db) -> User:
    """
    Make a test user in the database
    """

    user = User(
        first_name="Test User",
        email="fake@email.com",
        hashed_password=get_password_hash(),
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    return user


@pytest.fixture
def test_superuser(test_db) -> User:
    """
    Superuser for testing
    """

    user = User(
        email="fakeadmin@email.com",
        hashed_password=get_password_hash(),
        is_superuser=True,
    )
    test_db.add(user)
    test_db.commit()
    return user


def verify_password_mock(first: str, second: str) -> bool:
    return True


@pytest.fixture
def user_token_headers(
    client: TestClient, test_user, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_user.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def extension_token_headers() -> t.Dict[str, str]:
    headers = {"Authorization": f"Bearer {security.EXTENSION_TOKEN}"}
    return headers


@pytest.fixture
def superuser_token_headers(
    client: TestClient, test_superuser, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_superuser.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def test_role(test_db) -> Role:
    """
    Make a test role in the database
    """

    role = Role(name="Developer", description="Develops things")
    test_db.add(role)
    test_db.commit()
    return role


@pytest.fixture
def test_application_url(test_db) -> ApplicationUrl:
    """
    Make a test application url in the database
    """

    application_url = ApplicationUrl(
        name="Atlas", url="atlas.com", description="test"
    )
    test_db.add(application_url)
    test_db.commit()
    return application_url


@pytest.fixture
def test_application_type(test_db) -> ApplicationType:
    """
    Make a test application type in the database
    """

    application_type = ApplicationType(name="Atlas", description="test")
    test_db.add(application_type)
    test_db.commit()
    return application_type


@pytest.fixture
def test_job(test_db, test_application_url) -> Job:
    """
    Make a test Job in the database
    """

    jobs = Job(
        name="testName",
        description="testDesc",
        application_url_id=test_application_url.id,
        is_template=False,
    )
    test_db.add(jobs)
    test_db.commit()
    return jobs


@pytest.fixture
def test_playbook(test_db) -> Playbook:
    """
    Make a test playbook in the database
    """

    playbooks = Playbook(
        name="testName",
        description="testDesc",
        page_content="testpagecont",
    )
    test_db.add(playbooks)
    test_db.commit()
    return playbooks


@pytest.fixture
def test_lesson(test_db) -> Lesson:
    """
    Make a test lessons in the database
    """

    lesson = Lesson(
        name="test name",
        description="test desc",
        duration=1,
        page_content="testpagecont",
        is_template=True,
    )
    test_db.add(lesson)
    test_db.commit()
    return lesson


@pytest.fixture
def test_course(test_db) -> Course:
    """
    Make a test course in the database
    """

    course = Course(
        name="test name",
        description="test desc",
        duration=1,
        enroll_required=True,
        passing_percentage=1,
    )
    test_db.add(course)
    test_db.commit()
    return course


@pytest.fixture
def test_use_case(test_db) -> UseCase:
    """
    Make a test UseCase in the database
    """

    use_cases = UseCase(
        name="testname",
        description="testdesc",
        table_config="testconf",
    )
    test_db.add(use_cases)
    test_db.commit()
    return use_cases


@pytest.fixture
def test_screen(test_db) -> Screen:
    screens = Screen(name="testNameScreen", description="testDescScreen")
    test_db.add(screens)
    test_db.commit()
    return screens


@pytest.fixture
def test_portfolio(test_db) -> Portfolio:
    portfolio = Portfolio(name="test-portfolio", description="testDesc", id=1)
    test_db.add(portfolio)
    test_db.commit()
    return portfolio


@pytest.fixture
def test_program(test_db, test_portfolio, test_team) -> Program:
    program = Program(
        name="Test Program",
        description="Test Program desc",
        portfolio_id=test_portfolio.id,
        team_id=test_team.id,
        id=1,
    )
    test_db.add(program)
    test_db.commit()
    return program


@pytest.fixture
def test_team(test_db) -> Team:
    team = Team(name="Test Teams", description="test desc", type=1, id=1)
    test_db.add(team)
    test_db.commit()
    return team


@pytest.fixture
def test_cost_center(test_db) -> CostCenter:
    costcenter = CostCenter(
        name="Test Cost center", description="test desc", hr_rate=1, id=1
    )
    test_db.add(costcenter)
    test_db.commit()
    return costcenter


@pytest.fixture
def test_assessment(test_db) -> Assessment:
    assessment = Assessment(
        name="Test Assessment", description="test assessment desc"
    )
    test_db.add(assessment)
    test_db.commit()
    return assessment


@pytest.fixture
def test_dimension(test_db) -> Dimension:
    dimensions = Dimension(
        name="Test dimensions", description="test dimensions desc"
    )
    test_db.add(dimensions)
    test_db.commit()
    return dimensions


@pytest.fixture
def test_objective(test_db) -> Objective:
    objective = Objective(
        name="Test objective",
        description="test objective desc",
        start_value=1,
        target_value=2,
        metrics_type="UNITS",
    )
    test_db.add(objective)
    test_db.commit()
    return objective
