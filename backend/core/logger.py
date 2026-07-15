"""
Central logger.

Uses Loguru.
"""

from pathlib import Path
import sys

from loguru import logger


LOG_DIR = Path("logs")

LOG_DIR.mkdir(exist_ok=True)


logger.remove()

logger.add(

    sys.stdout,

    colorize=True,

    enqueue=True,

    level="INFO",

    format=(
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level}</level> | "
        "<cyan>{name}</cyan> | "
        "<level>{message}</level>"
    ),
)

logger.add(

    LOG_DIR / "application.log",

    rotation="10 MB",

    retention="14 days",

    compression="zip",

    enqueue=True,

    level="DEBUG",

)


def get_logger():

    return logger