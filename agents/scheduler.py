import time

from agents.connection_agent import find_connections
from agents.staleness_agent import find_stale_concepts

def run_agents():

    while True:

        print("Running connection agent")

        connections=find_connections()

        print("Potential connections:",connections)

        print("Running staleness agent")

        stale=find_stale_concepts()

        print("Stale concepts:",stale)

        time.sleep(600)