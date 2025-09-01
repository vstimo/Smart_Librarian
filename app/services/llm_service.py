# app/services/llm_service.py
import json
from typing import List, Dict, Any, Optional
from app.config import client, OPENAI_MODEL, SYSTEM_PROMPT
from app.utils.tools import get_full_summary, openai_tool_def

def recommend_and_summarize(query: str, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Returnează dict cu cheile:
      - ok: bool
      - message: str (răspunsul final pentru UI)
      - title: Optional[str] (titlul ales)
      - candidates: lista originală pt. UI/debug
    """

    context = {
        "query": query,
        "candidates": [{"title": c["title"], "summary": c["summary"][:400]} for c in candidates],
    }

    # Mesajele initiale folosite la primul apel
    base_messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': f"User query: {query}"},
        {'role': 'assistant', 'content': 'Here are the top RAG candidates:'},
        {'role': 'user', 'content': json.dumps(context)}
    ]

    # Primul apel - modelul decide ce titlu sa aleaga si cere tool-ul cu argumentele potrivite pt aceasta
    response = client.chat.completions.create(
        model = OPENAI_MODEL,
        tools = [openai_tool_def],
        tool_choice = "auto",
        messages = base_messages,
        temperature=0.3
    )

    # Verificam daca modelul a apelat tool-ul get_summary_by_title
    msg = response.choices[0].message
    tool_calls = getattr(msg, "tool_calls", None)
    # Daca nu a folosit tool_call, returneaza continul direct
    if not tool_calls:
        return {
            "ok": True,
            "message": msg.content or "No response from model.",
            "title": None,
            "candidates": candidates
        }
    
    picked_title: Optional[str] = None
    final_message: Optional[str] = None

    for tc in tool_calls: # doar un tool este apelat
        if tc.type == 'function' and tc.function.name == 'get_summary_by_title':
            args = json.loads(tc.function.arguments or '{}')
            picked_title = args.get('title')
            full = get_full_summary(picked_title)

            # IMPORTANT: In al doilea apel includem: istoricul initial, mesaj de assitant si raspunsul tool-ului
            follow_messages = [
                *base_messages,
                {
                    'role': 'assistant',
                    'content': msg.content,
                    'tool_calls': tool_calls
                },
                {
                    'role': 'tool',
                    'tool_call_id': tc.id,
                    'name': tc.function.name,
                    'content': full
                }
            ]

            # Al doilea apel - compune raspunsul final pentru user folosind rezultatul tool-ului
            follow_resp = client.chat.completions.create(
                model = OPENAI_MODEL,
                tools = [openai_tool_def],
                messages = follow_messages,
                temperature=0.2
            )
            final_message = follow_resp.choices[0].message.content
            break

        if final_message is None:
            final_message = msg.content or "No response from model."

    return {
        'ok': True,
        'message': final_message,
        'title': picked_title,
        'candidates': candidates
    }