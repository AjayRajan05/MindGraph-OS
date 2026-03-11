from datetime import datetime,timedelta
from db.neo4j_client import driver

THRESHOLD_DAYS=30

def find_stale_concepts():

    cutoff=datetime.utcnow()-timedelta(days=THRESHOLD_DAYS)

    with driver.session() as session:

        res=session.run(
        """
        MATCH (c:Concept)
        WHERE datetime(c.last_seen) < datetime($cutoff)
        RETURN c.name
        """,
        cutoff=cutoff.isoformat()
        )

        return [r["c.name"] for r in res]