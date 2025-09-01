# app/chat_controller.py

from app.models import ChatRequest, ChatResponse
from app.services.moderation_service import is_offensive
from app.services.rag_service import get_candidates
from app.services.llm_service import recommend_and_summarize

def handle_chat(request: ChatRequest) -> ChatResponse:
    query = (request.query or "").strip()

    if not query:
        return ChatResponse(ok=False, message="Query is empty.")
    
    if is_offensive(query):
        return ChatResponse(ok=False, message="Atentie with the language cu mine. Try again.")

    candidates = get_candidates(query, 5)

    result = recommend_and_summarize(query, candidates)
    return ChatResponse(
        ok=result["ok"],
        message=result["message"],
        title=result.get("title"),
        candidates=result.get("candidates")
    )