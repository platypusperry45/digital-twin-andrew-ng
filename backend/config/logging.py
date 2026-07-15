"""
Centralized logging.

Uses Loguru throughout the project.

Author:
Digital Twin Project
"""

import sys
from pathlib import Path

from loguru import logger

from backend.config.constants import LOG_DIR

LOG_DIR.mkdir(parents=True, exist_ok=True)

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    enqueue=True,
    backtrace=False,
    diagnose=False,
)

logger.add(
    LOG_DIR / "application.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="DEBUG",
    enqueue=True,
)

__all__ = ["logger"]