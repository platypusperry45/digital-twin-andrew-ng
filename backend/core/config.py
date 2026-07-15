"""
Centralized application configuration.

Loads:
- .env
- backend/config/api_keys.yaml

Python: 3.13
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import yaml
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[2]


class GeminiKey(BaseModel):
    name: str
    key: str


class GeminiProviderConfig(BaseModel):
    model: str = "gemini-2.5-flash"

    temperature: float = 0.3

    timeout: int = 60

    max_retries: int = 5

    keys: list[GeminiKey] = Field(default_factory=list)


class ProvidersConfig(BaseModel):
    gemini: GeminiProviderConfig


class ApplicationConfig(BaseSettings):

    app_name: str = "Digital Twin of Andrew Ng"

    version: str = "1.0.0"

    environment: str = "development"

    host: str = "127.0.0.1"

    port: int = 8000

    log_level: str = "INFO"

    database_url: str = (
        "sqlite:///backend/database/database.db"
    )

    chroma_directory: str = "vector_db"

    memory_directory: str = "memory_store"

    scientist_directory: str = "scientist_data"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


class AppConfig(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    application: ApplicationConfig

    providers: ProvidersConfig


def _load_provider_config() -> ProvidersConfig:

    config_path = (
        ROOT_DIR
        / "backend"
        / "config"
        / "api_keys.yaml"
    )

    if not config_path.exists():

        raise FileNotFoundError(
            f"{config_path} not found"
        )

    with open(config_path, encoding="utf-8") as file:

        data = yaml.safe_load(file)

    return ProvidersConfig(**data["providers"])


@lru_cache(maxsize=1)
def get_config() -> AppConfig:

    return AppConfig(

        application=ApplicationConfig(),

        providers=_load_provider_config(),

    )