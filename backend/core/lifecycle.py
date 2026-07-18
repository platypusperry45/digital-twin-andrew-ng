"""
Application lifecycle management.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.container import container
from backend.core.logger import logger


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    """
    Startup and shutdown lifecycle.
    """

    logger.info(
        "=" * 70
    )

    logger.info(
        "Starting Digital Twin Backend..."
    )

    try:

        container.initialize()

        logger.success(
            "All services initialized successfully."
        )

    except Exception as exc:

        logger.exception(
            f"Startup failed: {exc}"
        )

        raise

    yield

    logger.info(
        "Shutting down services..."
    )

    try:

        container.shutdown()

        logger.success(
            "Shutdown completed."
        )

    except Exception as exc:

        logger.exception(
            f"Shutdown error: {exc}"
        )

    logger.info(
        "=" * 70
    )