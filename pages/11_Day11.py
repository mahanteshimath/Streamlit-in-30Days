import streamlit as st

st.set_page_config(page_title="Day 11 - User Input", page_icon="1️⃣1️⃣")

st.title("Day 11: User Input Handling")
st.markdown("**Section 2: Building Chatbots**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Validate user input
- Handle different input types
- Error handling
- Input sanitization
""")

st.header("📖 Content")

st.subheader("Input Validation")
st.code("""
def validate_input(text):
    if not text or text.strip() == "":
        return False, "Input cannot be empty"
    
    if len(text) > 1000:
        return False, "Input too long (max 1000 characters)"
    
    if any(char in text for char in ['<', '>', '{', '}']):
        return False, "Input contains invalid characters"
    
    return True, "Valid"

if prompt := st.chat_input("Your message"):
    is_valid, message = validate_input(prompt)
    
    if is_valid:
        # Process the input
        st.success("Message sent!")
    else:
        st.error(message)
""", language="python")

st.subheader("Interactive Validation Demo")

demo_input = st.text_area("Try entering text:", max_chars=200)

if demo_input:
    if len(demo_input) < 3:
        st.warning("⚠️ Input too short (minimum 3 characters)")
    elif len(demo_input) > 200:
        st.error("❌ Input too long (maximum 200 characters)")
    else:
        st.success(f"✅ Valid input ({len(demo_input)} characters)")

st.subheader("Sanitization")
st.code("""
import re

def sanitize_input(text):
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters (optional)
    text = re.sub(r'[^\w\s.,!?-]', '', text)
    
    return text

user_input = sanitize_input(prompt)
""", language="python")

st.subheader("Rate Limiting")
st.code("""
import time

# Initialize rate limit state
if 'last_request_time' not in st.session_state:
    st.session_state.last_request_time = 0
    st.session_state.request_count = 0

def check_rate_limit():
    current_time = time.time()
    time_diff = current_time - st.session_state.last_request_time
    
    # Reset counter if more than 60 seconds passed
    if time_diff > 60:
        st.session_state.request_count = 0
    
    # Check if limit exceeded (e.g., 10 requests per minute)
    if st.session_state.request_count >= 10:
        return False, "Rate limit exceeded. Please wait."
    
    st.session_state.request_count += 1
    st.session_state.last_request_time = current_time
    return True, "OK"

# Usage
if prompt := st.chat_input("Message"):
    allowed, msg = check_rate_limit()
    if allowed:
        # Process message
        pass
    else:
        st.error(msg)
""", language="python")

st.subheader("Error Handling")
st.code("""
def process_message(prompt):
    try:
        # Validate
        if not prompt:
            raise ValueError("Empty input")
        
        # Sanitize
        clean_prompt = sanitize_input(prompt)
        
        # Process
        response = call_llm(clean_prompt)
        return response
        
    except ValueError as e:
        st.error(f"Validation error: {e}")
    except ConnectionError as e:
        st.error(f"Connection error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        # Log error for debugging
        print(f"Error processing message: {e}")
    
    return None
""", language="python")

st.markdown("---")
st.info("✅ Learn to handle user input securely!")

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
