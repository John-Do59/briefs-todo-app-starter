"""SQLAlchemy ORM models."""

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    """Represents a user in the database."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    """Represents a to-do task in the database."""

    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Foreign keys
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("todos.id"), nullable=True)

    # Relationships
    owner = relationship("User", back_populates="todos")
    parent = relationship("Todo", remote_side=[id], back_populates="subtasks")
    subtasks = relationship("Todo", back_populates="parent", cascade="all, delete-orphan")
    depends_on = relationship("Todo", secondary="todo_dependencies",
                              primaryjoin="Todo.id==todo_dependencies.c.todo_id",
                              secondaryjoin="Todo.id==todo_dependencies.c.depends_on_id",
                              backref="dependent_todos")


class TodoDependency(Base):
    """Represents a dependency between two todos."""

    __tablename__ = "todo_dependencies"

    todo_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)
    depends_on_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)
