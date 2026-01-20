import streamlit as st

st.set_page_config(page_title="Day 20 - RAG Implementation", page_icon="2️⃣0️⃣")

st.title("Day 20: RAG Implementation")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Build end-to-end RAG system
- Integrate all components
- Handle responses with sources
- Implement error handling
""")

st.header("📖 Content")

st.subheader("Complete RAG System")
st.code("""
import streamlit as st
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Initialize components
@st.cache_resource
def init_rag_system():
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    return vectorstore, llm

vectorstore, llm = init_rag_system()

# Create retrieval QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True
)

# Query
if query := st.chat_input("Ask a question"):
    with st.spinner("Searching..."):
        result = qa_chain({"query": query})
    
    st.write(result["result"])
    
    # Show sources
    with st.expander("📚 Sources"):
        for doc in result["source_documents"]:
            st.write(doc.page_content)
            st.caption(f"Source: {doc.metadata.get('source', 'Unknown')}")
""", language="python")

st.subheader("Custom RAG Prompt")
st.code("""
template = \"\"\"Use the following pieces of context to answer the question.
If you don't know the answer, say so. Don't make up information.

Context:
{context}

Question: {question}

Provide a detailed answer with specific references to the context:
\"\"\"

PROMPT = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": PROMPT},
    return_source_documents=True
)
""", language="python")

st.subheader("Conversational RAG")
st.code("""
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# Setup memory
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# Create conversational chain
conv_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    memory=memory,
    return_source_documents=True
)

# Use it
result = conv_chain({"question": query})
answer = result["answer"]
sources = result["source_documents"]
""", language="python")

st.subheader("Streaming RAG Responses")
st.code("""
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Create streaming LLM
streaming_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# Custom streaming handler for Streamlit
class StreamHandler:
    def __init__(self, container):
        self.container = container
        self.text = ""
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# Use it
if query := st.chat_input("Ask"):
    # Retrieve documents
    docs = vectorstore.similarity_search(query, k=3)
    context = "\\n\\n".join([doc.page_content for doc in docs])
    
    # Stream response
    response_container = st.empty()
    stream_handler = StreamHandler(response_container)
    
    # Generate with streaming
    # ... streaming logic
""", language="python")

st.subheader("Error Handling")
st.code("""
def query_rag_system(question):
    try:
        # Validate input
        if not question or len(question) < 3:
            return None, "Please enter a valid question"
        
        # Retrieve documents
        docs = vectorstore.similarity_search(question, k=3)
        
        if not docs:
            return None, "No relevant documents found"
        
        # Generate response
        result = qa_chain({"query": question})
        
        return result, None
        
    except Exception as e:
        return None, f"Error: {str(e)}"

# Usage
result, error = query_rag_system(user_question)

if error:
    st.error(error)
else:
    st.write(result["result"])
""", language="python")

st.subheader("Citation Display")
st.code("""
def display_answer_with_citations(result):
    answer = result["result"]
    sources = result["source_documents"]
    
    # Display answer
    st.markdown("### Answer")
    st.write(answer)
    
    # Display sources
    st.markdown("### Sources")
    for i, doc in enumerate(sources, 1):
        with st.expander(f"📄 Source {i}"):
            st.write(doc.page_content)
            
            # Show metadata
            if doc.metadata:
                st.json(doc.metadata)
""", language="python")

st.markdown("---")
st.info("✅ Build your RAG application!")

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
