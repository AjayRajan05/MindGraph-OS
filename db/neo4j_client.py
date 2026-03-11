from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASS

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASS)
)

def create_concept(name):

    with driver.session() as session:
        session.run(
            "MERGE (:Concept {name:$name})",
            name=name
        )

def link_concepts(a,b):

    with driver.session() as session:
        session.run(
            """
            MATCH (c1:Concept {name:$a})
            MATCH (c2:Concept {name:$b})
            MERGE (c1)-[:RELATED_TO]->(c2)
            """,
            a=a,
            b=b
        )