from datetime import datetime
import re
from app.db.neo4j_client import driver

def extract_concepts(text):

    # naive concept extraction
    words = re.findall(r"\b[A-Z][a-zA-Z]+\b", text)

    return list(set(words))


def build_graph(chunks, doc_id):

    with driver.session() as session:

        for chunk in chunks:

            concepts = extract_concepts(chunk)

            chunk_id = hash(chunk)

            session.run(
                """
                MERGE (c:Chunk {id:$cid})
                SET c.text=$text,
                    c.created_at=$time
                """,
                cid=str(chunk_id),
                text=chunk,
                time=datetime.utcnow().isoformat()
            )

            for concept in concepts:

                session.run(
                    """
                    MERGE (k:Concept {name:$name})
                    ON CREATE SET
                        k.first_seen=$time,
                        k.last_seen=$time
                    ON MATCH SET
                        k.last_seen=$time
                    """,
                    name=concept,
                    time=datetime.utcnow().isoformat()
                )

                session.run(
                    """
                    MATCH (c:Chunk {id:$cid})
                    MATCH (k:Concept {name:$name})
                    MERGE (c)-[:MENTIONS]->(k)
                    """,
                    cid=str(chunk_id),
                    name=concept
                )