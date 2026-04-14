from fastapi import APIRouter
from db.neo4j_client import driver

router=APIRouter()

@router.get("/graph")

def graph():

    with driver.session() as session:

        # Use a stable label for any node type: prefer `name`, fall back to `id`.
        res = session.run(
            """
            MATCH (a)-[r]->(b)
            RETURN coalesce(a.name, a.id) AS source,
                   coalesce(b.name, b.id) AS target
            """
        )

        # Build edge list, skipping any relationships where labels are missing.
        edges = [
            (record["source"], record["target"])
            for record in res
            if record["source"] is not None and record["target"] is not None
        ]

    return {"edges":edges}