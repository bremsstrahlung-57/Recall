from qdrant_client import QdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings
from app.core.constants import COLLECTION_NAME, EMBEDDING_DIM

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _client

    if _client is None:
        _client = QdrantClient(url=settings.qdrant_url)

    return _client


def ping_qdrant() -> None:
    client = get_qdrant_client()
    # client.get_collections()
    ensure_collection_exists(
        client=client,
        collection_name=COLLECTION_NAME,
        vector_size=EMBEDDING_DIM,
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
