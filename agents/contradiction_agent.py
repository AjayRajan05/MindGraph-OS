from db.qdrant_client import client, COLLECTION
from services.embedder import embed
import requests

OLLAMA="http://localhost:11434/api/generate"


def check_contradiction(a,b):

    prompt=f"""
Do these two statements contradict each other?

Statement A:
{a}

Statement B:
{b}

Answer YES or NO and explain.
"""

    r=requests.post(
        OLLAMA,
        json={
            "model":"llama3",
            "prompt":prompt,
            "stream":False
        }
    )

    return r.json()["response"]


def run_contradiction_scan(new_chunk):

    vec=embed(new_chunk)

    results=client.search(
        collection_name=COLLECTION,
        query_vector=vec,
        limit=10
    )

    contradictions=[]

    for r in results:

        old=r.payload["text"]

        response=check_contradiction(new_chunk,old)

        if "YES" in response.upper():

            contradictions.append({
                "old":old,
                "new":new_chunk,
                "reason":response
            })

    return contradictions