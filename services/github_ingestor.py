import os
import git

from services.code_parser import parse_code
from services.embedder import embed
from db.qdrant_client import client, COLLECTION
from qdrant_client.models import PointStruct
import uuid


def clone_repo(repo_url):

    path = f"/tmp/{uuid.uuid4()}"

    git.Repo.clone_from(repo_url, path)

    return path


def analyze_repo(repo_url):

    path = clone_repo(repo_url)

    points = []

    for root, dirs, files in os.walk(path):

        for file in files:

            if file.endswith(".py"):

                fp = os.path.join(root, file)

                with open(fp) as f:
                    code = f.read()

                structure = parse_code(code)

                embedding = embed(code)

                points.append(
                    PointStruct(
                        id=str(uuid.uuid4()),
                        vector=embedding,
                        payload={
                            "text": code,
                            "file": file,
                            "functions": structure["functions"],
                            "classes": structure["classes"]
                        }
                    )
                )

    client.upsert(COLLECTION, points)

    return {"files_indexed": len(points)}