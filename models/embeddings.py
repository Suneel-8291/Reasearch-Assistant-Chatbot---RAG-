from sentence_transformers import SentenceTransformer
import chromadb

embed_model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="research_papers")

def embed_texts(texts: list[str]):
    return embed_model.encode(texts).tolist()

def add_to_chroma(docs, metadatas, ids):
    embeddings = embed_texts(docs)
    collection.add(documents=docs, embeddings=embeddings, metadatas=metadatas, ids=ids)

def query_chroma(query: str, n_results=5):
    query_emb = embed_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_emb, n_results=n_results)
    return results

