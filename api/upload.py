from fastapi import APIRouter, UploadFile
import uuid
import os

from app.services.parser import parse_pdf
from app.services.chunker import chunk_text
from app.services.embedder import embed
from app.db.qdrant_client import client, COLLECTION
from qdrant_client.models import PointStruct
from app.services.graph_builder import build_graph

router = APIRouter()

@router.post("/upload")

async def upload(file:UploadFile):

    path=f"/tmp/{uuid.uuid4()}.pdf"

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

    build_graph(chunks)

    return {"chunks":len(chunks)}