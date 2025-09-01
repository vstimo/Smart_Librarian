# app/config.py
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(filename=".env", usecwd=True), override=True)

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = OpenAI()

SYSTEM_PROMPT = (
    "You are Smart Librarian. You recommend ONE book from the provided candidates. "
    "Explain briefly why it matches the user's interests, then call the tool with the exact title."
)