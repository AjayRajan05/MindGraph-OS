from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import QDRANT_URL

COLLECTION = "mindgraph"

client = QdrantClient(url=QDRANT_URL)

def init_collection():

    if COLLECTION not in [c.name for c in client.get_collections().collections]:

        client.create_collection(
            collection_name=COLLECTION,
            vectors_config=VectorParams(size=768, distance=Distance.COSINE)
        )