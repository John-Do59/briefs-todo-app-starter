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
    hashed_password = Column(String(255), nullable=False)
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    todos = relationship("Todo", foreign_keys="Todo.owner_id", back_populates="owner")

    def to_dict(self) -> dict:
        """Convert model to dict for serialization."""
        from sqlalchemy.orm import class_mapper
        mapper = class_mapper(self.__class__)
        result = {column.key: getattr(self, column.key) for column in mapper.columns}
        # Handle datetime conversion
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        # Remove hashed password from response
        result.pop("hashed_password", None)
        return result


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
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    parent_id = Column(Integer, ForeignKey("todos.id"), nullable=True)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="todos")
    assignee = relationship("User", foreign_keys=[assignee_id])
    parent = relationship("Todo", remote_side=[id], back_populates="subtasks")
    subtasks = relationship("Todo", back_populates="parent", cascade="all, delete-orphan")
    depends_on = relationship("Todo", secondary="todo_dependencies",
                              primaryjoin="Todo.id==todo_dependencies.c.todo_id",
                              secondaryjoin="Todo.id==todo_dependencies.c.depends_on_id",
                              backref="dependent_todos")

    def to_dict(self) -> dict:
        """Convert model to dict for serialization."""
        from sqlalchemy.orm import class_mapper
        mapper = class_mapper(self.__class__)
        result = {column.key: getattr(self, column.key) for column in mapper.columns}
        # Handle datetime conversion
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        # Handle relationships
        result["subtasks"] = [subtask.to_dict() for subtask in self.subtasks]
        result["depends_on"] = [dep.id for dep in self.depends_on]
        return result


class TodoDependency(Base):
    """Represents a dependency between two todos."""

    __tablename__ = "todo_dependencies"

    todo_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)
    depends_on_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)
