from fastapi import APIRouter
from fastapi import Request

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
async def health(
    request: Request,
):

    container = request.app.state.container

    config = container.resolve("config")

    return {

        "status": "healthy",

        "application": config.application.app_name,

        "environment": config.application.environment,

        "version": config.application.version,

    }