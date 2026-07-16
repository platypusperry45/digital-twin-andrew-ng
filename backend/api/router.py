"""
API router registry.
"""


from fastapi import APIRouter

from backend.api.routes.health import router as health_router

from backend.api.routes.chat import router as chat_router



router = APIRouter()


router.include_router(
    health_router
)


router.include_router(
    chat_router,
    prefix="/api/v1"
)