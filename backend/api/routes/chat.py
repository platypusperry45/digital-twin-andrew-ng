"""
Chat API endpoint.
"""

from fastapi import APIRouter, HTTPException

from backend.core.container import container

from backend.llm.models import LLMRequest

from backend.services.models import (
    ChatResponse,
    SourceReference,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: LLMRequest,
):

    try:

        conversation = (
            container
            .conversation
            .chat(request)
        )

        sources = []

        for result in conversation.knowledge.results:

            sources.append(

                SourceReference(

                    filename=result.filename,

                    source=result.source,

                    score=result.score,

                )

            )

        return ChatResponse(

            success=True,

            response=conversation.llm.content,

            model=conversation.llm.model_used,

            latency_ms=conversation.llm.latency_ms,

            timestamp=conversation.llm.timestamp,

            sources=sources,

        )

    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc),

        )