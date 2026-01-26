from fastapi import APIRouter, Query

from app.db.qdrant import search_docs
from app.retrieval.retrieve import retrieve_data

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "version": "0.2.1"}


@router.get("/search")
def search_api(
    query: str = Query(..., min_length=3),
    limit: int = Query(5, ge=1, le=50),
    k: int = Query(3, ge=1, le=5),
    debug: bool = Query(False),
):
    if debug:
        return search_docs(query, limit, k)
    else:
        return retrieve_data(query, limit, k)
