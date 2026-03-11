# 🧠 MindGraph OS

### *The AI Workspace That Thinks **With** You, Not Just **For** You*

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-API-green)
![Neo4j](https://img.shields.io/badge/Neo4j-Knowledge%20Graph-blue)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20Database-orange)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

MindGraph OS is an **AI-powered knowledge operating system** that transforms documents, codebases, and research into a **living knowledge graph with autonomous reasoning agents**.

Unlike traditional RAG systems that simply retrieve text, MindGraph OS **builds a temporal knowledge graph of your ideas**, tracks how your thinking evolves over time, detects contradictions, and proactively surfaces insights.

It acts as a **second brain for developers, researchers, and teams.**

---

# 🚀 Core Idea

Most AI tools work like this:

```
User Question
     ↓
Vector Search
     ↓
LLM Answer
```

MindGraph OS introduces **knowledge reasoning**:

```
Documents + Code + Notes
        ↓
Embedding Index (Qdrant)
        ↓
Knowledge Graph (Neo4j)
        ↓
Autonomous AI Agents
        ↓
Insight Generation
        ↓
Human Decision Making
```

This turns a static knowledge base into a **self organizing intelligent system**.

---

# ✨ Key Features

## 📚 Multi-Source Knowledge Ingestion

MindGraph can ingest and understand:

* PDFs
* Markdown notes
* Plain text documents
* Entire GitHub repositories
* Python codebases

It automatically extracts **concepts, relationships, and structures**.

---

## 🧩 Temporal Knowledge Graph

Every concept is stored with timestamps.

You can ask:

* *“How has my understanding of transformers evolved?”*
* *“When did this concept first appear in my research?”*
* *“What knowledge has become outdated?”*

Graph nodes store:

```
Concept
Chunk
Document
Contradiction
```

Relationships:

```
MENTIONS
RELATED_TO
INVOLVES
BELONGS_TO
```

---

## 🤖 Autonomous AI Agents

MindGraph includes background AI agents that continuously analyze your knowledge base.

### Contradiction Agent

Detects conflicting information between documents.

Example:

```
Doc A: Transformers outperform CNNs
Doc B: CNNs outperform Transformers
```

Agent flags:

```
⚠️ Knowledge Conflict Detected
```

---

### Connection Discovery Agent

Finds **hidden relationships between ideas**.

Example:

```
Graph Neural Networks
        ↕
Knowledge Graph Embeddings
```

---

### Knowledge Staleness Agent

Identifies knowledge that hasn't been updated recently.

Example:

```
Concept last updated: 92 days ago
Status: STALE
```

---

## 🧠 GraphRAG (Graph + Vector Retrieval)

Traditional RAG:

```
Vector search only
```

MindGraph uses **hybrid retrieval**:

```
Vector similarity (Qdrant)
       +
Graph traversal (Neo4j)
```

This allows **context-aware reasoning across documents**.

---

## 🧑‍💻 Codebase Intelligence

MindGraph can analyze entire GitHub repositories.

Using **tree-sitter**, it extracts:

* classes
* functions
* module structure
* imports

This enables queries like:

```
Explain this repository architecture
```

or

```
Where is authentication implemented?
```

---

## ⚡ Real-Time Insight Notifications

Background agents push insights using **WebSockets**.

Examples:

```
⚠️ Contradiction detected in research notes

🔗 New connection discovered between concepts

📉 Knowledge staleness detected
```

These insights appear instantly in the UI.

---

## 📊 Knowledge Debt Report

MindGraph can generate a **Knowledge Debt Report** summarizing:

* contradictions
* outdated knowledge
* missing conceptual connections

This helps researchers and engineers maintain **clean knowledge structures**.

---
### Feature Comparison


| Feature                      | Traditional RAG | MindGraph OS |
| :--------------------------- | :-------------: | :----------: |
| Vector Search                | ✅              | ✅           |
| Knowledge Graph              | ❌              | ✅           |
| Temporal Knowledge Tracking  | ❌              | ✅           |
| Contradiction Detection      | ❌              | ✅           |
| Autonomous Agents            | ❌              | ✅           |
| Codebase Understanding       | ❌              | ✅           |
| Real-time Knowledge Insights | ❌              | ✅           |

---

# 🏗 Architecture

```
                    Streamlit UI
                         │
                  WebSocket Updates
                         │
                       FastAPI
                         │
         ┌───────────────┼───────────────┐
         │               │               │
      Qdrant           Neo4j           Redis
   (Vector DB)     (Knowledge Graph)   (Cache)
         │
         │
      Ollama
(Local LLM + Embeddings)

Autonomous Agents

 ├── Contradiction Agent
 ├── Connection Agent
 ├── Staleness Agent
 └── Knowledge Debt Generator
```

---

# 🧰 Tech Stack

## Backend

* **FastAPI** – high-performance async API
* **Python 3.11**

## Databases

* **Qdrant** – vector database
* **Neo4j** – graph database
* **Redis** – caching and pub/sub

## AI

* **Ollama** – local LLM runtime
* **Llama3 / Mistral / Phi3**
* **nomic-embed-text** embeddings

## Code Analysis

* **tree-sitter**

## Graph Reasoning

* **LangGraph**

## Frontend

* **Streamlit**

---

# 📂 Project Structure

```
mindgraph-os
│   |
│   |── api
│   │   ├── upload.py
│   │   ├── query.py
│   │   ├── graph.py
│   │   └── ws.py
│   │
│   ├── agents
│   │   ├── contradiction_agent.py
│   │   ├── connection_agent.py
│   │   ├── staleness_agent.py
│   │   └── workflow.py
│   │
│   ├── services
│   │   ├── parser.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   ├── graph_builder.py
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   └── github_ingestor.py
│   │
│   └── db
│   |   ├── qdrant_client.py
│   |   └── neo4j_client.py
│   └── app.py
│
└── docker-compose.yml
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```
git clone https://github.com/yourusername/mindgraph-os.git

cd mindgraph-os
```

---

## 2️⃣ Install Dependencies

```
pip install -r backend/requirements.txt
```

---

## 3️⃣ Start Databases

```
docker compose up -d
```

This starts:

* Neo4j
* Qdrant
* Redis

---

## 4️⃣ Install Ollama Models

```
ollama pull llama3
ollama pull nomic-embed-text
```

---

## 5️⃣ Start Backend

```
uvicorn app.main:app --reload
```

---

## 6️⃣ Start Frontend

```
streamlit run frontend/app.py
```

---

# 💬 Example Queries

Once running, you can ask:

```
Explain this research paper
```

```
What contradictions exist in my knowledge?
```

```
Explain this GitHub repository architecture
```

```
Which concepts in my research are outdated?
```

---

# 🧪 Example Use Cases

### AI Research Assistant

Track how your understanding of topics evolves.

---

### Codebase Intelligence

Analyze large repositories with natural language.

---

### Knowledge Management

Maintain a **living knowledge graph of ideas**.

---

# 🛣 Roadmap

Planned upgrades:

* Multi-tenant collaboration
* Knowledge personas (researcher / engineer modes)
* Graph visualization with D3
* Autonomous research agents
* arXiv paper ingestion
* citation graph analysis
* real-time knowledge dashboards

---

# 🤝 Contributing

Contributions are welcome!

Steps:

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Open a pull request

Please follow clean code practices and include tests when possible.

---

# 📜 License

MIT License.

You are free to use this project for research, commercial products, or learning.

---

# 🌟 Inspiration

MindGraph OS was inspired by the idea that:

> Knowledge should not just be stored —
> it should **evolve, reason, and challenge itself**.

---

# ⭐ If You Like This Project

Please consider **starring the repository** and sharing it with others.

It helps the project grow and motivates further development.

---

**MindGraph OS — where your knowledge becomes intelligent.**
