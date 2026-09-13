# data/seed_notes.py
from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

embedding_model = TextEmbedding(threads=1) # defaults to BAAI/bge-small-en-v1.5
client = QdrantClient(url="http://localhost:6333")

notes = [
    "Meeting with design team moved to Thursday 3pm, need to prep mockup feedback.",
    "Idea: automate weekly status report using the agent's calendar + task summary.",
    "Remember to renew domain registration before it expires next month.",
    "Book recommendation from Raj: 'Thinking in Systems' - good for architecture planning.",
]

vectors = list(embedding_model.embed(notes))
vector_size = len(vectors[0])

if not client.collection_exists("notes"):
    client.create_collection(
        collection_name="notes",
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )

client.upsert(
    collection_name="notes",
    points=[
        PointStruct(id=i + 1, vector=vectors[i].tolist(), payload={"text": notes[i], "source": "seed"})
        for i in range(len(notes))
    ],
)
print(f"Seeded {len(notes)} notes (embedding dim: {vector_size}).")