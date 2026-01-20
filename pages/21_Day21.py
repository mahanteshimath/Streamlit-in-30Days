import streamlit as st

st.set_page_config(page_title="Day 21 - Practice Project 3", page_icon="2️⃣1️⃣")

st.title("Day 21: Practice Project 3")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Project: Document Q&A System")
st.markdown("""
Build a complete RAG application with document upload, processing, and Q&A!

### Requirements:
1. ✅ Document upload (PDF, TXT, DOCX)
2. ✅ Document processing and chunking
3. ✅ Vector database integration
4. ✅ Semantic search
5. ✅ Context-aware responses
6. ✅ Source citations
7. ✅ Chat history
8. ✅ Export functionality
""")

st.header("📝 Complete Implementation")

st.code("""
import streamlit as st
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import tempfile
import os

st.set_page_config(page_title="Document Q&A", page_icon="📚", layout="wide")

# Initialize session state
if 'vectorstore' not in st.session_state:
    st.session_state.vectorstore = None
if 'qa_history' not in st.session_state:
    st.session_state.qa_history = []

# Sidebar for document upload
with st.sidebar:
    st.header("📁 Upload Documents")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            all_chunks = []
            
            for file in uploaded_files:
                # Save temp file
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp:
                    tmp.write(file.read())
                    tmp_path = tmp.name
                
                # Load document
                if file.name.endswith('.pdf'):
                    loader = PyPDFLoader(tmp_path)
                else:
                    loader = TextLoader(tmp_path)
                
                docs = loader.load()
                
                # Split into chunks
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                chunks = splitter.split_documents(docs)
                
                # Add source metadata
                for chunk in chunks:
                    chunk.metadata['source'] = file.name
                
                all_chunks.extend(chunks)
                os.unlink(tmp_path)
            
            # Create vector store
            embeddings = OpenAIEmbeddings()
            st.session_state.vectorstore = Chroma.from_documents(
                documents=all_chunks,
                embedding=embeddings,
                persist_directory="./doc_qa_db"
            )
            
            st.success(f"Processed {len(all_chunks)} chunks from {len(uploaded_files)} documents!")
    
    st.divider()
    
    # Settings
    st.subheader("⚙️ Settings")
    k_docs = st.slider("Documents to retrieve", 1, 10, 3)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0)
    
    st.divider()
    
    if st.button("Clear Database"):
        st.session_state.vectorstore = None
        st.session_state.qa_history = []
        st.success("Cleared!")

# Main area
st.title("📚 Document Q&A System")

if st.session_state.vectorstore is None:
    st.info("👈 Upload documents to get started!")
else:
    # Display history
    for qa in st.session_state.qa_history:
        with st.chat_message("user"):
            st.write(qa["question"])
        
        with st.chat_message("assistant"):
            st.write(qa["answer"])
            
            with st.expander("📄 View Sources"):
                for i, source in enumerate(qa["sources"], 1):
                    st.markdown(f"**Source {i}:**")
                    st.write(source["content"])
                    st.caption(f"From: {source['metadata']}")
                    st.divider()
    
    # Question input
    if question := st.chat_input("Ask a question about your documents..."):
        # Display question
        with st.chat_message("user"):
            st.write(question)
        
        # Get answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # Create QA chain
                llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=temperature
                )
                
                qa_chain = RetrievalQA.from_chain_type(
                    llm=llm,
                    retriever=st.session_state.vectorstore.as_retriever(
                        search_kwargs={"k": k_docs}
                    ),
                    return_source_documents=True
                )
                
                # Get result
                result = qa_chain({"query": question})
                answer = result["result"]
                sources = result["source_documents"]
                
                # Display answer
                st.write(answer)
                
                # Display sources
                with st.expander("📄 View Sources"):
                    for i, doc in enumerate(sources, 1):
                        st.markdown(f"**Source {i}:**")
                        st.write(doc.page_content)
                        st.caption(f"From: {doc.metadata.get('source', 'Unknown')}")
                        st.divider()
                
                # Save to history
                st.session_state.qa_history.append({
                    "question": question,
                    "answer": answer,
                    "sources": [
                        {
                            "content": doc.page_content,
                            "metadata": doc.metadata.get('source', 'Unknown')
                        }
                        for doc in sources
                    ]
                })
    
    # Export functionality
    if st.session_state.qa_history:
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Q&A History"):
                import json
                export_data = json.dumps(st.session_state.qa_history, indent=2)
                st.download_button(
                    "Download JSON",
                    export_data,
                    "qa_history.json",
                    "application/json"
                )
        
        with col2:
            if st.button("🗑️ Clear History"):
                st.session_state.qa_history = []
                st.rerun()
""", language="python")

st.header("🎨 Enhancement Ideas")
st.markdown("""
1. **Multi-language Support** - Detect and handle multiple languages
2. **Document Comparison** - Compare information across documents
3. **Summary Generation** - Auto-summarize uploaded documents
4. **Keyword Highlighting** - Highlight relevant parts in sources
5. **Document Preview** - Show document thumbnails
6. **Advanced Filters** - Filter by date, source, topic
7. **Conversation Branching** - Create new conversation threads
8. **Analytics Dashboard** - Show usage statistics
9. **Collaborative Features** - Share Q&A with team
10. **API Integration** - Create REST API endpoints
""")

st.header("🧪 Testing Checklist")
checklist_items = [
    "Upload various file types",
    "Handle large documents",
    "Test with multiple documents",
    "Verify source citations",
    "Check answer accuracy",
    "Test edge cases (empty docs, special characters)",
    "Verify export functionality",
    "Test clear/reset functions",
    "Check mobile responsiveness",
    "Validate error handling"
]

for item in checklist_items:
    st.checkbox(item, key=f"test_{item}")

st.markdown("---")
st.success("🎉 Complete this project to finish Section 3!")

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
