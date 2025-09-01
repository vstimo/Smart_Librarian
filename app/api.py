# app/api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models import ChatRequest, ChatResponse
from app.chat_controller import handle_chat
from app.services.rag_service import ensure_collection_ready

app = FastAPI(title="Smart Librarian API", version="1.0.0")

# CORS pentru React (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    ensure_collection_ready()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(body: ChatRequest):
    resp = handle_chat(ChatRequest(query=body.query))
    return ChatResponse(ok=resp.ok, message=resp.message, title=resp.title, candidates=resp.candidates)