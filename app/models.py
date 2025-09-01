# app/models.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

@dataclass
class ChatRequest:
    query: str

@dataclass
class ChatResponse:
    ok: bool
    message: str
    title: Optional[str] = None
    candidates: Optional[List[Dict[str, Any]]] = None