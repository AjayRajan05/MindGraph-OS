from fastapi import APIRouter
from db.neo4j_client import driver

router=APIRouter()

@router.get("/graph")

def graph():

    with driver.session() as session:
        # Get nodes
        nodes_res=session.run(
            "MATCH (n) RETURN DISTINCT n.name as name, labels(n) as labels"
        )
        
        nodes=[]
        for r in nodes_res:
            node_type = r["labels"][0] if r["labels"] else "Unknown"
            nodes.append({
                "data": {
                    "id": r["name"],
                    "label": r["name"],
                    "type": node_type
                }
            })
        
        # Get edges
        edges_res=session.run(
            "MATCH (a)-[r]->(b) RETURN a.name as source, b.name as target, type(r) as relationship"
        )
        
        edges=[]
        for r in edges_res:
            edges.append({
                "data": {
                    "id": f"{r['source']}-{r['target']}",
                    "source": r["source"],
                    "target": r["target"],
                    "label": r["relationship"] or "RELATED_TO"
                }
            })

    return {"nodes": nodes, "edges": edges}