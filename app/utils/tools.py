import json
from pathlib import Path

FULL = json.loads(Path("app/data/full_summaries.json").read_text(encoding="utf-8"))

def get_full_summary(title: str) -> str:
    # Returneaza rezumatul complet pentru un titlu dat
    return FULL.get(title, f"No full summary found for '{title}'")

openai_tool_def = {
  "type": "function",
  "function": {
    "name": "get_summary_by_title",
    "description": "Return the full summary for the exact book title.",
    "parameters": {
      "type": "object",
      "properties": { "title": { "type": "string" } },
      "required": ["title"],
      "additionalProperties": False
    },
  },
}