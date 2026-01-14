def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100):
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk size")

    chunks = []
    step = chunk_size - overlap
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
        start += step

    return chunks
