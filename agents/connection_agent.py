from db.neo4j_client import driver

def find_connections():

    with driver.session() as session:

        result=session.run(
        """
        MATCH (a:Concept),(b:Concept)
        WHERE a<>b
        AND NOT (a)-[:RELATED_TO]->(b)
        RETURN a.name,b.name
        LIMIT 20
        """
        )

        return [(r["a.name"],r["b.name"]) for r in result]