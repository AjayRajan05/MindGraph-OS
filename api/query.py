from fastapi import APIRouter
from app.services.retriever import retrieve
from app.services.generator import generate

router=APIRouter()

@router.post("/query")

def query(q:str):

    chunks=retrieve(q)

    context="\n".join(chunks)

    answer=generate(context,q)

    return {"answer":answer}