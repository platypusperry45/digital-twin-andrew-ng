"""
Global project constants.
"""

from pathlib import Path

# -----------------------------------------------------------------------------
# Project Paths
# -----------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

BACKEND_DIR = PROJECT_ROOT / "backend"

DATA_DIR = PROJECT_ROOT / "scientist_data"

VECTOR_DB_DIR = PROJECT_ROOT / "vector_db"

MEMORY_STORE_DIR = PROJECT_ROOT / "memory_store"

DOCS_DIR = PROJECT_ROOT / "docs"

LOG_DIR = PROJECT_ROOT / "logs"

CONFIG_DIR = BACKEND_DIR / "config"

API_KEYS_FILE = CONFIG_DIR / "api_keys.json"

# -----------------------------------------------------------------------------
# Scientist
# -----------------------------------------------------------------------------

SCIENTIST_NAME = "Andrew Ng"

SCIENTIST_DOMAIN = "Artificial Intelligence"

# -----------------------------------------------------------------------------
# API
# -----------------------------------------------------------------------------

API_PREFIX = "/api/v1"

DEFAULT_TIMEOUT = 60

DEFAULT_RETRIES = 3

KEY_COOLDOWN_SECONDS = 300

# -----------------------------------------------------------------------------
# RAG
# -----------------------------------------------------------------------------

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

TOP_K_DOCUMENTS = 6

# -----------------------------------------------------------------------------
# Memory
# -----------------------------------------------------------------------------

SHORT_TERM_MEMORY_LIMIT = 20

LONG_TERM_IMPORTANCE_THRESHOLD = 0.65