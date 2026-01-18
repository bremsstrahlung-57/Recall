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


def search_chunks(query: str, limit: int = 5):
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
                "score": score,
                "text": text,
                "chunk_id": chunk_id,
            }
        else:
            doc_score_map[doc_id]["score"] = max(doc_score_map[doc_id]["score"], score)
            if chunk_id != doc_score_map[doc_id]["chunk_id"]:
                doc_score_map[doc_id]["chunk_id"] = chunk_id
                doc_score_map[doc_id]["text"] = text

    doc_db = doc_database.read_from_cache()
    results = []

    for row in doc_db:
        doc_id = row[0]
        if doc_id in doc_score_map:
            results.append(
                {
                    "doc_id": doc_id,
                    "score": doc_score_map[doc_id]["score"],
                    "content": row[1],
                    "max_chunk_text": doc_score_map[doc_id]["text"],
                    "source": row[2],
                    "total_chunks": row[3],
                    "chunk_id": doc_score_map[doc_id]["chunk_id"],
                    "created_at": row[4],
                }
            )

    results.sort(key=lambda item: item["score"], reverse=True)
    return results


def ingest_data(docs: list):
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
