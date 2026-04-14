# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
PORT = 5000


QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

# Neo4j uses the Bolt protocol, not HTTP, for the Python driver.
# Default to bolt on the standard port; can be overridden via NEO4J_URI.
NEO4J_URI =  os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")