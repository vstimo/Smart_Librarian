# app/services/moderation_service.py
from app.utils.moderation import is_offensive

def is_message_offensive(message: str) -> bool:
    return is_offensive(message or "")