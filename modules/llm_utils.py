import requests
import os
from config import PERPLEXITY_ENDPOINT, LLM_MODEL

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

def query_llm(prompt):
    if not PERPLEXITY_API_KEY:
        return "⚠️ Missing API credentials"

    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(PERPLEXITY_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {e}"

def rewrite_clause(clause_text):
    prompt = f"Simplify the following legal clause:\n\"{clause_text}\""
    return query_llm(prompt)

def generate_negotiation_tip(clause_text):
    prompt = f"What should someone consider negotiating in this clause?\n\"{clause_text}\""
    return query_llm(prompt)

