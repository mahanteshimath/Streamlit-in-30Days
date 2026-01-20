import streamlit as st

st.set_page_config(page_title="Day 16 - Document Processing", page_icon="1️⃣6️⃣")

st.title("Day 16: Document Processing")
st.markdown("**Section 3: RAG Applications**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Load various document types
- Text extraction techniques
- Document chunking strategies
- Preprocessing best practices
""")

st.header("📖 Content")

st.subheader("Loading Documents")
st.code("""
from langchain.document_loaders import (
    TextLoader,
    PDFLoader,
    CSVLoader,
    UnstructuredMarkdownLoader
)

# Load different file types
txt_loader = TextLoader("document.txt")
pdf_loader = PDFLoader("document.pdf")
csv_loader = CSVLoader("data.csv")

documents = txt_loader.load()
""", language="python")

st.subheader("File Upload in Streamlit")
st.code("""
uploaded_file = st.file_uploader(
    "Upload a document",
    type=["txt", "pdf", "docx", "md"]
)

if uploaded_file:
    # Read file content
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode()
    elif uploaded_file.type == "application/pdf":
        # Use PyPDF2 or pdfplumber
        import pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            content = ""
            for page in pdf.pages:
                content += page.extract_text()
    
    st.success(f"Loaded {len(content)} characters")
""", language="python")

st.subheader("Text Chunking")
st.markdown("Split documents into smaller, overlapping chunks:")

st.code("""
from langchain.text_splitter import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Characters per chunk
    chunk_overlap=200,     # Overlap between chunks
    length_function=len,
    separators=["\\n\\n", "\\n", " ", ""]
)

chunks = text_splitter.split_text(document_text)
st.write(f"Created {len(chunks)} chunks")
""", language="python")

st.subheader("Chunking Strategies")
st.markdown("""
| Strategy | Chunk Size | Overlap | Best For |
|----------|------------|---------|----------|
| Small | 200-500 | 50-100 | Precise retrieval |
| Medium | 500-1000 | 100-200 | General Q&A |
| Large | 1000-2000 | 200-400 | Context-heavy |
| Semantic | Variable | Smart | Coherent sections |
""")

st.subheader("Preprocessing")
st.code("""
import re

def preprocess_text(text):
    # Remove extra whitespace
    text = re.sub(r'\\s+', ' ', text)
    
    # Remove special characters (optional)
    # text = re.sub(r'[^\\w\\s.,!?-]', '', text)
    
    # Normalize case (optional)
    # text = text.lower()
    
    return text.strip()

# Apply to chunks
processed_chunks = [preprocess_text(chunk) for chunk in chunks]
""", language="python")

st.markdown("---")
st.info("✅ Master document processing!")

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
