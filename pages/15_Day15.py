import streamlit as st

st.set_page_config(page_title="Day 15 - Intro to RAG", page_icon="1️⃣5️⃣")

st.title("Day 15: Introduction to RAG")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Understand RAG (Retrieval-Augmented Generation) concepts
- Learn RAG architecture
- Explore use cases for RAG
- Compare RAG vs fine-tuning
""")

st.header("📖 Content")

st.subheader("What is RAG?")
st.markdown("""
**Retrieval-Augmented Generation (RAG)** combines information retrieval with text generation to provide accurate, context-specific responses.

**How it works:**
1. **Retrieve** relevant documents from a knowledge base
2. **Augment** the prompt with retrieved context
3. **Generate** a response using the LLM
""")

st.subheader("RAG Architecture")
st.code("""
┌─────────────┐
│ User Query  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ Embed Query     │ ← Convert to vector
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Search Vector DB│ ← Find similar docs
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Retrieve Docs   │ ← Get top K results
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Augment Prompt  │ ← Add context
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Generate Answer │ ← LLM produces response
└─────────────────┘
""", language="text")

st.subheader("RAG vs Fine-Tuning")

comparison = {
    "Aspect": ["Update Frequency", "Cost", "Data Requirements", "Accuracy", "Setup Time"],
    "RAG": ["Real-time", "Low", "Any amount", "High (with good docs)", "Quick"],
    "Fine-Tuning": ["Periodic retraining", "High", "Large datasets needed", "High (with good data)", "Slow"]
}

import pandas as pd
st.table(pd.DataFrame(comparison))

st.subheader("Use Cases")
st.markdown("""
**Perfect for RAG:**
- 📚 Document Q&A systems
- 💼 Customer support with knowledge bases
- 🔬 Research assistants
- 📖 Educational tutors
- 💻 Code documentation helpers
- 🏢 Internal company wikis

**When to use Fine-Tuning:**
- Specific writing style
- Domain-specific language
- Task-specific behavior
- No external knowledge needed
""")

st.subheader("Simple RAG Example")
st.code("""
# Pseudo-code for RAG
def answer_question(question, knowledge_base):
    # 1. Embed the question
    query_embedding = embed(question)
    
    # 2. Search for relevant documents
    relevant_docs = vector_db.search(query_embedding, top_k=3)
    
    # 3. Create context from documents
    context = "\\n".join([doc.text for doc in relevant_docs])
    
    # 4. Generate answer with context
    prompt = f\"\"\"
    Context: {context}
    
    Question: {question}
    
    Answer based on the context provided:
    \"\"\"
    
    response = llm.generate(prompt)
    return response
""", language="python")

st.subheader("Key Components")
st.markdown("""
1. **Document Loader** - Load various file types
2. **Text Splitter** - Chunk documents into manageable pieces
3. **Embedding Model** - Convert text to vectors
4. **Vector Database** - Store and search embeddings
5. **LLM** - Generate final response
6. **Retriever** - Fetch relevant documents
""")

st.markdown("---")
st.info("✅ Start your RAG journey!")

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
