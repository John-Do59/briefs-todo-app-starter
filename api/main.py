"""FastAPI application entry point."""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import Base, engine, get_db

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="To-Do API",
    description="REST API for managing to-do tasks",
    version="0.2.0",
)


# User endpoints
@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    """List all users."""
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID."""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if username or email already exists
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


# Todo endpoints
@app.get("/todos", response_model=list[schemas.TodoResponse])
def list_todos(db: Session = Depends(get_db)):
    """List all todos."""
    return crud.get_todos(db)


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a single todo by ID."""
    todo = crud.get_todo(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=schemas.TodoResponse, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo."""
    return crud.create_todo(db, todo)


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """Update an existing todo."""
    updated = crud.update_todo(db, todo_id, todo)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo."""
    if not crud.delete_todo(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")


# Todo dependency endpoints
@app.post("/todos/{todo_id}/dependencies/{depends_on_id}", status_code=201)
def add_dependency(todo_id: int, depends_on_id: int, db: Session = Depends(get_db)):
    """Add a dependency: todo_id depends on depends_on_id."""
    if todo_id == depends_on_id:
        raise HTTPException(status_code=400, detail="A todo cannot depend on itself")
    if not crud.add_todo_dependency(db, todo_id, depends_on_id):
        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}/dependencies/{depends_on_id}", status_code=204)
def remove_dependency(todo_id: int, depends_on_id: int, db: Session = Depends(get_db)):
    """Remove a dependency."""
    if not crud.remove_todo_dependency(db, todo_id, depends_on_id):
        raise HTTPException(status_code=404, detail="Dependency not found")
