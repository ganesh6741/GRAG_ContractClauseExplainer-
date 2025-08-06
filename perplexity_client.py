import os
import json
import requests
import streamlit as st
from config import EXPLANATION_CACHE_PATH

# 📦 Retrieve API key securely from Streamlit secrets or environment
API_KEY = (
    st.secrets.get("perplexity", {}).get("api_key")
    or os.getenv("PERPLEXITY_API_KEY")
)

# ⚠️ Graceful fallback if key is missing
if not API_KEY:
    st.error("🚨 Perplexity API key is missing!")

ENDPOINT = "https://api.perplexity.ai/chat/completions"


def _load_cache() -> dict:
    """
    Load cached explanations from JSON file.
    Returns an empty dict if cache file does not exist.
    """
    if os.path.exists(EXPLANATION_CACHE_PATH):
        with open(EXPLANATION_CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(cache: dict):
    """
    Persist the cache dict to disk at EXPLANATION_CACHE_PATH.
    Creates parent directories if needed.
    """
    os.makedirs(os.path.dirname(EXPLANATION_CACHE_PATH), exist_ok=True)
    with open(EXPLANATION_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def explain_with_perplexity(clause: str) -> str:
    """
    Check the persistent cache first. If the clause is not cached,
    call Perplexity API, cache the result, and return the explanation.
    """
    cache = _load_cache()
    if clause in cache:
        return cache[clause]

    # 🔧 Compose prompt
    full_prompt = f"""As a legal expert, break down this contract clause for a non-lawyer, ensuring every term is fully explained in plain English.

Clause:
{clause}

Explanation:"""

    # 🎯 Construct API request
    payload = {
        "model": "sonar-pro",
        "messages": [{"role": "user", "content": full_prompt}],
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # 📡 Send request
    response = requests.post(ENDPOINT, headers=headers, json=payload)

    # 📨 Parse response
    if response.status_code == 200:
        explanation = response.json()["choices"][0]["message"]["content"].strip()
        # Cache and return
        cache[clause] = explanation
        _save_cache(cache)
        return explanation
    else:
        st.error(f"⚠️ Error {response.status_code}: {response.text}")
        return "Something went wrong while contacting Perplexity."


