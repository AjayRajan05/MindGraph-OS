from db.qdrant_client import client,COLLECTION
from services.embedder import embed
from db.neo4j_client import driver

def retrieve(query):

    vec=embed(query)

    results=client.search(
        collection_name=COLLECTION,
        query_vector=vec,
        limit=5
    )

    chunks=[r.payload["text"] for r in results]

    graph_context=[]

    with driver.session() as session:

        res=session.run(
        """
        MATCH (c:Concept)
        RETURN c.name
        LIMIT 20
        """
        )

        graph_context=[r["c.name"] for r in res]

    return chunks+graph_context