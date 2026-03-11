from fastapi import APIRouter
from db.neo4j_client import driver

router=APIRouter()

@router.get("/graph")

def graph():

    with driver.session() as session:

        res=session.run(
            "MATCH (a)-[r]->(b) RETURN a.name,b.name"
        )

        edges=[(r["a.name"],r["b.name"]) for r in res]

    return {"edges":edges}