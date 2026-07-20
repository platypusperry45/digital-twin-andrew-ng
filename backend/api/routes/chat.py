"""
Chat API.

Thin API layer.

All business logic lives inside
ConversationService.
"""

from fastapi import APIRouter, HTTPException

from backend.core.logger import logger

from backend.services.conversation_service import (
    ConversationService,
)

from backend.services.models import (
    ConversationRequest,
    ConversationResponse,
)

router = APIRouter()

service = ConversationService()


@router.post(
    "/chat",
    response_model=ConversationResponse,
)
def chat(
    request: ConversationRequest,
) -> ConversationResponse:
    """
    Chat endpoint.
    """

    logger.info("Received chat request.")

    try:

        return service.chat(
            request.message,
        )

    except Exception as exc:

        logger.exception(
            "Chat request failed."
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc