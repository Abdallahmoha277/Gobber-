from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
client = QdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "code_memory"


def init_memory():
    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def search_memory(query: str, limit: int = 1) -> str:
    init_memory()
    query_vector = embeddings.embed_query(query)
    search_result = client.query_points(
        collection_name=COLLECTION_NAME, query=query_vector, limit=limit
    ).points
    if search_result:
        return search_result[0].payload.get("solution", "")
    return ""


def save_memory(query: str, solution: str):
    init_memory()
    vector = embeddings.embed_query(query)
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={"query": query, "solution": solution},
            )
        ],
    )
