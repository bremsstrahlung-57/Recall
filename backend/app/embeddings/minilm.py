import asyncio
import logging

from fastembed import TextEmbedding

logger = logging.getLogger(__name__)
_model: TextEmbedding | None = None
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_model():
    """Creates instance for embedding model"""
    global _model
    if _model is None:
        logger.info("loading embedding model", extra={"model": EMBEDDING_MODEL})
        _model = TextEmbedding(EMBEDDING_MODEL)
        logger.info("embedding model loaded", extra={"model": EMBEDDING_MODEL})

    return _model


def _embed_sync(text: str) -> list[float]:
    model = get_model()
    vector = list(model.embed([text]))[0].tolist()
    logger.debug(
        "text embedded", extra={"text_len": len(text), "vector_dim": len(vector)}
    )
    return vector


async def embed(text: str) -> list[float]:
    """Embed given str input"""
    return await asyncio.to_thread(_embed_sync, text)
