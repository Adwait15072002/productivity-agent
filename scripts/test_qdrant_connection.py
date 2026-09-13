from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

client = QdrantClient(url="http://localhost:6333")

if not client.collection_exists("connectivity_check"):
    client.create_collection(
        collection_name="connectivity_check",
        vectors_config=VectorParams(size=4, distance=Distance.COSINE),
    )

client.upsert(
    collection_name="connectivity_check",
    points=[PointStruct(id=1, vector=[0.1, 0.2, 0.3, 0.4], payload={"note": "hello qdrant"})],
)
print(client.retrieve(collection_name="connectivity_check", ids=[1]))