# config.py
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = True
PORT = 5000


QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

NEO4J_URI =  os.getenv("NEO4J_URI", "http://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASS = os.getenv("NEO4J_PASS", "password")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")