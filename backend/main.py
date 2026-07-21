"""
Andrew Ng Digital Twin Backend.

Application entrypoint.
"""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.container import container
from backend.core.config import settings
from backend.core.logger import logger

from backend.api.routes.chat import router as chat_router


# ==========================================================
# Lifespan
# ==========================================================


@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info(
        "Starting Andrew Ng Backend..."
    )

    container.initialize()

    logger.success(
        "Application startup complete."
    )

    yield

    logger.info(
        "Stopping Andrew Ng Backend..."
    )

    container.shutdown()

    logger.success(
        "Application shutdown complete."
    )


# ==========================================================
# FastAPI
# ==========================================================


app = FastAPI(

    title="Andrew Ng Digital Twin",

    description="Production AI backend",

    version="1.0.0",

    lifespan=lifespan,

)


# ==========================================================
# Middleware
# ==========================================================


app.add_middleware(

    CORSMiddleware,

    allow_origins=getattr(
        settings,
        "CORS_ORIGINS",
        ["*"],
    ),

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)


# ==========================================================
# Routes
# ==========================================================


app.include_router(chat_router)


# ==========================================================
# Root
# ==========================================================


@app.get("/")
def root():

    return {

        "name": "Andrew Ng Digital Twin",

        "status": "running",

        "version": "1.0.0",

    }


# ==========================================================
# Readiness
# ==========================================================


@app.get("/ready")
def ready():

    return {

        "ready": True,

        "llm": container.llm.health(),

    }


# ==========================================================
# Liveness
# ==========================================================


@app.get("/live")
def live():

    return {

        "alive": True,

    }