from pytest_bdd import scenarios, given, when, then, parsers
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# In-memory DB setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = lambda: Session(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Load scenarios
scenarios("features/auth_collaboration.feature")

@pytest.fixture
def context():
    return {}

@given(parsers.parse('the user registers with username "{username}", email "{email}", and password "{password}"'))
def register_user(username, email, password):
    response = client.post(
        "/users",
        json={"username": username, "email": email, "password": password}
    )
    assert response.status_code == 201

@when(parsers.parse('the user logs in with username "{username}" and password "{password}"'))
@given(parsers.parse('the user logs in with username "{username}" and password "{password}"'))
def login_user(username, password, context):
    response = client.post(
        "/token",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    context["token"] = response.json()["access_token"]
    context["headers"] = {"Authorization": f"Bearer {context['token']}"}

@then("the user should receive an access token")
def check_token(context):
    assert "token" in context

@when(parsers.parse('the user creates a task with title "{title}" assigned to "{assignee}"'))
def create_task(title, assignee, context):
    # First get the assignee ID
    users_resp = client.get("/users", headers=context["headers"])
    assert users_resp.status_code == 200
    assignee_id = next(u["id"] for u in users_resp.json() if u["username"] == assignee)
    
    response = client.post(
        "/todos",
        json={"title": title, "assignee_id": assignee_id},
        headers=context["headers"]
    )
    assert response.status_code == 201
    context["last_task"] = response.json()

@then("the task should be successfully created")
def check_task_created(context):
    assert "last_task" in context
    assert context["last_task"]["id"] is not None

@then(parsers.parse('the task should show "{assignee}" as the assignee'))
def check_task_assignee(assignee, context):
    task = context["last_task"]
    assert task["assignee"]["username"] == assignee

@when("the user lists tasks")
def list_tasks(context):
    response = client.get("/todos", headers=context["headers"])
    assert response.status_code == 200
    context["tasks"] = response.json()

@then(parsers.parse('the list should contain the task "{title}"'))
def check_list_contains_task(title, context):
    tasks = context["tasks"]
    titles = [t["title"] for t in tasks]
    assert title in titles
