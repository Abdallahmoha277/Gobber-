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
