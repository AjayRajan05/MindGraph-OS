import requests
from config import OLLAMA_URL


def generate(context, question):

    prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""

    try:

        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        # Raise for HTTP errors (4xx / 5xx) so we can surface a clear message.
        r.raise_for_status()

        data = r.json()

        # Ollama responses should contain a "response" field; fall back if missing.
        return data.get("response", "[Generation error: missing 'response' field from Ollama]")

    except requests.Timeout:
        return "[Generation error: Ollama request timed out]"

    except requests.RequestException as e:
        # Network / HTTP-level problems when talking to Ollama.
        return f"[Generation error: could not reach Ollama server: {e}]"

    except ValueError as e:
        # JSON decoding issues (invalid / non-JSON response).
        snippet = r.text[:200] if 'r' in locals() else ""
        return f"[Generation error: invalid JSON from Ollama: {e}. Raw response: {snippet}]"