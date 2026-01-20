import streamlit as st

st.set_page_config(page_title="Day 25 - Testing & Debugging", page_icon="2️⃣5️⃣")

st.title("Day 25: Testing & Debugging")
st.markdown("**Section 4: Advanced Features**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Unit testing Streamlit apps
- Debugging techniques
- Logging best practices
- Error handling patterns
""")

st.header("📖 Content")

st.subheader("Testing Streamlit Apps")
st.code("""
# test_app.py
from streamlit.testing.v1 import AppTest

def test_app():
    # Initialize app
    at = AppTest.from_file("app.py")
    at.run()
    
    # Test initial state
    assert at.title[0].value == "My App"
    
    # Interact with widgets
    at.text_input[0].set_value("test input")
    at.button[0].click()
    at.run()
    
    # Check results
    assert "expected output" in at.markdown[0].value

# Run tests
# pytest test_app.py
""", language="python")

st.subheader("Unit Testing Functions")
st.code("""
# app_functions.py
def process_data(text):
    return text.upper()

# test_functions.py
import pytest
from app_functions import process_data

def test_process_data():
    assert process_data("hello") == "HELLO"
    assert process_data("") == ""
    
def test_process_data_error():
    with pytest.raises(AttributeError):
        process_data(None)

# Mock API calls
from unittest.mock import patch, MagicMock

@patch('openai.ChatCompletion.create')
def test_llm_call(mock_create):
    mock_create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="Test response"))]
    )
    
    result = call_llm("test prompt")
    assert result == "Test response"
""", language="python")

st.subheader("Debugging Techniques")
st.code("""
# 1. Use st.write for debugging
st.write("Debug:", variable)
st.write("Session State:", st.session_state)

# 2. Expander for debug info
with st.expander("🐛 Debug Info"):
    st.json(st.session_state.to_dict())
    st.write("Variables:", locals())

# 3. Try-except with details
try:
    result = risky_operation()
except Exception as e:
    st.error(f"Error: {e}")
    st.exception(e)  # Shows full traceback
    
    # Log for debugging
    import traceback
    st.code(traceback.format_exc())

# 4. Conditional debugging
DEBUG = st.sidebar.checkbox("Debug Mode")

if DEBUG:
    st.sidebar.json({
        "state": dict(st.session_state),
        "query_params": st.experimental_get_query_params()
    })
""", language="python")

st.subheader("Logging")
st.code("""
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)

# Use in app
def process_query(query):
    logger.info(f"Processing query: {query}")
    
    try:
        result = llm.generate(query)
        logger.info("Query processed successfully")
        return result
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        raise

# View logs in Streamlit
if st.checkbox("Show Logs"):
    with open('app.log', 'r') as f:
        st.code(f.read())
""", language="python")

st.subheader("Error Handling Patterns")
st.code("""
# Pattern 1: Graceful degradation
def get_llm_response(prompt):
    try:
        return llm.generate(prompt)
    except ConnectionError:
        st.warning("Connection issue. Using cached response.")
        return get_cached_response(prompt)
    except Exception as e:
        st.error("Unexpected error. Please try again.")
        logger.error(f"LLM error: {e}")
        return None

# Pattern 2: User-friendly errors
def display_error(error_type, details=None):
    error_messages = {
        'api_key': "❌ Invalid API key. Check your settings.",
        'rate_limit': "⏱️ Rate limit reached. Please wait.",
        'network': "🌐 Network error. Check your connection.",
        'unknown': "❓ Something went wrong. Try again."
    }
    
    st.error(error_messages.get(error_type, error_messages['unknown']))
    
    if details and st.checkbox("Show details"):
        st.code(str(details))

# Pattern 3: Retry logic
from time import sleep

def retry_operation(func, max_attempts=3, delay=1):
    for attempt in range(max_attempts):
        try:
            return func()
        except Exception as e:
            if attempt == max_attempts - 1:
                raise
            st.warning(f"Attempt {attempt + 1} failed. Retrying...")
            sleep(delay)
""", language="python")

st.subheader("Performance Monitoring")
st.code("""
import time

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def measure(self, name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                
                if name not in self.metrics:
                    self.metrics[name] = []
                self.metrics[name].append(duration)
                
                return result
            return wrapper
        return decorator
    
    def display(self):
        st.subheader("Performance Metrics")
        for name, times in self.metrics.items():
            avg = sum(times) / len(times)
            st.metric(name, f"{avg:.3f}s", f"{len(times)} calls")

# Usage
monitor = PerformanceMonitor()

@monitor.measure("llm_call")
def call_llm(prompt):
    return llm.generate(prompt)

# Display metrics
if st.checkbox("Show Performance"):
    monitor.display()
""", language="python")

st.markdown("---")
st.info("✅ Ensure app quality!")

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
