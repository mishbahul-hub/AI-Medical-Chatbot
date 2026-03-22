# 🏥 AI Medical Chatbot

> A Retrieval-Augmented Generation (RAG) powered medical chatbot that answers clinical questions by intelligently querying domain-specific medical documents.

![Python](https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&logo=python&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=flat-square)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [How It Works](#-how-it-works)
- [Knowledge Base](#-knowledge-base)
- [API Reference](#-api-reference)
- [Known Issues](#-known-issues)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🔍 Overview

The **AI Medical Chatbot** is an intelligent, document-grounded conversational assistant built on a Retrieval-Augmented Generation (RAG) pipeline. It processes structured medical literature (currently focused on **Diabetes**), converts the content into vector embeddings, and enables users to ask natural-language questions that are answered with clinically accurate, source-backed responses.

This project bridges the gap between complex medical documentation and patient-friendly accessibility — providing instant, context-aware answers rather than generic web search results.

---

## ✨ Features

- 📄 **Document Ingestion** — Processes medical PDFs and chunks them into semantically meaningful segments
- 🧠 **Embedding Generation** — Converts text chunks into dense vector representations for similarity search
- 🔎 **Semantic Retrieval** — Retrieves the most relevant document passages in response to user queries
- 💬 **Conversational Interface** — Clean, responsive chat UI for seamless interaction
- 🏥 **Domain-Specific Focus** — Grounded in trusted medical documents (Diabetes knowledge base included)
- ⚡ **Fast Responses** — Low-latency query pipeline designed for real-time interaction
- 🌐 **Full-Stack Application** — Decoupled Python backend and JavaScript frontend

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface (Frontend)                │
│                     HTML · CSS · JavaScript                     │
└─────────────────────────┬───────────────────────────────────────┘
                          │  HTTP / REST API
┌─────────────────────────▼───────────────────────────────────────┐
│                      Python Backend (API)                       │
│                                                                 │
│  ┌──────────────┐    ┌───────────────┐    ┌──────────────────┐  │
│  │  PDF Loader  │───▶│  Text Chunker │───▶│ Embedding Model  │  │
│  └──────────────┘    └───────────────┘    └────────┬─────────┘  │
│                                                    │            │
│  ┌──────────────────────────────────────────────────▼─────────┐ │
│  │                    Vector Store (ChromaDB / FAISS)         │ │
│  └──────────────────────────────────────────────────┬─────────┘ │
│                                                    │            │
│  ┌─────────────────┐    ┌─────────────────────────▼──────────┐  │
│  │   LLM (OpenAI / │◀───│    RAG Chain (Query + Retrieval)   │  │
│  │   Local Model)  │    └────────────────────────────────────┘  │
│  └────────┬────────┘                                            │
└───────────┼─────────────────────────────────────────────────────┘
            │
            ▼
     Grounded Medical Response
```

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.13+, FastAPI / Flask |
| **AI / ML** | LangChain, OpenAI API / Hugging Face, Sentence Transformers |
| **Vector Store** | ChromaDB / FAISS |
| **PDF Processing** | PyMuPDF / PyPDF2 |
| **Frontend** | JavaScript (ES6+), HTML5, CSS3 |
| **Notebook** | Jupyter Notebook (prototyping & evaluation) |
| **Package Manager** | uv / pip |

---

## 📁 Project Structure

```
AI-Medical-Chatbot/
├── backend/                    # Python backend service
│   ├── api/                    # API route handlers
│   ├── rag/                    # RAG pipeline (loader, chunker, retriever)
│   ├── embeddings/             # Embedding generation logic
│   ├── vector_store/           # Vector DB integration
│   └── models/                 # Data models / schemas
│
├── frontend/                   # Web UI
│   ├── index.html              # Entry point
│   ├── style.css               # Stylesheet
│   └── app.js                  # Chat interface logic
│
├── DIABETES.pdf                # Sample medical knowledge base
├── main.py                     # Application entry point
├── pyproject.toml              # Project metadata & dependencies
├── .python-version             # Python version pin (3.13)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- **Python 3.13+** — [Download](https://www.python.org/downloads/)
- **Node.js** (optional, for frontend tooling) — [Download](https://nodejs.org/)
- **uv** (recommended) or `pip` for Python package management
  ```bash
  curl -Ls https://astral.sh/uv/install.sh | sh
  ```
- An **OpenAI API key** (or a compatible local LLM setup)

---

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/mishbahul-hub/AI-Medical-Chatbot.git
cd AI-Medical-Chatbot
```

**2. Create and activate a virtual environment**

Using `uv` (recommended):
```bash
uv venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows
```

Using standard `venv`:
```bash
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies**

```bash
uv pip install -r requirements.txt
# or
pip install -r requirements.txt
```

---

### Configuration

Create a `.env` file in the project root:

```env
# LLM Provider
OPENAI_API_KEY=your_openai_api_key_here

# Embedding Model (optional override)
EMBEDDING_MODEL=text-embedding-ada-002

# Vector Store Path
VECTOR_STORE_PATH=./vector_store

# Backend Server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

### Running the Application

**1. Ingest and embed the knowledge base**

```bash
python backend/rag/ingest.py --source DIABETES.pdf
```

**2. Start the backend server**

```bash
python main.py
# or
uvicorn backend.api.main:app --reload --host 0.0.0.0 --port 8000
```

**3. Open the frontend**

Open `frontend/index.html` in your browser, or serve it locally:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Then navigate to `http://localhost:3000`.

---

## ⚙️ How It Works

The chatbot follows a standard **RAG pipeline** in four stages:

**Stage 1 — Document Loading**
The medical PDF (`DIABETES.pdf`) is loaded and parsed into raw text using a PDF reader.

**Stage 2 — Text Chunking**
The raw text is split into overlapping chunks (e.g., 500 tokens with a 50-token overlap) to preserve context across boundaries.

**Stage 3 — Embedding & Indexing**
Each chunk is passed through an embedding model to produce a high-dimensional vector. These vectors are stored in a local vector database (ChromaDB or FAISS) for fast similarity search.

**Stage 4 — Query & Generation**
When a user sends a question:
1. The query is embedded using the same model.
2. The top-k most similar document chunks are retrieved.
3. The retrieved context + user query are passed to an LLM.
4. The LLM generates a grounded, accurate response.

---

## 📚 Knowledge Base

The current knowledge base includes:

| Document | Topic | Source |
|----------|-------|--------|
| `DIABETES.pdf` | Diabetes — diagnosis, symptoms, treatment, management | Bundled |

To add more documents, place them in the project root (or a designated `docs/` folder) and re-run the ingestion script:

```bash
python backend/rag/ingest.py --source path/to/your_document.pdf
```

---

## 📡 API Reference

### `POST /api/chat`

Send a user message and receive a grounded medical response.

**Request Body:**
```json
{
  "message": "What are the early symptoms of Type 2 diabetes?",
  "session_id": "optional-session-id"
}
```

**Response:**
```json
{
  "response": "Early symptoms of Type 2 diabetes include...",
  "sources": ["DIABETES.pdf — Page 12", "DIABETES.pdf — Page 34"],
  "session_id": "optional-session-id"
}
```

---

### `GET /api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "vector_store": "loaded",
  "documents_indexed": 142
}
```

---

## 🐛 Known Issues

| Issue | Status | Notes |
|-------|--------|-------|
| Embeddings not generated correctly | 🔴 Active | Vector store produces malformed embeddings; under investigation |
| Session memory not persisted | 🟡 Planned | Conversational context resets between sessions |
| Single-document knowledge base | 🟡 Planned | Only `DIABETES.pdf` is currently supported |

> If you encounter any bugs, please [open an issue](https://github.com/mishbahul-hub/AI-Medical-Chatbot/issues) with reproduction steps.

---

## 🗺 Roadmap

- [x] Project scaffolding (backend + frontend)
- [x] PDF document ingestion
- [ ] Fix embedding generation pipeline
- [ ] Integrate vector store (ChromaDB / FAISS)
- [ ] Complete RAG chain with LLM
- [ ] Conversational memory (multi-turn chat)
- [ ] Expand knowledge base (multiple medical PDFs)
- [ ] Authentication & user sessions
- [ ] Docker containerization
- [ ] Deployment (cloud / self-hosted)

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages.

---

## ⚠️ Disclaimer

> **This application is intended for educational and informational purposes only.** It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions you may have regarding a medical condition. Never disregard professional medical advice based on information provided by this chatbot.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ by <a href="https://github.com/mishbahul-hub">mishbahul-hub</a></sub>
</div>
