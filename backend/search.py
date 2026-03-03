"""
FAISS-based semantic search engine using sentence-transformers.
"""

import time
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from database import SessionLocal
from crud import fetch_all_subtopics, fetch_videos_for_subtopics


MODEL_NAME = "all-MiniLM-L6-v2"  # fast, lightweight, great quality

_model: SentenceTransformer | None = None
_index: faiss.IndexFlatIP | None = None
_subtopics: list[dict] = []


def _normalize(vectors: np.ndarray) -> np.ndarray:
    """L2-normalize row vectors for cosine similarity via inner product."""
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1e-10, norms)
    return vectors / norms


def build_index() -> None:
    """Load model, open DB connection, and build FAISS index from SubTopics."""
    global _model, _index, _subtopics

    print(f"[search] Loading model '{MODEL_NAME}' ...")
    _model = SentenceTransformer(MODEL_NAME)

    print("[search] Fetching subtopics from SQL Server...")
    _subtopics = fetch_all_subtopics()

    if not _subtopics:
        print("[search] WARNING: No subtopics found or DB connection failed. Index will be empty.")
        return

    texts = [s["text"] for s in _subtopics]
    print(f"[search] Encoding {len(texts)} subtopics ...")
    embeddings = _model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    embeddings = _normalize(embeddings.astype("float32"))

    dim = embeddings.shape[1]
    _index = faiss.IndexFlatIP(dim)  # Inner product = cosine after normalization
    _index.add(embeddings)
    print(f"[search] FAISS index built: {_index.ntotal} vectors, dim={dim}")


def semantic_search(query: str, top_k: int = 5) -> tuple[list[dict], float]:
    """
    Semantic search flow:
      1. Encode query to a dense vector.
      2. Search FAISS for top_k nearest SubTopics (by cosine similarity).
      3. Fetch all Videos from LMSVideoContents whose SubTopicID matched.
      4. Attach the subtopic's similarity score to each video.
      5. Return videos sorted by score descending.
    """
    if _model is None or _index is None:
        raise RuntimeError("Search index not ready. Call build_index() first.")

    t0 = time.perf_counter()

    # Step 1 + 2: encode query, search FAISS
    q_vec = _model.encode([query], convert_to_numpy=True)
    q_vec = _normalize(q_vec.astype("float32"))
    scores, indices = _index.search(q_vec, top_k)

    # Step 3: build a map  SubTopicID -> {text, score}
    # _subtopics[idx] = {"id": SubTopicID, "text": SubTopic}
    matched: dict[int, dict] = {}
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue
        st = _subtopics[idx]
        matched[st["id"]] = {
            "subtopic_text": st["text"],
            "score": round(float(score), 4),
        }

    elapsed_ms = (time.perf_counter() - t0) * 1000

    if not matched:
        return [], round(elapsed_ms, 2)

    # Step 4: fetch videos from DB for matched subtopic IDs
    videos = fetch_videos_for_subtopics(list(matched.keys()))

    # Step 5: merge and sort
    # video keys from DB: vc_id, subtopic_id, caption, file_name, thumbnail
    results = []
    for vid in videos:
        s_id = vid["subtopic_id"]
        m = matched.get(s_id)
        if m is None:
            continue
        results.append({
            "vc_id":       vid["vc_id"],
            "subtopic_id": s_id,
            "subtopic":    m["subtopic_text"],
            "caption":     vid["caption"],
            "file_name":   vid["file_name"],
            "thumbnail":   vid["thumbnail"],
            "score":       m["score"],
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results, round(elapsed_ms, 2)
