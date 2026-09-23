from fastembed import TextEmbedding
from qdrant_client import QdrantClient
from langchain_core.tools import tool

embedding_model = TextEmbedding(threads=1)
client = QdrantClient(url="http://localhost:6333")

SIMILARITY_THRESHOLD = 0.4

@tool
def search_notes(query: str, limit: int = 3) -> str:
    """Search the user's saved notes for recommendations, ideas, reminders, and general information the user has jotted down. Use this for questions about opinions, suggestions, or things someone said or recommended — not for tasks or calendar events."""
    query_vector = list(embedding_model.embed([query]))[0]
    results = client.query_points(
        collection_name="notes",
        query=query_vector.tolist(),
        limit=limit,
    )
    relevant = [p for p in results.points if p.score >= SIMILARITY_THRESHOLD]
    if not relevant:
        return "No relevant notes found."
    return "\n".join(f"- {p.payload['text']}" for p in relevant)