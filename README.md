# Semantic Search Demo

> FAISS-backed semantic search with React + Vite + TypeScript frontend and FastAPI + sentence-transformers backend.

```
d:\SemanticSearch\
├── backend/   ← FastAPI + FAISS + sentence-transformers
└── frontend/  ← React 18 + Vite + TypeScript
```

---

## Quick Start

### 1 — Backend

```powershell
cd d:\SemanticSearch\backend

# Create & activate virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server (port 8000)
uvicorn main:app --reload --port 8000
```

On first run the model (`all-MiniLM-L6-v2`, ~80 MB) will be downloaded automatically.

**API Endpoints**

| Method | Path       | Description                        |
|--------|------------|------------------------------------|
| GET    | `/health`  | Liveness check                     |
| POST   | `/search`  | Semantic search (JSON body below)  |
| GET    | `/corpus`  | List all 30 demo documents         |

**POST /search body**
```json
{ "query": "deep learning vision models", "top_k": 5 }
```

---

### 2 — Frontend

```powershell
cd d:\SemanticSearch\frontend

# Install dependencies (only needed once)
npm install

# Start dev server (port 5173)
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Tech Stack

| Layer    | Technology |
|----------|-----------|
| Embeddings | `sentence-transformers` — all-MiniLM-L6-v2 |
| Vector Index | Facebook AI — FAISS (IndexFlatIP, cosine) |
| Backend API | FastAPI + uvicorn |
| Frontend | React 18 + Vite + TypeScript |
| HTTP Client | Axios |
| Icons | lucide-react |

---

## Architecture

```
Browser
  │
  ├─ POST /search ──────────────► FastAPI (port 8000)
  │    { query, top_k }               │
  │                                   ├─ SentenceTransformer.encode(query)
  │                                   ├─ FAISS.search(q_vec, top_k)
  │                                   └─ Return ranked results + score
  │
  └─ Render ResultCard[] ◄─────── [ {title, text, score}, … ]
```

Scores are cosine similarities in \[0, 1\]. A score ≥ 0.70 is shown in green, ≥ 0.45 in aquamarine, and below in blue.
