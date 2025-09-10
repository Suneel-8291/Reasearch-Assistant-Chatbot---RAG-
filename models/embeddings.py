from sentence_transformers import SentenceTransformer
import chromadb

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client (in-memory for now)
client = chromadb.Client()
collection = client.get_or_create_collection("research_papers")


def embed_texts(texts: list[str]):
    return embed_model.encode(texts).tolist()


def reset_collection():
    """Clear the Chroma collection so only the latest doc is stored."""
    global collection
    client.delete_collection("research_papers")
    collection = client.create_collection("research_papers")


def add_to_chroma(docs, metadatas, ids):
    embeddings = embed_texts(docs)
    collection.add(
        documents=docs,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def query_chroma(query: str, n_results=5):
    query_emb = embed_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_emb,
        n_results=n_results
    )
    return results










