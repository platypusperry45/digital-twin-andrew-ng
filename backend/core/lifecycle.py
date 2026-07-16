"""
Application lifecycle management.
"""


from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.core.container import container
from backend.core.logger import logger



@asynccontextmanager
async def lifespan(
    app: FastAPI
):

    logger.info(
        "Starting Digital Twin backend"
    )


    container.initialize()


    logger.info(
        "Services initialized"
    )


    yield


    logger.info(
        "Shutting down services"
    )


    container.shutdown()