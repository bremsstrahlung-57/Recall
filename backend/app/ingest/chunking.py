def chunk_text(text: str, chunk_size: int = 512, overlap: int = 128):
    """Chunk text"""
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": chunk,
            }
        )

        chunk_id += 1
        start += chunk_size - overlap
    
    return chunks