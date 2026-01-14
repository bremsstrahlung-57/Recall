from app.db.qdrant import search_text

query = "elden ring"
# texts = [
#     "This is a document about AI and machine learning",
#     "Qdrant is a vector database",
#     "FastAPI is used for backend services",
# ]
# info = ingest_data(texts)
vector = search_text(query)
max = 0
text = ""
for i in vector:
    score = i["score"]
    if max < score:
        max = score
        text = i["text"]

print(f"Score: {max}\nDoc: {text}")
