# 🔍 AI Smart Search Engine

> Stop browsing. Start knowing.
Ask a question — get a cited, intelligent answer in seconds. No tab-switching, no skimming. Just answers.
Built with FastAPI + Google Gemini + Tavily. Streams like Perplexity. Deploys with one Docker command.

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?style=flat-square&logo=fastapi)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat-square&logo=google)
![Redis](https://img.shields.io/badge/Redis-Cloud-DC382D?style=flat-square&logo=redis)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker)

---

## ✨ Features

- **Real-time Web Search** — Powered by Tavily API, optimized for AI applications
- **AI-Generated Answers** — Google Gemini reads search results and generates cited, accurate responses
- **Streaming Responses** — Server-Sent Events (SSE) stream answers word-by-word like Perplexity
- **Redis Caching** — Repeated queries return instantly without hitting external APIs
- **Search History** — Last searches stored and retrievable via API
- **Rate Limiting** — 5 req/min on search, 3 req/min on stream (SlowAPI)
- **Clean Frontend** — Dark-themed UI with stream/normal mode toggle
- **Docker Ready** — Multi-stage build for minimal image size

---

## 🏗️ Architecture

```
User Query
    │
    ▼
┌─────────────────────────────────────┐
│           FastAPI Backend           │
│                                     │
│  Redis Cache ──► Hit? Return fast   │
│       │                             │
│       ▼ Miss                        │
│  Tavily API  ──► Web Search Results │
│       │                             │
│       ▼                             │
│  Google Gemini ──► RAG Pipeline     │
│       │                             │
│       ▼                             │
│  SSE Stream ──► Client              │
└─────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Python 3.12 |
| Web Search | Tavily API |
| LLM | Google Gemini 2.0 Flash |
| Caching | Redis Cloud |
| Streaming | Server-Sent Events (SSE) |
| Rate Limiting | SlowAPI |
| Deployment | Docker (Multi-stage) |

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/mohamedDawoood/RAG-Search-API.git
cd RAG-Search-API
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Fill in your `.env`:

```env
APP_NAME="AI Smart Search Engine"
DEBUG=False
TAVILY_API_KEY=your_tavily_key
GEMINI_API_KEY=your_gemini_key
REDIS_URL=redis://:password@host:port
```

### 3. Run with Docker

```bash
docker build -t ai-search-engine .
docker run -p 8000:8000 --env-file .env ai-search-engine
```

### 4. Or run locally

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## 📡 API Endpoints

### `POST /search/`
Standard search — returns full answer + sources.

```json
// Request
{
  "query": "What is RAG in AI?",
  "limit": 5
}

// Response
{
  "answer": "RAG (Retrieval-Augmented Generation) is...",
  "sources": [
    { "title": "...", "url": "..." }
  ]
}
```

### `POST /search/stream`
Streaming search — returns answer as SSE chunks.

```bash
curl -X POST http://localhost:8000/search/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "What is RAG?", "limit": 5}'
```

```
data: RAG stands for
data:  Retrieval-Augmented Generation...
data: [DONE]
```

### `GET /history/`
Returns last 10 search queries.

```json
{
  "searches": ["What is RAG?", "Will AI replace programmers?"],
  "total": 2
}
```

### `GET /health`
Health check endpoint.

```json
{ "status": "healthy" }
```

---

## 📁 Project Structure

```
app/
├── api/
│   ├── deps.py          # Shared dependencies
│   └── v1/
│       ├── search.py    # Search endpoints
│       └── history.py   # History endpoint
├── core/
│   └── config.py        # Settings (pydantic-settings)
├── db/
│   └── redis.py         # Redis async client
├── schemas/
│   └── search.py        # Pydantic models
├── services/
│   ├── search_service.py  # Tavily integration
│   └── llm_service.py     # Gemini integration
└── main.py              # FastAPI app + middleware
frontend/
└── index.html           # Search UI
```

---

## 🔑 API Keys

| Service | Free Tier | Link |
|---|---|---|
| Tavily | 1,000 req/month | [tavily.com](https://tavily.com) |
| Google Gemini | 1,500 req/day | [aistudio.google.com](https://aistudio.google.com) |
| Redis Cloud | 30MB free | [redis.io/cloud](https://redis.io/cloud) |

---

## 👨‍💻 Author

**Muhammed Ahmed Dawod** — AI Backend Engineer  
[GitHub](https://github.com/mohamedDawoood)

---

> Built with FastAPI + Google Gemini + Tavily — no abstraction frameworks, pure implementation.