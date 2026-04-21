from fastapi import APIRouter
from db.neo4j_client import driver
import logging

router=APIRouter()

@router.get("/graph")

def graph():
    try:
        with driver.session() as session:
            # Get nodes with better error handling
            nodes_res=session.run(
                "MATCH (n) WHERE coalesce(n.name, n.id) IS NOT NULL RETURN DISTINCT coalesce(n.name, n.id) as name, labels(n) as labels LIMIT 100"
            )
            
            nodes=[]
            for r in nodes_res:
                if r["name"]:  # Ensure name is not None or empty
                    node_type = r["labels"][0] if r["labels"] else "Unknown"
                    nodes.append({
                        "data": {
                            "id": str(r["name"]),
                            "label": str(r["name"]),
                            "type": node_type
                        }
                    })
            
            # Get edges with better error handling
            edges_res=session.run(
                "MATCH (a)-[r]->(b) WHERE coalesce(a.name, a.id) IS NOT NULL AND coalesce(b.name, b.id) IS NOT NULL RETURN coalesce(a.name, a.id) as source, coalesce(b.name, b.id) as target, type(r) as relationship LIMIT 200"
            )
            
            edges=[]
            for r in edges_res:
                if r["source"] and r["target"]:  # Ensure both nodes exist
                    edges.append({
                        "data": {
                            "id": f"{r['source']}-{r['target']}",
                            "source": str(r["source"]),
                            "target": str(r["target"]),
                            "label": r["relationship"] or "RELATED_TO"
                        }
                    })

            # Add sample data if no data exists
            if not nodes:
                nodes = [
                    {"data": {"id": "Sample", "label": "Sample Concept", "type": "Concept"}},
                    {"data": {"id": "Document1", "label": "Document 1", "type": "Document"}}
                ]
                edges = [
                    {"data": {"id": "Sample-Document1", "source": "Sample", "target": "Document1", "label": "RELATED_TO"}}
                ]

            return {"nodes": nodes, "edges": edges}
            
    except Exception as e:
        logging.error(f"Error in graph API: {e}")
        # Return sample data on error
        return {
            "nodes": [
                {"data": {"id": "Error", "label": "Database Error", "type": "Error"}},
                {"data": {"id": "Check", "label": "Check Backend", "type": "Error"}}
            ],
            "edges": [
                {"data": {"id": "Error-Check", "source": "Error", "target": "Check", "label": "CONNECTION"}}
            ]
        }
