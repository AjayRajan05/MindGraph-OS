from fastapi import APIRouter, HTTPException
from services.retriever import retrieve
from services.generator import generate

router=APIRouter()

@router.post("/query")

def query(q:str):

    chunks=retrieve(q)

    context="\n".join(chunks)

    answer = generate(context, q)

    if answer.startswith("[Generation error"):
        raise HTTPException(status_code=502, detail=answer)

    return {"answer": answer}