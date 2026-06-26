"""Pydantic schemas for request/response validation."""

from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Shared fields for user operations."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    avatar_url: str | None = Field(None, max_length=255)


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str = Field(..., min_length=6, max_length=100)


class UserLogin(BaseModel):
    """Schema for user login."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=100)


class UserResponse(UserBase):
    """Schema for user responses."""

    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TodoBase(BaseModel):
    """Shared fields for todo operations."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=500)
    completed: bool = False
    owner_id: int | None = None
    parent_id: int | None = None


class TodoCreate(TodoBase):
    """Schema for creating a new todo."""


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo. All fields optional."""

    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=500)
    completed: bool | None = None
    owner_id: int | None = None
    parent_id: int | None = None


from pydantic import BaseModel, Field, EmailStr, field_validator

class TodoResponse(TodoBase):
    """Schema for todo responses including database-generated fields."""

    id: int
    created_at: datetime
    updated_at: datetime | None = None
    subtasks: list["TodoResponse"] = []
    depends_on: list[int] = []

    model_config = {"from_attributes": True}

    @field_validator("depends_on", mode="before")
    @classmethod
    def extract_dependency_ids(cls, v):
        if not v:
            return []
        return [item.id if hasattr(item, "id") else item for item in v]

TodoResponse.model_rebuild()
