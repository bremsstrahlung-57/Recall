from sentence_transformers import SentenceTransformer

from app.core.constants import EMBEDDING_MODEL

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Creates instance for embedding model"""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)

    return _model


def embed(text: str) -> list[float]:
    """Embed given str input"""
    model = get_model()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
