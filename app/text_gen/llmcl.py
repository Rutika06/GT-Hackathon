# app/text_gen/llmcl.py
import google.generativeai as genai
from app.conf import settings

def _get_client():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set. Add it to the .env file.")
    genai.configure(api_key=api_key)
    return genai

def generate_insights(prompt: str) -> str:
    client = _get_client()

    model = client.GenerativeModel("models/gemini-2.5-flash")  # ← using available model

    response = model.generate_content(prompt)
    return response.text
