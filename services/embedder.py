import requests
from config import OLLAMA_URL

MODEL="nomic-embed-text"

def embed(text):

    r = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={
            "model":MODEL,
            "prompt":text
        }
    )

    return r.json()["embedding"]