import requests
from app.config import OLLAMA_URL

def generate(context, question):

    prompt=f"""
Context:
{context}

Question:
{question}

Answer:
"""

    r=requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }
    )

    return r.json()["response"]