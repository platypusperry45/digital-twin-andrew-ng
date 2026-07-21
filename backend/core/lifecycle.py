"""
Application Lifecycle Management.

Single source of truth for FastAPI startup and shutdown sequences.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI

from backend.core.container import container
from backend.core.logger import logger
from backend.knowledge.corpus_manager import CorpusManager
from backend.knowledge.synchronizer import KnowledgeSynchronizer


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Andrew Ng Digital Twin Backend...")

    try:
        # Initialize Core Dependency Injection Graph
        container.initialize()

        # Initialize Corpus & Knowledge Base
        try:
            CorpusManager().initialize()
            KnowledgeSynchronizer().synchronize()
            logger.info("Knowledge corpus & sync completed.")
        except Exception as ke:
            logger.warning(f"Knowledge corpus initialization warning (non-fatal): {ke}")

        logger.success("Backend startup completed successfully.")

        yield

    finally:
        logger.info("Stopping Andrew Ng Digital Twin Backend...")

        try:
            container.shutdown()
            logger.success("Backend shutdown completed successfully.")
        except Exception as e:
            logger.exception(f"Unexpected error during shutdown: {e}")