"""
Application configuration management.

Loads:
- environment variables
- provider configuration
- application settings

Compatible with:
Python 3.13
Pydantic v2
"""

from pathlib import Path

import yaml

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


BASE_DIR = Path(__file__).resolve().parent.parent.parent

PROVIDERS_FILE = (
    BASE_DIR
    /
    "backend"
    /
    "config"
    /
    "providers.yaml"
)


class Settings(BaseSettings):

    # ==========================
    # Application
    # ==========================

    APP_NAME: str = (
        "Digital Twin of Andrew Ng"
    )

    APP_VERSION: str = "1.0.0"

    APP_ENV: str = "development"

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    DEBUG: bool = True

    LOG_LEVEL: str = "INFO"


    # ==========================
    # Database
    # ==========================

    DATABASE_URL: str = (
        "sqlite:///backend/database/database.db"
    )


    # ==========================
    # Storage
    # ==========================

    CHROMA_DB_PATH: str = "vector_db"

    MEMORY_STORE_PATH: str = "memory_store"

    SCIENTIST_DATA_PATH: str = "scientist_data"


    # ==========================
    # Gemini Keys
    # ==========================

    GEMINI_API_KEYS: str = ""

    # ==========================
    # Gemini Models
    # ==========================

    PRIMARY_MODEL: str = (
        "gemini-3.5-flash"
    )

    FALLBACK_MODEL: str = (
        "gemini-2.5-pro"
    )

    FAST_MODEL: str = (
        "gemini-3.1-flash-lite"
    )

    EMBEDDING_MODEL: str = (
        "gemini-embedding-2"
    )


    # ==========================
    # LLM Reliability
    # ==========================

    LLM_MAX_RETRIES: int = 3

    LLM_RETRY_DELAY: int = 2

    KEY_COOLDOWN_SECONDS: int = 60

    # ==========================
    # Conversation
    # ==========================

    MAX_CONVERSATION_HISTORY = 10
    
    # ==========================
    # Feature Flags
    # ==========================

    ENABLE_MEMORY: bool = True

    ENABLE_RAG: bool = True

    ENABLE_MODEL_FALLBACK: bool = True

    ENABLE_KEY_ROTATION: bool = True


    TOP_K_RESULTS: int = 5


    # ==========================
    # Scheduler
    # ==========================

    KEY_ROTATION_STRATEGY: str = (
        "round_robin"
    )


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


    def load_providers(self):

        if not PROVIDERS_FILE.exists():
            return {}

        with open(
            PROVIDERS_FILE,
            "r",
            encoding="utf-8",
        ) as file:

            return yaml.safe_load(file)



# IMPORTANT:
# Singleton used everywhere

settings = Settings()


# Normalize Gemini keys

# Normalize Gemini keys

settings.GEMINI_API_KEYS = [
    key.strip()
    for key in settings.GEMINI_API_KEYS.split(",")
    if key.strip()
]