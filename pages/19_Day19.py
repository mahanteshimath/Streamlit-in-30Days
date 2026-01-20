import streamlit as st

st.set_page_config(page_title="Day 19 - Retrieval Strategies", page_icon="1️⃣9️⃣")

st.title("Day 19: Retrieval Strategies")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Semantic search techniques
- Hybrid search approaches
- Re-ranking strategies
- Query optimization
""")

st.header("📖 Content")

st.subheader("Retrieval Strategies")
st.markdown("""
Different approaches to find the most relevant documents:

1. **Semantic Search** - Vector similarity
2. **Keyword Search** - Traditional BM25
3. **Hybrid Search** - Combine both
4. **Re-ranking** - Improve initial results
5. **Multi-query** - Generate multiple queries
""")

st.subheader("Basic Semantic Search")
st.code("""
from langchain.vectorstores import Chroma

# Simple retrieval
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

docs = retriever.get_relevant_documents("your query")
""", language="python")

st.subheader("MMR (Maximum Marginal Relevance)")
st.markdown("Retrieves diverse documents to avoid redundancy:")

st.code("""
# MMR retrieval
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,              # Number of documents
        "fetch_k": 20,       # Initial fetch size
        "lambda_mult": 0.5   # Diversity (0=max diversity, 1=max relevance)
    }
)

docs = retriever.get_relevant_documents(query)
""", language="python")

st.subheader("Similarity Score Threshold")
st.code("""
# Only return docs above threshold
retriever = vectorstore.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "score_threshold": 0.7,  # Minimum similarity
        "k": 5
    }
)

docs = retriever.get_relevant_documents(query)
""", language="python")

st.subheader("Hybrid Search")
st.code("""
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever

# Keyword-based retriever
bm25_retriever = BM25Retriever.from_texts(texts)
bm25_retriever.k = 3

# Vector-based retriever
vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

# Combine both
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.4, 0.6]  # Weight keyword vs semantic
)

docs = ensemble_retriever.get_relevant_documents(query)
""", language="python")

st.subheader("Contextual Compression")
st.markdown("Extract only relevant parts of documents:")

st.code("""
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Create compressor
compressor = LLMChainExtractor.from_llm(llm)

# Wrap base retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_retriever
)

compressed_docs = compression_retriever.get_relevant_documents(query)
""", language="python")

st.subheader("Multi-Query Retrieval")
st.code("""
from langchain.retrievers.multi_query import MultiQueryRetriever

# Generate multiple query variations
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=vectorstore.as_retriever(),
    llm=llm
)

# Automatically generates variations and retrieves
unique_docs = multi_query_retriever.get_relevant_documents(
    query="What is machine learning?"
)

# Might generate queries like:
# - "Define machine learning"
# - "Explain AI and ML"
# - "How does ML work?"
""", language="python")

st.subheader("Custom Retrieval Logic")
st.code("""
def advanced_retrieve(query, vectorstore, top_k=5):
    # 1. Get initial results
    initial_docs = vectorstore.similarity_search_with_score(query, k=top_k*2)
    
    # 2. Filter by score threshold
    filtered = [(doc, score) for doc, score in initial_docs if score < 0.5]
    
    # 3. Re-rank by metadata (e.g., recency)
    sorted_docs = sorted(
        filtered,
        key=lambda x: x[0].metadata.get('date', ''),
        reverse=True
    )
    
    # 4. Return top K
    return [doc for doc, score in sorted_docs[:top_k]]
""", language="python")

st.markdown("---")
st.info("✅ Optimize retrieval performance!")

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
