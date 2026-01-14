from pathlib import Path

from app.db.qdrant import ingest_data
from app.ingest.chunking import chunk_text
from app.ingest.doc_id import make_doc_id


def ingest_file(path: str):
    text = Path(path).read_text(encoding="utf-8")
    doc_id = make_doc_id(text)
    chunks = chunk_text(text)

    docs = []
    for c in chunks:
        docs.append(
            {
                "text": c["text"],
                "doc_id": doc_id,
                "chunk_id": c["chunk_id"],
            }
        )

    ingest_data(docs)


if __name__ == "__main__":
    ingest_file("app/debug/sample.txt")
