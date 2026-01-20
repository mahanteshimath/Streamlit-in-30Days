import streamlit as st

st.set_page_config(page_title="Day 12 - Conversation Context", page_icon="1️⃣2️⃣")

st.title("Day 12: Conversation Context")
st.markdown("**Section 2: Building Chatbots**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Maintain conversation context
- Manage message windows
- Context truncation strategies
- Memory management
""")

st.header("📖 Content")

st.subheader("Context Window Management")
st.markdown("""
LLMs have token limits. You need to manage the conversation context to stay within limits.

**Common Limits:**
- GPT-3.5-turbo: 4,096 tokens
- GPT-4: 8,192 tokens
- GPT-4-32k: 32,768 tokens
""")

st.code("""
def get_context_window(messages, max_messages=10):
    # Keep only the last N messages
    return messages[-max_messages:]

def get_token_count(messages):
    # Approximate token count
    # More accurate: use tiktoken library
    total = 0
    for msg in messages:
        total += len(msg['content'].split())
    return total * 1.3  # Rough approximation

# Usage
context = get_context_window(st.session_state.messages)
token_count = get_token_count(context)

if token_count > 3000:
    st.warning("Approaching token limit!")
""", language="python")

st.subheader("Context Strategies")

st.markdown("**Strategy 1: Sliding Window**")
st.code("""
# Keep last N messages
MAX_MESSAGES = 20

if len(st.session_state.messages) > MAX_MESSAGES:
    # Keep system message + recent messages
    system_msg = st.session_state.messages[0]
    recent = st.session_state.messages[-MAX_MESSAGES:]
    st.session_state.messages = [system_msg] + recent
""", language="python")

st.markdown("**Strategy 2: Token-Based Truncation**")
st.code("""
import tiktoken

def truncate_by_tokens(messages, max_tokens=3000):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    total_tokens = 0
    truncated = []
    
    # Process messages in reverse (keep recent ones)
    for msg in reversed(messages):
        msg_tokens = len(encoding.encode(msg['content']))
        
        if total_tokens + msg_tokens > max_tokens:
            break
        
        truncated.insert(0, msg)
        total_tokens += msg_tokens
    
    return truncated
""", language="python")

st.markdown("**Strategy 3: Summarization**")
st.code("""
def summarize_old_context(messages):
    if len(messages) > 20:
        # Summarize old messages
        old_msgs = messages[:10]
        summary_prompt = "Summarize this conversation: " + str(old_msgs)
        
        summary = get_llm_summary(summary_prompt)
        
        # Replace old messages with summary
        summary_msg = {
            "role": "system",
            "content": f"Previous conversation summary: {summary}"
        }
        
        return [summary_msg] + messages[10:]
    
    return messages
""", language="python")

st.subheader("Demo: Context Window")

if 'context_demo' not in st.session_state:
    st.session_state.context_demo = []

col1, col2 = st.columns([3, 1])

with col1:
    if st.button("Add Message"):
        st.session_state.context_demo.append(
            f"Message {len(st.session_state.context_demo) + 1}"
        )

with col2:
    max_window = st.number_input("Window Size", 1, 20, 5)

# Show all messages
st.write("**Full History:**", len(st.session_state.context_demo), "messages")

# Show windowed messages
context_window = st.session_state.context_demo[-max_window:]
st.write("**Context Window:**")
for msg in context_window:
    st.caption(f"• {msg}")

if st.button("Clear Demo"):
    st.session_state.context_demo = []
    st.rerun()

st.markdown("---")
st.info("✅ Build context-aware chatbots!")

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
