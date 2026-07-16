"""
Chat API endpoint.
"""

from fastapi import APIRouter, HTTPException

from backend.core.container import container

from backend.llm.models import (
    LLMRequest,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)



@router.post("")
async def chat(
    request: LLMRequest
):

    try:

        response = (
            container
            .gemini
            .generate(request)
        )


        return {

            "success": True,

            "response":
                response.content,

            "model":
                response.model_used,

            "latency_ms":
                response.latency_ms,

            "timestamp":
                response.timestamp,

        }


    except Exception as exc:

        raise HTTPException(

            status_code=500,

            detail=str(exc)

        )