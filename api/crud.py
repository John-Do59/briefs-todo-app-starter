"""CRUD operations for Todo and User models."""

from sqlalchemy.orm import Session

from models import Todo, User, TodoDependency
from schemas import TodoCreate, TodoUpdate, UserCreate


# User CRUD
def get_users(db: Session) -> list[User]:
    """Return all users."""
    return db.query(User).all()


def get_user(db: Session, user_id: int) -> User | None:
    """Return a single user by ID, or None if not found."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Return a single user by username, or None if not found."""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    """Return a single user by email, or None if not found."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user and return it."""
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Todo CRUD
def get_todos(db: Session) -> list[Todo]:
    """Return all todos ordered by creation date (newest first)."""
    return db.query(Todo).order_by(Todo.created_at.desc()).all()


def get_todo(db: Session, todo_id: int) -> Todo | None:
    """Return a single todo by ID, or None if not found."""
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create_todo(db: Session, todo: TodoCreate) -> Todo:
    """Create a new todo and return it."""
    db_todo = Todo(**todo.model_dump())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: TodoUpdate) -> Todo | None:
    """Update an existing todo. Returns None if not found."""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return None
    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int) -> bool:
    """Delete a todo by ID. Returns True if deleted, False if not found."""
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not db_todo:
        return False
    db.delete(db_todo)
    db.commit()
    return True


# Todo Dependencies CRUD
def add_todo_dependency(db: Session, todo_id: int, depends_on_id: int) -> bool:
    """Add a dependency from todo_id to depends_on_id. Returns False if either todo doesn't exist."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    depends_on = db.query(Todo).filter(Todo.id == depends_on_id).first()
    if not todo or not depends_on:
        return False
    if depends_on_id not in [t.id for t in todo.depends_on]:
        todo.depends_on.append(depends_on)
        db.commit()
    return True


def remove_todo_dependency(db: Session, todo_id: int, depends_on_id: int) -> bool:
    """Remove a dependency. Returns False if either todo or the dependency doesn't exist."""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    depends_on = db.query(Todo).filter(Todo.id == depends_on_id).first()
    if not todo or not depends_on or depends_on not in todo.depends_on:
        return False
    todo.depends_on.remove(depends_on)
    db.commit()
    return True
