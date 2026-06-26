"""Unit tests for the CRUD layer (no HTTP)."""

import pytest
import crud
from schemas import TodoCreate, TodoUpdate, UserCreate


@pytest.fixture
def user_id(db_session):
    user = crud.create_user(db_session, UserCreate(username="testuser", email="test@example.com", password="password123"))
    return user.id


def test_create_and_get_todo(db_session, user_id):
    todo = crud.create_todo(db_session, TodoCreate(title="Buy milk"), user_id)

    assert todo.id is not None
    assert todo.title == "Buy milk"
    assert todo.completed is False

    fetched = crud.get_todo(db_session, todo.id, user_id)
    assert fetched is not None
    assert fetched.id == todo.id


def test_get_todo_returns_none_when_missing(db_session, user_id):
    assert crud.get_todo(db_session, 9999, user_id) is None


def test_list_todos_returns_all(db_session, user_id):
    crud.create_todo(db_session, TodoCreate(title="first"), user_id)
    crud.create_todo(db_session, TodoCreate(title="second"), user_id)

    todos = crud.get_todos(db_session, user_id)

    assert len(todos) == 2
    assert {t.title for t in todos} == {"first", "second"}


def test_update_todo_only_changes_provided_fields(db_session, user_id):
    todo = crud.create_todo(
        db_session,
        TodoCreate(title="Original", description="keep me"),
        user_id
    )

    updated = crud.update_todo(
        db_session,
        todo.id,
        TodoUpdate(completed=True),
        user_id
    )

    assert updated is not None
    assert updated.completed is True
    assert updated.title == "Original"
    assert updated.description == "keep me"


def test_update_todo_returns_none_when_missing(db_session, user_id):
    assert crud.update_todo(db_session, 9999, TodoUpdate(title="x"), user_id) is None


def test_delete_todo(db_session, user_id):
    todo = crud.create_todo(db_session, TodoCreate(title="Drop me"), user_id)

    assert crud.delete_todo(db_session, todo.id, user_id) is True
    assert crud.get_todo(db_session, todo.id, user_id) is None


def test_delete_todo_returns_false_when_missing(db_session, user_id):
    assert crud.delete_todo(db_session, 9999, user_id) is False
