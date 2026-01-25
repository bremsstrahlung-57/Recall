from app.db.qdrant import search_docs


def retrieve_data(query: str, limit: int):
    original_data = search_docs(query, limit)
    context_data = []

    for item in original_data:
        doc_id = item["doc_id"]
        score = item["score"]
        chunk_doc = item["max_chunk_text"]
        con = {
            "doc_id": doc_id,
            "score": score,
            "chunk_doc": chunk_doc,
        }
        context_data.append(con)

    return context_data


# def build_context()
