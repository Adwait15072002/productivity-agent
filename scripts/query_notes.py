# scripts/query_notes.py
from fastembed import TextEmbedding
from qdrant_client import QdrantClient

embedding_model = TextEmbedding(threads=1)
client = QdrantClient(url="http://localhost:6333")

query_vector = list(embedding_model.embed(["what did Raj recommend?"]))[0]

results = client.query_points(
    collection_name="notes",
    query=query_vector.tolist(),
    limit=3,
)
for point in results.points:
    print(round(point.score, 3), point.payload["text"])