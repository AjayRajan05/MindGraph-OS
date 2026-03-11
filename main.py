from fastapi import FastAPI

from api.upload import router as upload_router
from api.query import router as query_router
from api.graph import router as graph_router

from db.qdrant_client import init_collection

app=FastAPI()

init_collection()

app.include_router(upload_router)
app.include_router(query_router)
app.include_router(graph_router)