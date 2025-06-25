"""
Configuration settings for the application.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import field_validator, ConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # API settings
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Quiz Mercedes Benz API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"

    # PostgreSQL specific settings (for Docker)
    POSTGRES_DB: str = "quiz_db"
    POSTGRES_USER: str = "quiz_user"
    POSTGRES_PASSWORD: str = "quiz_password"
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: str = "5432"

    # Security settings
    SECRET_KEY: str = "your-secret-key-here"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    ALLOWED_HOSTS: str = "*"

    # External API settings
    STAR_WARS_API_URL: str = "https://swapi.dev/api/"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @property
    def database_url(self) -> str:
        """Get the database URL, constructing it from components if needed."""
        if self.DATABASE_URL != "sqlite:///./app.db":
            return self.DATABASE_URL

        # If we're in Docker or have PostgreSQL settings, use PostgreSQL
        if os.getenv("POSTGRES_USER") or os.getenv("DATABASE_URL", "").startswith(
            "postgresql"
        ):
            # Use environment variables if available, otherwise use defaults
            user = os.getenv("POSTGRES_USER", self.POSTGRES_USER)
            password = os.getenv("POSTGRES_PASSWORD", self.POSTGRES_PASSWORD)
            host = os.getenv("POSTGRES_HOST", self.POSTGRES_HOST)
            port = os.getenv("POSTGRES_PORT", self.POSTGRES_PORT)
            db = os.getenv("POSTGRES_DB", self.POSTGRES_DB)

            return f"postgresql://{user}:{password}@{host}:{port}/{db}"

        # Default to SQLite for local development
        return self.DATABASE_URL

    model_config = ConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        protected_namespaces=(),  # Disable protected namespace warnings
    )


settings = Settings()
