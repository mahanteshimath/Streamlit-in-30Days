import streamlit as st

st.set_page_config(page_title="Day 17 - Vector Databases", page_icon="1️⃣7️⃣")

st.title("Day 17: Vector Databases")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Introduction to vector databases
- Popular options (Chroma, Pinecone, FAISS)
- Vector storage and retrieval
- Similarity search
""")

st.header("📖 Content")

st.subheader("What are Vector Databases?")
st.markdown("""
Vector databases store and search high-dimensional vectors (embeddings) efficiently.

**Key Features:**
- Fast similarity search
- Scalable storage
- Metadata filtering
- Hybrid search capabilities
""")

st.subheader("Popular Vector Databases")
st.markdown("""
| Database | Type | Best For |
|----------|------|----------|
| **Chroma** | Open-source | Development, small-medium projects |
| **FAISS** | Library | Local, fast prototyping |
| **Pinecone** | Cloud | Production, scalability |
| **Weaviate** | Open-source | Self-hosted production |
| **Qdrant** | Open-source | Performance, filtering |
""")

st.subheader("Chroma DB Example")
st.code("""
import chromadb
from chromadb.config import Settings

# Initialize Chroma client
@st.cache_resource
def get_chroma_client():
    return chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="./chroma_db"
    ))

client = get_chroma_client()

# Create collection
collection = client.create_collection(
    name="my_documents",
    metadata={"description": "Document collection"}
)

# Add documents
collection.add(
    documents=["Text 1", "Text 2", "Text 3"],
    ids=["id1", "id2", "id3"],
    metadatas=[{"source": "doc1"}, {"source": "doc2"}, {"source": "doc3"}]
)

# Query
results = collection.query(
    query_texts=["your search query"],
    n_results=3
)
""", language="python")

st.subheader("LangChain Integration")
st.code("""
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings

# Create embeddings
embeddings = OpenAIEmbeddings()

# Create vector store
vectorstore = Chroma.from_texts(
    texts=chunks,
    embedding=embeddings,
    persist_directory="./db"
)

# Save
vectorstore.persist()

# Query
docs = vectorstore.similarity_search("your query", k=3)
""", language="python")

st.subheader("Similarity Search")
st.markdown("""
**How it works:**
1. Convert query to embedding
2. Calculate distance to all vectors
3. Return nearest neighbors

**Distance Metrics:**
- **Cosine similarity** - Most common
- **Euclidean distance** - Geometric distance
- **Dot product** - Fast computation
""")

st.code("""
# Similarity search with score
docs_with_scores = vectorstore.similarity_search_with_score(
    query="your question",
    k=3
)

for doc, score in docs_with_scores:
    st.write(f"Score: {score}")
    st.write(doc.page_content)
    st.divider()
""", language="python")

st.markdown("---")
st.info("✅ Work with vector databases!")

st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: blue;
        color: white; # Adjust this for expander header color
    }
    .streamlit-expanderContent {
        background-color: blue;
        color: white; # Expander content color
    }
    </style>
    ''',
    unsafe_allow_html=True
)

footer="""<style>

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: #2C1E5B;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤️ by <a style='display: inline; text-align: center;' href="https://bit.ly/atozaboutdata" target="_blank">MAHANTESH HIREMATH</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
