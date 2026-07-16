"""
Central logger.

Uses Loguru.
"""

import sys
from pathlib import Path

from loguru import logger

from backend.core.config import settings


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger.remove()

# Console logger
logger.add(
    sys.stdout,
    colorize=True,
    enqueue=True,
    level=settings.LOG_LEVEL,
    backtrace=True,
    diagnose=settings.DEBUG,
    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    ),
)

# File logger
logger.add(
    LOG_DIR / "application.log",
    rotation="10 MB",
    retention="14 days",
    compression="zip",
    enqueue=True,
    level="DEBUG",
    backtrace=True,
    diagnose=settings.DEBUG,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
)


def get_logger():
    return logger