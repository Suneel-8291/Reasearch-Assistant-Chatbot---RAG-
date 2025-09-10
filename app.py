__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")




import streamlit as st
from models.embeddings import add_to_chroma, query_chroma
from models.llm import ask_gemini
from utils.url_loader import load_url
from utils.web_search import serper_search

st.title("Research Assistant Chatbot")


# -----------------------------
# Helper function: get context
# -----------------------------
def get_context(user_query, n_results=5):
    """Retrieve context from local RAG or fallback to Serper search."""

    # 🔹 Special handling: if user asks about stock price → go directly to Serper
    if "stock price" in user_query.lower():
        st.info("Fetching live stock price via web search...")
        web_results = serper_search(user_query)
        if web_results:
            context = "\n\n".join(
                [f"{r['title']}: {r['snippet']} ({r['link']})" for r in web_results]
            )
        else:
            context = "No stock price information found."
        source_info = "Sources: Web search via Serper"
        return context, source_info

    # 🔹 Default path: first try local RAG
    results = query_chroma(user_query, n_results=n_results)

    docs = results.get("documents", [])
    metas = results.get("metadatas", [])

    has_valid_docs = bool(docs and len(docs[0]) > 0 and any(d.strip() for d in docs[0]))

    if has_valid_docs:
        context = "\n\n".join(docs[0])
        sources = [m.get("source", "unknown") for m in metas[0]] if metas and metas[0] else []
        source_text = ", ".join(set(sources)) if sources else "unknown source"
        source_info = "Sources: " + source_text
    else:
        st.warning("No relevant context found locally. Searching the web...")
        web_results = serper_search(user_query)
        if web_results:
            context = "\n\n".join(
                [f"{r['title']}: {r['snippet']} ({r['link']})" for r in web_results]
            )
        else:
            context = "No information found."
        source_info = "Sources: Web search via Serper"

    return context, source_info


# -----------------------------
# URL ingestion
# -----------------------------
url = st.text_input("Paste a research article URL")
if url:
    text = load_url(url)
    if "Error" not in text:
        chunks = [text[i:i + 1000] for i in range(0, len(text), 1000)]
        add_to_chroma(
            docs=chunks,
            metadatas=[{"source": url}] * len(chunks),
            ids=[f"{url}_{i}" for i in range(len(chunks))]
        )
        st.success(f"URL added to knowledge base: {url}")
    else:
        st.error(text)


# -----------------------------
# User query
# -----------------------------
query = st.text_input("Ask a research question")
mode = st.radio("Response Mode", ["Concise", "Detailed"])

if query:

    # Normalize query for "who is this" style
    if query.strip().lower() in ["name", "who", "who is this", "who is described in the url"]:
        query = "Summarize the main person or subject that this document/URL is about."

    # Get context from RAG or Serper
    context, source_info = get_context(query, n_results=5)

    # Construct prompt
    prompt = f"""
You are a research assistant. Use the context below (extracted from {source_info})
to answer the user's question.

Context:
{context}

Question:
{query}

Instructions:
- If the user asks "who is described in the URL" or similar, identify the main person or subject
  the page is about (not just any names mentioned).
- If the user asks for stock prices, give the most recent figure from the search results.
- Give a clear, direct answer in a {mode.lower()} way.
"""

    # Get LLM answer
    answer = ask_gemini(prompt)

    # Display result
    st.write(answer)
    st.caption(source_info)

