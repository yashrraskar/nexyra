from fastapi import APIRouter
from ...schemas import ChatRequest, ChatResponse
from ...services.ai_assistant import get_ai_assistant_response

router = APIRouter(prefix="/assistant", tags=["AI Assistant"])


@router.post("/chat", response_model=ChatResponse)
def chat_with_assistant(payload: ChatRequest):
    """Answers citizen inquiries on schemes, required documents, and consent."""
    response = get_ai_assistant_response(
        query=payload.message,
        citizen_id=payload.citizen_id or "C001"
    )
    return response
