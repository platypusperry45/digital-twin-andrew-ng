"""
Chat API Routes.

Exposes the conversation service through FastAPI.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from backend.core.container import container
from backend.core.logger import logger

from backend.llm.exceptions import (
    LLMException,
    SafetyBlockedError,
    RateLimitError,
    ModelUnavailableError,
)

from backend.services.models import (
    ConversationRequest,
    ConversationResponse,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# ==========================================================
# Chat
# ==========================================================

@router.post(
    "",
    response_model=ConversationResponse,
)
def chat(
    request: ConversationRequest,
) -> ConversationResponse:

    try:

        return (
            container
            .conversation_service
            .chat(request)
        )

    except SafetyBlockedError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except RateLimitError as exc:

        raise HTTPException(
            status_code=429,
            detail=str(exc),
        )

    except ModelUnavailableError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        )

    except LLMException as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    except Exception:

        logger.exception(
            "Unexpected server error."
        )

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )


# ==========================================================
# Streaming Chat
# ==========================================================

@router.post(
    "/stream",
)
def stream(
    request: ConversationRequest,
):

    service = container.conversation_service

    try:

        memory = service.memory.retrieve_context(
            request.message
        )

        knowledge = service.retriever.retrieve(
            request.message
        )

        profile = service.personality.get_profile()

        llm_request = (
            service.prompt_builder.build(
                profile=profile,
                memory=memory,
                knowledge=knowledge,
                user_prompt=request.message,
            )
        )

        return StreamingResponse(

            service.llm.stream(
                llm_request
            ),

            media_type="text/plain",

        )

    except Exception:

        logger.exception(
            "Streaming request failed."
        )

        raise HTTPException(
            status_code=500,
            detail="Streaming failed.",
        )


# ==========================================================
# LLM Health
# ==========================================================

@router.get(
    "/llm/health",
)
def llm_health():

    return (
        container
        .conversation_service
        .llm
        .health()
    )


# ==========================================================
# Backend Health
# ==========================================================

@router.get(
    "/health",
)
def backend_health():

    return (
        container
        .conversation_service
        .health()
    )