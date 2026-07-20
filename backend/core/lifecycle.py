"""
Application lifecycle.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.container import container
from backend.core.logger import logger

from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.synchronizer import (
    KnowledgeSynchronizer,
)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    logger.info(
        "Starting Digital Twin Backend"
    )

    container.initialize()

    CorpusManager().initialize()

    KnowledgeSynchronizer().synchronize()

    logger.success(
        "Backend initialized."
    )

    yield

    logger.info(
        "Shutting down backend."
    )

    container.shutdown()