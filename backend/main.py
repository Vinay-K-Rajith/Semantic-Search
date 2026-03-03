"""
FastAPI application entry point for the Semantic Search demo.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import SearchRequest, SearchResponse, VideoResult
from search import build_index, semantic_search


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Build the FAISS index once on startup."""
    build_index()
    yield


app = FastAPI(
    title="Semantic Search API",
    description="FAISS-backed semantic search using sentence-transformers (all-MiniLM-L6-v2)",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow all origins for the local demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# CloudFront base URL for thumbnails
THUMBNAIL_BASE_URL = "https://d1vhmuhlcbqf8v.cloudfront.net/Images/StudentPortal/VideoThumbNail"


def build_thumbnail_url(filename: str) -> str:
    """Construct CloudFront URL for a thumbnail."""
    if not filename:
        return ""
    return f"{THUMBNAIL_BASE_URL}/{filename}"


@app.get("/health", tags=["status"])
async def health():
    """Liveness check."""
    return {"status": "ok", "message": "Semantic Search API is running"}


@app.post("/search", response_model=SearchResponse, tags=["search"])
async def search(request: SearchRequest):
    """
    Perform semantic search over the document corpus.

    - **query**: Natural-language query string.
    - **top_k**: Number of results to return (1–20, default 5).
    """
    try:
        results_raw, elapsed_ms = semantic_search(request.query, request.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

    # Enhance results with CloudFront thumbnail URLs
    enhanced_results = []
    for r in results_raw:
        r_copy = r.copy()
        # Convert thumbnail filename to CloudFront URL
        if r["thumbnail"]:
            r_copy["thumbnail"] = build_thumbnail_url(r["thumbnail"])
        enhanced_results.append(VideoResult(**r_copy))

    return SearchResponse(
        query=request.query,
        results=enhanced_results,
        total=len(enhanced_results),
        time_ms=elapsed_ms,
    )


@app.get("/subtopics/count", tags=["status"])
async def subtopics_count():
    """Return how many subtopics are indexed in the FAISS index."""
    from search import _subtopics
    return {"indexed_subtopics": len(_subtopics)}


@app.post("/reload", tags=["status"])
async def reload_index():
    """Re-fetch subtopics from DB and rebuild the FAISS index without restarting."""
    try:
        build_index()
        from search import _subtopics
        return {"status": "ok", "indexed_subtopics": len(_subtopics)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reload failed: {str(e)}")
