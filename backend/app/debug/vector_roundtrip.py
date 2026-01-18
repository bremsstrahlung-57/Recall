from app.db.qdrant import search_chunks
# from app.debug.ingestion import ingest_file

# paths = ["app/debug/samples/eldenring.txt", "app/debug/samples/recipe.txt", "app/debug/samples/sample.txt"]
# for path in paths:
#     ingest_file(path)

# ingest_file("app/debug/samples/eldenring.txt")

query = input("Enter Query: ")
results = search_chunks(query)

print(f"Query: {query}\n")

for i in results:
    doc_id = i["doc_id"]
    score = i["score"]
    source = i["source"]
    doc = i["content"][:100] + "..."
    chunk_doc = i["max_chunk_text"]
    chunk_id = i["chunk_id"]
    total_chunks = i["total_chunks"]
    created_at = i["created_at"]

    print(
        f"Doc ID: {doc_id}\nScore: {score:.4f}\nSource: {source}\nDoc: {doc}\nChunk Doc: {chunk_doc}\nChunk ID: {chunk_id}\nTotal Chunks: {total_chunks}\nCreated At: {created_at}\n"
    )
