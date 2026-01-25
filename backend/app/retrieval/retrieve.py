from app.db.qdrant import fetch_chunk_by_ids, search_docs


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


def expand_chunk_ids(chunk_ids, total_chunks):
    window = set()
    for cid in chunk_ids:
        for x in (cid - 1, cid, cid + 1):
            if 0 <= x < total_chunks:
                window.add(x)

    return sorted(window)


def get_evidence_chunks(all_chunks):
    return sorted(
        all_chunks,
        key=lambda c: c["score"],
        reverse=True,
    )


def build_context(doc_id, evidence, total_chunks):
    hit_ids = [e["chunk_id"] for e in evidence]
    window_ids = expand_chunk_ids(hit_ids, total_chunks)

    points = fetch_chunk_by_ids(doc_id, window_ids)

    points.sort(key=lambda p: p.payload["chunk_id"])

    return "\n".join(p.payload["text"] for p in points)


def refine_results(results):
    refined_for_context = []

    for item in results:
        doc_id = item["doc_id"]
        title = item["title"]
        source = item["source"]
        chunks = item["all_chunks"]
        total_chunks = item["total_chunks"]

        evidence = get_evidence_chunks(
            item["all_chunks"],
        )

        context = build_context(doc_id, chunks, total_chunks)

        refined_for_context.append(
            {
                "doc_id": doc_id,
                "title": title,
                "source": source,
                "context": context,
                "evidence": [
                    {"chunk_id": e["chunk_id"], "score": e["score"]} for e in evidence
                ],
            }
        )

    return refined_for_context
