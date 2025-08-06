import requests

def reformulate_query(query: str, api_key: str, endpoint: str) -> str:
    """
    Sends a clause-related query to an LLM via API (e.g., Perplexity) to get a clarified version.
    Returns a precise, searchable version of the input query.
    """

    payload = {
        "model": "gpt-3.5-turbo",  # Replace with Perplexity's model identifier if different
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a legal assistant. Rewrite vague clause queries to be precise, "
                    "searchable, and clause-aware."
                )
            },
            {
                "role": "user",
                "content": query
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Reformulation Error] {e}")
        return query  # Fallback: return original query if anything fails