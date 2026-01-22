from app.db.qdrant import search_chunks

# from app.debug.ingestion import ingest_file

# paths = [
# "app/debug/samples/eldenring.txt",
# "app/debug/samples/recipe.txt",
# "app/debug/samples/sample.txt",
# "app/debug/samples/bloodborne.txt",
# "app/debug/samples/cp2077.txt",
# "app/debug/samples/doom.txt",
# "app/debug/samples/food.txt",
# "app/debug/samples/gow.txt",
# "app/debug/samples/history1.txt",
# "app/debug/samples/history2.txt",
# "app/debug/samples/hollow_knight.txt",
# "app/debug/samples/rdr2.txt",
# "app/debug/samples/recipe.txt",
# "app/debug/samples/sekiro.txt",
# "app/debug/samples/space.txt",
# "app/debug/samples/witcher3.txt",
# ]
# for path in paths:
#     ingest_file(path)

query = input("Enter Query: ")
limit = int(input("Enter Limit: "))
results = search_chunks(query, limit)

print(f"Query: {query}")

for i in results:
    doc_id = i["doc_id"]
    score = i["score"]
    max_score = i["max_score"]
    source = i["source"]
    doc = i["content"][:100] + "..."
    chunk_doc = i["max_chunk_text"][:100] + "..."
    chunk_id = i["chunk_id"]
    total_chunks = i["total_chunks"]
    created_at = i["created_at"]
    all_scores = i["all_scores"]
    stats = i["stats"]

    print(
        f"Doc ID: {doc_id}\nScore: {score:.4f}\nMax Score: {max_score:.4f}\nAll Scores: {all_scores}\nStats: {stats}\nSource: {source}\nDoc: {doc}\nChunk Doc: {chunk_doc}\nChunk ID: {chunk_id}\nTotal Chunks: {total_chunks}\nCreated At: {created_at}\n"
    )
