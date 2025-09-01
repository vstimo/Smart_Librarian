# app/services/rag_service.py
from typing import List, Dict, Any
from app.utils.rag_store import retrieve_candidates, ingest_if_needed

def ensure_collection_ready() -> int:
    return ingest_if_needed(force=False)

def get_candidates(query: str, n: int = 5) -> List[Dict[str, Any]]:
    return retrieve_candidates(query, n)