"""
Chat Endpoint for Digital Twin API.

Provides POST route for conversational turns and GET route for browser status inspection.
"""

from fastapi import APIRouter, HTTPException
from backend.core.container import container
from backend.services.models import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.get("")
def chat_info():
    """
    GET handler providing endpoint usage instructions when accessed via browser URL bar.
    """
    return {
        "status": "online",
        "endpoint": "/api/chat",
        "method": "POST",
        "message": "Send a POST request with JSON body to chat with the Andrew Ng Digital Twin.",
        "sample_payload": {
            "session_id": "demo_session_123",
            "message": "Hi Andrew! Tell me about machine learning.",
            "user_id": "default_user"
        }
    }


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Executes a single multi-turn chat interaction with the Andrew Ng Digital Twin.
    """
    try:
        response = container.conversation_service.chat(
            session_id=request.session_id,
            message=request.message,
            user_id=request.user_id or "default_user",
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))