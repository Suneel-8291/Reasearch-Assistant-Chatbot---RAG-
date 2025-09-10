from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import os

# Load embedding model
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Path where FAISS index will be stored
FAISS_PATH = "./faiss_index"


def embed_texts(texts: list[str]):
    """Generate embeddings for a list of texts"""
    return embed_model.encode(texts).tolist()


def add_to_faiss(docs: list[str], metadatas: list[dict], ids: list[str]):
    """Add documents to FAISS index"""
    # Convert raw docs into LangChain Document objects
    documents = [Document(page_content=text, metadata=meta) for text, meta in zip(docs, metadatas)]
    
    # Create FAISS vectorstore from documents
    vectorstore = FAISS.from_documents(documents, lambda x: embed_model.encode(x).tolist())
    
    # Save index
    vectorstore.save_local(FAISS_PATH)


def query_faiss(query: str, n_results=5):
    """Query FAISS index"""
    if not os.path.exists(FAISS_PATH):
        raise ValueError("FAISS index not found. Please add documents first.")

    # Load stored index
    vectorstore = FAISS.load_local(FAISS_PATH, lambda x: embed_model.encode(x).tolist(), allow_dangerous_deserialization=True)
    
    # Run similarity search
    results = vectorstore.similarity_search(query, k=n_results)
    return results


