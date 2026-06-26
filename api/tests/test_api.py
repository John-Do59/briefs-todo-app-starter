"""Integration-style tests against the FastAPI app via TestClient."""


# User tests
def test_list_users_empty(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user(client):
    response = client.post(
        "/users",
        json={"username": "johndoe", "email": "john@example.com", "password": "password123", "avatar_url": "https://example.com/avatar.jpg"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["username"] == "johndoe"
    assert body["email"] == "john@example.com"
    assert body["avatar_url"] == "https://example.com/avatar.jpg"


def test_create_user_duplicate_username(client):
    client.post("/users", json={"username": "jane", "email": "jane1@example.com", "password": "password123"})
    response = client.post("/users", json={"username": "jane", "email": "jane2@example.com", "password": "password123"})
    assert response.status_code == 400


def test_create_user_duplicate_email(client):
    client.post("/users", json={"username": "jake1", "email": "jake@example.com", "password": "password123"})
    response = client.post("/users", json={"username": "jake2", "email": "jake@example.com", "password": "password123"})
    assert response.status_code == 400


def test_get_user(client):
    created = client.post("/users", json={"username": "bob", "email": "bob@example.com", "password": "password123"}).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()["username"] == "bob"

def test_get_user_not_found(client):
    response = client.get("/users/9999")
    assert response.status_code == 404


# Todo tests
def test_list_todos_empty(auth_client):
    response = auth_client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []


def test_create_todo(auth_client):
    response = auth_client.post(
        "/todos",
        json={"title": "Write tests", "description": "with pytest"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["id"] > 0
    assert body["title"] == "Write tests"
    assert body["description"] == "with pytest"
    assert body["completed"] is False
    assert "created_at" in body


def test_create_todo_with_owner(auth_client, client):
    user = client.post("/users", json={"username": "alice", "email": "alice@example.com", "password": "password123"}).json()
    response = auth_client.post(
        "/todos",
        json={"title": "Alice's task", "owner_id": user["id"]},
    )
    assert response.status_code == 201
    # The endpoint should ignore the provided owner_id and use the authenticated user's ID
    assert response.json()["owner_id"] != user["id"]
    # get current user ID
    me = auth_client.get("/users/me").json()
    assert response.json()["owner_id"] == me["id"]


def test_create_todo_with_subtask(auth_client):
    parent = auth_client.post("/todos", json={"title": "Parent task"}).json()
    subtask = auth_client.post(
        "/todos",
        json={"title": "Subtask", "parent_id": parent["id"]},
    ).json()
    assert subtask["parent_id"] == parent["id"]
    parent_response = auth_client.get(f"/todos/{parent['id']}").json()
    assert any(t["id"] == subtask["id"] for t in parent_response["subtasks"])


def test_create_todo_validation_error(auth_client):
    response = auth_client.post("/todos", json={"title": ""})
    assert response.status_code == 422


def test_get_todo(auth_client):
    created = auth_client.post("/todos", json={"title": "Read book"}).json()

    response = auth_client.get(f"/todos/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == "Read book"


def test_get_todo_not_found(auth_client):
    response = auth_client.get("/todos/9999")
    assert response.status_code == 404


def test_update_todo(auth_client):
    created = auth_client.post("/todos", json={"title": "Old title"}).json()

    response = auth_client.put(
        f"/todos/{created['id']}",
        json={"title": "New title", "completed": True},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "New title"
    assert body["completed"] is True


def test_update_todo_not_found(auth_client):
    response = auth_client.put("/todos/9999", json={"title": "nope"})
    assert response.status_code == 404


def test_delete_todo(auth_client):
    created = auth_client.post("/todos", json={"title": "Delete me"}).json()

    response = auth_client.delete(f"/todos/{created['id']}")

    assert response.status_code == 204
    assert auth_client.get(f"/todos/{created['id']}").status_code == 404


def test_delete_todo_not_found(auth_client):
    response = auth_client.delete("/todos/9999")
    assert response.status_code == 404


# Dependency tests
def test_add_todo_dependency(auth_client):
    todo1 = auth_client.post("/todos", json={"title": "Do first"}).json()
    todo2 = auth_client.post("/todos", json={"title": "Do second"}).json()

    response = auth_client.post(f"/todos/{todo2['id']}/dependencies/{todo1['id']}")
    assert response.status_code == 201

    todo2_response = auth_client.get(f"/todos/{todo2['id']}").json()
    assert todo1["id"] in todo2_response["depends_on"]


def test_add_self_dependency(auth_client):
    todo = auth_client.post("/todos", json={"title": "Self"}).json()
    response = auth_client.post(f"/todos/{todo['id']}/dependencies/{todo['id']}")
    assert response.status_code == 400


def test_remove_todo_dependency(auth_client):
    todo1 = auth_client.post("/todos", json={"title": "1"}).json()
    todo2 = auth_client.post("/todos", json={"title": "2"}).json()
    auth_client.post(f"/todos/{todo2['id']}/dependencies/{todo1['id']}")

    response = auth_client.delete(f"/todos/{todo2['id']}/dependencies/{todo1['id']}")
    assert response.status_code == 204

    todo2_response = auth_client.get(f"/todos/{todo2['id']}").json()
    assert todo1["id"] not in todo2_response["depends_on"]
