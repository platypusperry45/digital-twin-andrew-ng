"""
Application settings.

Loads configuration from the environment.

Author:
Digital Twin Project
"""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.config.constants import PROJECT_ROOT


class Settings(BaseSettings):

    APP_NAME: str = "Digital Twin of Andrew Ng"

    VERSION: str = "1.0.0"

    ENVIRONMENT: str = "development"

    LOG_LEVEL: str = "INFO"

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    DATABASE_URL: str = Field(
        default="sqlite:///backend/database/database.db"
    )

    GOOGLE_API_KEY_1: str | None = None
    GOOGLE_API_KEY_2: str | None = None
    GOOGLE_API_KEY_3: str | None = None
    GOOGLE_API_KEY_4: str | None = None
    GOOGLE_API_KEY_5: str | None = None

    REQUEST_TIMEOUT: int = 60

    MAX_RETRIES: int = 3

    CHROMA_DIRECTORY: str = str(PROJECT_ROOT / "vector_db")

    MEMORY_DIRECTORY: str = str(PROJECT_ROOT / "memory_store")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()