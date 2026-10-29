<div align="center">

# 🤖 Gobber

### Production-Ready Multi-Agent AI System

An advanced AI backend that autonomously generates, executes, and learns from Python code using LangGraph, Docker, and RAG.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-FF9900?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-FF4F00?style=for-the-badge&logo=qdrant&logoColor=white)](https://qdrant.tech/)

<br>

<a href="https://github.com/Abdallahmoha277/Gobber-">
  <img src="https://img.shields.io/badge/🚀_Live_Demo-Coming_Soon-blue?style=for-the-badge&logo=vercel&logoColor=white" alt="Live Demo" />
</a>
<br>
<i>(API Documentation will be available here upon deployment)</i>
<br><br>

</div>

---

## 📖 About the Project

**Gobber** is a production-ready Multi-Agent AI backend designed to automate software development tasks. It receives user queries, routes them to specialized AI agents, generates Python code, and executes it securely in an isolated environment. 

What makes Gobber unique is its ability to **learn from its own executions** (RAG) and its full **observability stack** to monitor performance and latency.

---

## ✨ Key Features

- 🧠 **Multi-Agent Workflow (LangGraph):** Uses a state machine to orchestrate specialized agents (Router, Coder, Responder).
- 🛡️ **Secure Code Execution (Docker Sandbox):** AI-generated code runs safely in an isolated Docker container with strict resource limits to prevent malicious activity.
- 🔍 **Semantic Memory (RAG):** Uses Qdrant Vector DB and Hugging Face embeddings to remember past successful code executions and reuse them for similar future tasks.
- 📊 **Observability:** Fully instrumented with Prometheus and Grafana to monitor API latency, request counts, and system health.
- 🔐 **Authentication:** Secure REST API using JWT (JSON Web Tokens) and bcrypt password hashing.

---

## 🏗️ System Architecture

```text
User Request
    │
    ▼
┌─────────────┐
│   Router    │ ──(Decides the best path)
└──────┬──────┘
       │
       ├───▶ (If Code Task) ──▶ 1. RAG Memory Search (Qdrant)
       │                         2. Coder Agent (DeepSeek LLM)
       │                         3. Executor (Docker Sandbox)
       │                         4. Save to Memory (Background)
       │
       └───▶ (If General QA) ──▶ Responder Agent (DeepSeek LLM)

---

```

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **AI & Orchestration:** LangChain, LangGraph, DeepSeek API, Hugging Face
- **Databases & Caching:** PostgreSQL (SQLAlchemy), Qdrant (Vector DB), Redis
- **DevOps & Security:** Docker, Docker Compose, JWT, Passlib
- **Observability:** Prometheus, Grafana

---

## 🚀 Quick Start (Local Setup)

### 1. Prerequisites
- Docker & Docker Compose installed.
- A `.env` file with your API keys (see below).

### 2. Environment Variables
Create a `.env` file in the root directory:

```env
DEEPSEEK_API_KEY="sk-your-deepseek-key"
DATABASE_URL="postgresql://admin:secretpassword@localhost:5432/gobber_db"
REDIS_URL="redis://localhost:6379/0"
```

### 3. Run the Application
```bash
git clone https://github.com/Abdallahmoha277/Gobber-.git
cd Gobber-
docker compose up -d
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. Access the API
- **Swagger UI:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/api/v1/health/db`
- **Prometheus:** `http://localhost:9090`
- **Grafana:** `http://localhost:3000` (admin / admin)

---

## 🧪 Testing

To run the automated test suite:

```bash
pytest tests/ -v
```

---

## 👨‍💻 Author

**Abdallah Mohammed**

- [LinkedIn](https://www.linkedin.com/in/abdallah-mohammed-80a58a216/)
- [GitHub](https://github.com/Abdallahmoha277)

---

⭐ *If you find this project interesting, feel free to star the repository!*
```.
