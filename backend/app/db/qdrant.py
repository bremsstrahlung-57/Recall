import statistics
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.core.config import settings
from app.core.constants import COLLECTION_NAME, EMBEDDING_DIM
from app.db.sqlitedb import SQLiteDB
from app.embeddings.minilm import embed

_client: QdrantClient | None = None
_collection_checked = False
doc_database = SQLiteDB()


def get_qdrant_client() -> QdrantClient:
    """Creates QDrant Client if doesn't exist and returns it"""
    global _client, _collection_checked

    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url)

    if not _collection_checked:
        ensure_collection_exists(
            client=_client,
            collection_name=COLLECTION_NAME,
            vector_size=EMBEDDING_DIM,
        )
        _collection_checked = True

    return _client


def ping_qdrant() -> None:
    client = get_qdrant_client()


def _assert_embedding_dim():
    """Check for right dimensions"""
    vec = embed("dim check")
    if len(vec) != EMBEDDING_DIM:
        raise RuntimeError(
            f"Embedding dim mismatch: expected {EMBEDDING_DIM}, got {len(vec)}"
        )


def ensure_collection_exists(
    client: QdrantClient, collection_name: str, vector_size: int
) -> None:
    try:
        client.get_collection(collection_name)
        return
    except UnexpectedResponse as e:
        if e.status_code != 404:
            raise

    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE,
        ),
    )


def search_docs(query, limit=5, k=3):
    """Search for a query from the Vector DB"""
    client: QdrantClient = get_qdrant_client()
    query_vector = embed(text=query)

    search_results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit,
        with_vectors=False,
    )

    doc_score_map = {}

    for item in search_results.points:
        doc_id = item.payload.get("doc_id")
        score = item.score
        text = item.payload.get("text", "")
        chunk_id = item.payload.get("chunk_id")

        if doc_id not in doc_score_map:
            doc_score_map[doc_id] = {
                "max_score": score,
                "text": text,
                "chunk_id": chunk_id,
                "all_scores": [score],
                "chunks": [
                    {
                        "chunk_id": chunk_id,
                        "text": text,
                        "score": score,
                    }
                ],
            }
        else:
            doc_score_map[doc_id]["max_score"] = max(
                doc_score_map[doc_id]["max_score"], score
            )
            doc_score_map[doc_id]["all_scores"].append(score)
            if not any(
                c["chunk_id"] == chunk_id for c in doc_score_map[doc_id]["chunks"]
            ):
                doc_score_map[doc_id]["chunks"].append(
                    {
                        "chunk_id": chunk_id,
                        "text": text,
                        "score": score,
                    }
                )

    doc_db = doc_database.read_from_cache()
    results = []

    for row in doc_db:
        doc_id = row[0]
        if doc_id in doc_score_map:
            chunks = doc_score_map[doc_id]["chunks"]

            sorted_chunks = sorted(
                chunks,
                key=lambda c: c["score"],
                reverse=True,
            )
            topk_chunks = [
                {
                    "chunk_id": c["chunk_id"],
                    "score": c["score"],
                    "text": c["text"],
                }
                for c in sorted_chunks[:k]
            ]

            best_chunk = topk_chunks[0]
            scores = [c["score"] for c in chunks]
            mean = statistics.mean(scores)
            median = statistics.median(scores)
            mode = statistics.median(scores)
            topk_score = statistics.mean(scores[:k])

            results.append(
                {
                    "doc_id": doc_id,
                    "score": topk_score,
                    "max_score": best_chunk["score"],
                    "title": row[1],
                    "content": row[2],
                    "max_chunk_text": best_chunk["text"],
                    "source": row[3],
                    "total_chunks": row[4],
                    "chunk_id": best_chunk["chunk_id"],
                    "all_chunks": topk_chunks,
                    "created_at": row[5],
                    "all_scores": scores,
                    "stats": {
                        "mean": mean,
                        "median": median,
                        "mode": mode,
                    },
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)
    max_score = results[0].get("score")
    final_res = list(
        filter(
            lambda d: d.get("score") >= 0.25 and d.get("score") >= max_score * 0.60,
            results,
        )
    )
    return final_res


def ingest_data(docs):
    """Upsert data in Vector DB"""
    client: QdrantClient = get_qdrant_client()
    points = []
    for doc in docs:
        text = doc["text"]
        doc_id = doc["doc_id"]
        chunk_id = doc["chunk_id"]

        points.append(
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embed(text),
                payload={
                    "text": text,
                    "source": "debug",
                    "doc_id": doc_id,
                    "chunk_id": chunk_id,
                },
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return client.get_collection(COLLECTION_NAME)
