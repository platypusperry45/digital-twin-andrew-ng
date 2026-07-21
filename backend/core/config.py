"""
Application configuration management for Digital Twin of Andrew Ng.

Loads:
- Environment variables
- Provider configuration
- Application settings

Compatible with:
- Python 3.10+
- Pydantic v2
"""

from pathlib import Path
from typing import Literal, Any, Union
import yaml
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project Root Directory Resolution
BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROVIDERS_FILE = BASE_DIR / "backend" / "config" / "providers.yaml"


class Settings(BaseSettings):

    # ==========================
    # Application Metadata
    # ==========================
    APP_NAME: str = "Digital Twin of Andrew Ng"
    APP_VERSION: str = "1.0.0"
    APP_ENV: Literal[
        "development",
        "testing",
        "staging",
        "production",
    ] = "development"

    HOST: str = "0.0.0.0"
    PORT: int = Field(default=8000, ge=1, le=65535)
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # ==========================
    # Database & Storage Paths
    # ==========================
    DATABASE_URL: str = "sqlite:///backend/database/database.db"
    CHROMA_DB_PATH: str = "backend/data/vectorstore"
    MEMORY_STORE_PATH: str = "backend/data/memory"
    SCIENTIST_DATA_PATH: str = "backend/data/knowledge"

    # ==========================
    # Gemini API Keys
    # Union[list[str], str] prevents pydantic-settings from failing json.loads on comma-separated env values
    # ==========================
    GEMINI_API_KEYS: Union[list[str], str] = Field(default_factory=list)

    # ==========================
    # Gemini Model Specification
    # Enforcing Gemini 2.5 Flash per assignment constraints
    # ==========================
    PRIMARY_MODEL: str = "gemini-2.5-flash"
    FALLBACK_MODEL: str = "gemini-2.5-flash"
    FAST_MODEL: str = "gemini-2.5-flash"
    EMBEDDING_MODEL: str = "gemini-embedding-001"

    # ==========================
    # LLM Reliability & Scheduling
    # ==========================
    LLM_MAX_RETRIES: int = Field(default=3, ge=0)
    LLM_RETRY_DELAY: int = Field(default=2, ge=0)
    KEY_COOLDOWN_SECONDS: int = Field(default=60, ge=0)
    KEY_ROTATION_STRATEGY: str = "round_robin"

    # ==========================
    # Conversation & RAG Tuning
    # ==========================
    MAX_CONVERSATION_HISTORY: int = Field(default=10, ge=1)
    TOP_K_RESULTS: int = Field(default=5, ge=1)

    # ==========================
    # Feature Flags
    # ==========================
    ENABLE_MEMORY: bool = True
    ENABLE_RAG: bool = True
    ENABLE_MODEL_FALLBACK: bool = True
    ENABLE_KEY_ROTATION: bool = True

    # ==========================
    # Security & CORS
    # ==========================
    CORS_ORIGINS: Union[list[str], str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("GEMINI_API_KEYS", mode="before")
    @classmethod
    def parse_api_keys(cls, value: Any) -> list[str]:
        """Ensures comma-separated string or list input is parsed into a clean list of keys."""
        if isinstance(value, list):
            return [str(k).strip() for k in value if str(k).strip()]
        if isinstance(value, str) and value.strip():
            # If string is formatted as JSON array string like '["key1", "key2"]'
            if value.strip().startswith("[") and value.strip().endswith("]"):
                import json
                try:
                    parsed = json.loads(value)
                    if isinstance(parsed, list):
                        return [str(k).strip() for k in parsed if str(k).strip()]
                except Exception:
                    pass
            # Comma-separated fallback
            return [k.strip() for k in value.split(",") if k.strip()]
        return []

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(v).strip() for v in value]
        if isinstance(value, str) and value.strip():
            return [v.strip() for v in value.split(",") if v.strip()]
        return ["*"]

    def load_providers(self) -> dict[str, Any]:
        """Loads additional service providers configuration from YAML if present."""
        if not PROVIDERS_FILE.exists():
            return {}

        with open(PROVIDERS_FILE, "r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}


# Singleton settings instance used application-wide
settings = Settings()