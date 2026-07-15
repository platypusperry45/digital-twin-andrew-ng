from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.container import Container
from backend.core.config import get_config
from backend.core.logger import get_logger

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Loading configuration...")

    config = get_config()

    container = Container()

    container.register("config", config)

    app.state.container = container

    logger.success("Application Started")

    yield

    logger.info("Cleaning resources...")

    container.clear()

    logger.success("Shutdown Complete")