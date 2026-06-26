"""Configuration management using environment variables."""

from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    environment: Literal["development", "production"] = "development"
    database_url: str = "sqlite:///./todo.db"
    secret_key: str = "change-me-in-production-please-very-important"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
