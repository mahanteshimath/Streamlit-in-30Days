import streamlit as st

st.set_page_config(page_title="Day 18 - Embeddings", page_icon="1️⃣8️⃣")

st.title("Day 18: Embeddings")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Create text embeddings
- Choose embedding models
- Embed documents and queries
- Understand cosine similarity
""")

st.header("📖 Content")

st.subheader("What are Embeddings?")
st.markdown("""
Embeddings are numerical representations of text that capture semantic meaning.

**Properties:**
- Fixed-length vectors (e.g., 1536 dimensions)
- Similar text → Similar vectors
- Enable semantic search
- Language-agnostic capabilities
""")

st.subheader("Creating Embeddings")
st.code("""
from openai import OpenAI

@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = get_client()

def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# Example
text = "What is machine learning?"
embedding = get_embedding(text)
st.write(f"Embedding dimensions: {len(embedding)}")
""", language="python")

st.subheader("Embedding Models Comparison")
st.markdown("""
| Model | Dimensions | Cost | Performance |
|-------|------------|------|-------------|
| text-embedding-ada-002 | 1536 | $0.0001/1K tokens | Good |
| text-embedding-3-small | 1536 | $0.00002/1K tokens | Better |
| text-embedding-3-large | 3072 | $0.00013/1K tokens | Best |
| sentence-transformers | 384-768 | Free (local) | Decent |
""")

st.subheader("Cosine Similarity")
st.markdown("Measure how similar two embeddings are:")

st.code("""
import numpy as np

def cosine_similarity(vec1, vec2):
    # Calculate dot product
    dot_product = np.dot(vec1, vec2)
    
    # Calculate magnitudes
    magnitude1 = np.linalg.norm(vec1)
    magnitude2 = np.linalg.norm(vec2)
    
    # Calculate cosine similarity
    return dot_product / (magnitude1 * magnitude2)

# Example
text1 = "I love programming"
text2 = "I enjoy coding"
text3 = "The weather is nice"

emb1 = get_embedding(text1)
emb2 = get_embedding(text2)
emb3 = get_embedding(text3)

sim_1_2 = cosine_similarity(emb1, emb2)  # High similarity
sim_1_3 = cosine_similarity(emb1, emb3)  # Low similarity

st.write(f"Similarity (1-2): {sim_1_2:.4f}")
st.write(f"Similarity (1-3): {sim_1_3:.4f}")
""", language="python")

st.subheader("Batch Embedding")
st.code("""
def embed_documents(texts, batch_size=100):
    embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        response = client.embeddings.create(
            input=batch,
            model="text-embedding-3-small"
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        embeddings.extend(batch_embeddings)
        
        st.progress((i + batch_size) / len(texts))
    
    return embeddings

# Use it
doc_embeddings = embed_documents(document_chunks)
""", language="python")

st.subheader("Caching Embeddings")
st.code("""
@st.cache_data
def get_cached_embedding(text):
    return get_embedding(text)

# Or save to file
import pickle

def save_embeddings(embeddings, filename):
    with open(filename, 'wb') as f:
        pickle.dump(embeddings, f)

def load_embeddings(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
""", language="python")

st.markdown("---")
st.info("✅ Master embeddings!")

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
