import streamlit as st

st.set_page_config(page_title="Day 14 - Practice Project 2", page_icon="1️⃣4️⃣")

st.title("Day 14: Practice Project 2")
st.markdown("**Section 2: Building Chatbots**")
st.markdown("---")

st.header("🎯 Project: Full-Featured Chatbot")
st.markdown("""
Build a complete, production-ready chatbot with all the features you've learned!

### Requirements:
1. ✅ Professional chat interface
2. ✅ Message history with persistence
3. ✅ Context window management
4. ✅ Input validation and sanitization
5. ✅ Customizable personality
6. ✅ User preferences
7. ✅ Streaming responses
8. ✅ Error handling
""")

st.header("📝 Full Implementation Template")

st.code("""
import streamlit as st
from openai import OpenAI
import tiktoken
import json
from datetime import datetime

# Page config
st.set_page_config(page_title="Advanced Chatbot", page_icon="🤖", layout="wide")

# Initialize session state
def init_state():
    defaults = {
        'messages': [],
        'conversation_id': datetime.now().strftime("%Y%m%d_%H%M%S"),
        'total_tokens': 0,
        'user_prefs': {
            'personality': 'Professional',
            'temperature': 0.7,
            'max_tokens': 500
        }
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# Cache LLM client
@st.cache_resource
def get_client():
    return OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

client = get_client()

# System prompts
PERSONALITIES = {
    "Professional": "You are a professional AI assistant. Be clear and concise.",
    "Friendly": "You are a friendly AI companion. Be warm and engaging.",
    "Technical": "You are a technical expert. Provide detailed explanations.",
    "Creative": "You are a creative AI. Think outside the box."
}

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    personality = st.selectbox(
        "Personality",
        list(PERSONALITIES.keys()),
        index=0
    )
    
    temperature = st.slider(
        "Temperature",
        0.0, 2.0,
        st.session_state.user_prefs['temperature'],
        0.1
    )
    
    max_tokens = st.number_input(
        "Max Response Tokens",
        100, 2000,
        st.session_state.user_prefs['max_tokens']
    )
    
    st.divider()
    
    st.subheader("📊 Statistics")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Total Tokens", st.session_state.total_tokens)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.total_tokens = 0
        st.rerun()
    
    if st.button("💾 Export Chat"):
        export_data = {
            'conversation_id': st.session_state.conversation_id,
            'messages': st.session_state.messages,
            'timestamp': datetime.now().isoformat()
        }
        st.download_button(
            "Download JSON",
            json.dumps(export_data, indent=2),
            f"chat_{st.session_state.conversation_id}.json",
            "application/json"
        )

# Main chat interface
st.title("🤖 Advanced Chatbot")
st.caption(f"Conversation ID: {st.session_state.conversation_id}")

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("tokens"):
            st.caption(f"Tokens: {msg['tokens']}")

# Input validation
def validate_input(text):
    if not text or not text.strip():
        return False, "Please enter a message"
    if len(text) > 2000:
        return False, "Message too long (max 2000 characters)"
    return True, ""

# Token counting
def count_tokens(text, model="gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        return len(text.split())

# Context management
def manage_context(messages, max_tokens=3000):
    if len(messages) <= 1:
        return messages
    
    total = 0
    kept_messages = []
    
    for msg in reversed(messages):
        msg_tokens = count_tokens(msg['content'])
        if total + msg_tokens > max_tokens:
            break
        kept_messages.insert(0, msg)
        total += msg_tokens
    
    return kept_messages

# Chat input
if prompt := st.chat_input("Type your message..."):
    is_valid, error_msg = validate_input(prompt)
    
    if not is_valid:
        st.error(error_msg)
    else:
        # Add user message
        user_tokens = count_tokens(prompt)
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "tokens": user_tokens
        })
        st.session_state.total_tokens += user_tokens
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            try:
                # Prepare messages with system prompt
                system_msg = {"role": "system", "content": PERSONALITIES[personality]}
                context_msgs = manage_context(st.session_state.messages)
                api_messages = [system_msg] + context_msgs
                
                # Stream response
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=api_messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True
                )
                
                response = st.write_stream(stream)
                
                # Add to history
                assistant_tokens = count_tokens(response)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "tokens": assistant_tokens
                })
                st.session_state.total_tokens += assistant_tokens
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("💡 Tip: Use the sidebar to customize the bot's behavior")
""", language="python")

st.header("🎨 Enhancement Checklist")

checklist = {
    "Core Features": [
        "Streaming responses",
        "Message history",
        "Context management",
        "Error handling"
    ],
    "Customization": [
        "Multiple personalities",
        "Temperature control",
        "Token limits",
        "Custom avatars"
    ],
    "User Experience": [
        "Input validation",
        "Loading indicators",
        "Token counter",
        "Clear chat button"
    ],
    "Advanced": [
        "Export chat history",
        "Import conversations",
        "Conversation naming",
        "Search in history"
    ]
}

for category, items in checklist.items():
    with st.expander(f"**{category}**"):
        for item in items:
            st.checkbox(item, key=f"check_{category}_{item}")

st.header("🚀 Deployment Preparation")
st.markdown("""
Before deploying your chatbot:

1. **Security**
   - [ ] API keys in secrets
   - [ ] Input sanitization
   - [ ] Rate limiting
   - [ ] Error handling

2. **Performance**
   - [ ] Caching implemented
   - [ ] Context optimization
   - [ ] Token management
   - [ ] Lazy loading

3. **User Experience**
   - [ ] Loading states
   - [ ] Error messages
   - [ ] Mobile responsive
   - [ ] Accessibility

4. **Testing**
   - [ ] Edge cases
   - [ ] Long conversations
   - [ ] Error scenarios
   - [ ] Multiple users
""")

st.markdown("---")
st.success("🎉 Complete this project to finish Section 2!")

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
