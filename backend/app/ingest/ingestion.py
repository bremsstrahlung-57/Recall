from pathlib import Path

from app.db.qdrant import ingest_data
from app.db.sqlitedb import SQLiteDB
from app.ingest.chunking import chunk_text
from app.ingest.doc_id import make_doc_id

db_action = SQLiteDB()


def ingest_file(path: str, source="user"):
    """File ingestion for Vector DB"""
    text = Path(path).read_text(encoding="utf-8")
    title = Path(path).stem
    doc_id = make_doc_id(text)
    chunks = chunk_text(text)
    total_chunks = chunks[-1].get("chunk_id", 0) + 1
    db_action.insert_doc_ib_db(
        doc_id=doc_id,
        title=title.strip(),
        content=text,
        source=source,
        total_chunks=total_chunks,
    )

    docs = []
    for c in chunks:
        docs.append(
            {
                "doc_id": doc_id,
                "text": c["text"],
                "chunk_id": c["chunk_id"],
            }
        )

    ingest_data(docs)


def ingest_text(text: str):
    """Text ingestiong for Vector DB"""
    doc_id = make_doc_id(text)
    chunks = chunk_text(text)

    docs = []
    for c in chunks:
        docs.append(
            {
                "doc_id": doc_id,
                "text": c["text"],
                "chunk_id": c["chunk_id"],
            }
        )

    ingest_data(docs)
