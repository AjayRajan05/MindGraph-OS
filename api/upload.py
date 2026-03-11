from fastapi import APIRouter, UploadFile
import uuid
import os

from services.parser import parse_pdf
from services.chunker import chunk_text
from services.embedder import embed
from db.qdrant_client import client, COLLECTION
from qdrant_client.models import PointStruct
from services.graph_builder import build_graph

router = APIRouter()

@router.post("/upload")

async def upload(file:UploadFile):

    doc_id=str(uuid.uuid4())
    path=f"{doc_id}.pdf"

    with open(path,"wb") as f:
        f.write(await file.read())

    text=parse_pdf(path)

    chunks=chunk_text(text)

    points=[]

    for chunk in chunks:

        vector=embed(chunk)

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"text":chunk}
            )
        )

    client.upsert(COLLECTION,points)

    build_graph(chunks, doc_id)

    # clean up
    if os.path.exists(path):
        os.remove(path)

    return {"chunks":len(chunks), "doc_id":doc_id}