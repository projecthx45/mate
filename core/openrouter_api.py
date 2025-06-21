# NOTE: For open-source model usage (e.g., Mistral, LLaMA), see the 'mate_open_llm' folder for a local LLM integration example.
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

DOTENV_PATH = Path(__file__).parent.parent / 'open.env'
if DOTENV_PATH.exists():
    load_dotenv(dotenv_path=DOTENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please add it to open.env.")

GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def call_gemini(prompt):
    """
    Call the Gemini 2.0 Flash API with the given prompt and return the response.
    Args:
        prompt (str): The prompt to send to Gemini.
    Returns:
        str: The model's response text.
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    
    with open("gemini_debug.log", "a", encoding="utf-8") as logf:
        logf.write(f"\n--- PROMPT ---\n{prompt}\n--- RESPONSE ({response.status_code}) ---\n{response.text}\n")
    if response.status_code != 200:
        raise RuntimeError(f"Gemini API error: {response.status_code} {response.text}")
    result = response.json()
    
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        raise RuntimeError(f"Unexpected Gemini API response: {result}") 