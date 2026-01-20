import streamlit as st

st.set_page_config(page_title="Day 13 - Chatbot Customization", page_icon="1️⃣3️⃣")

st.title("Day 13: Chatbot Customization")
st.markdown("**Section 2: Building Chatbots**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Customize chat appearance
- Add system prompts
- Personality configuration
- User preferences
""")

st.header("📖 Content")

st.subheader("System Prompts")
st.markdown("Define your chatbot's personality and behavior:")

st.code("""
# Predefined personalities
PERSONALITIES = {
    "Professional": "You are a professional assistant. Be formal and concise.",
    "Friendly": "You are a friendly helper. Be warm and conversational.",
    "Teacher": "You are a patient teacher. Explain things clearly.",
    "Coding Expert": "You are an expert programmer. Provide code examples."
}

# Let user select personality
personality = st.selectbox("Bot Personality", PERSONALITIES.keys())
system_prompt = PERSONALITIES[personality]

# Use in messages
messages = [
    {"role": "system", "content": system_prompt},
    *st.session_state.messages
]
""", language="python")

st.subheader("Interactive Demo")

if 'custom_messages' not in st.session_state:
    st.session_state.custom_messages = []

# Customization sidebar
with st.sidebar:
    st.header("⚙️ Customization")
    
    personality = st.selectbox(
        "Personality",
        ["Professional", "Friendly", "Teacher", "Technical"]
    )
    
    temperature = st.slider("Creativity", 0.0, 2.0, 0.7)
    
    max_tokens = st.number_input("Max Response Length", 50, 1000, 150)
    
    show_tokens = st.checkbox("Show token count")
    
    st.divider()
    
    avatar_user = st.text_input("User Avatar", "👤")
    avatar_bot = st.text_input("Bot Avatar", "🤖")
    
    st.divider()
    
    st.caption("Theme & Style")
    message_style = st.radio("Message Style", ["Default", "Compact", "Detailed"])

# Display current settings
st.write("**Current Configuration:**")
config_col1, config_col2, config_col3 = st.columns(3)
with config_col1:
    st.metric("Personality", personality)
with config_col2:
    st.metric("Creativity", f"{temperature:.1f}")
with config_col3:
    st.metric("Max Tokens", max_tokens)

st.subheader("Custom Styling")
st.code("""
# Custom CSS for chat messages
st.markdown(\"\"\"
<style>
.stChatMessage {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 0.5rem;
}

.stChatMessage[data-role="user"] {
    background-color: #e3f2fd;
}

.stChatMessage[data-role="assistant"] {
    background-color: #f5f5f5;
}
</style>
\"\"\", unsafe_allow_html=True)
""", language="python")

st.subheader("User Preferences")
st.code("""
# Save user preferences
def save_preferences():
    prefs = {
        'personality': personality,
        'temperature': temperature,
        'theme': selected_theme,
        'avatar': selected_avatar
    }
    
    # Save to session state
    st.session_state.user_prefs = prefs
    
    # Optionally save to file/database
    import json
    with open('user_prefs.json', 'w') as f:
        json.dump(prefs, f)

def load_preferences():
    try:
        with open('user_prefs.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Load on startup
if 'user_prefs' not in st.session_state:
    st.session_state.user_prefs = load_preferences()
""", language="python")

st.subheader("Advanced Features")
st.code("""
# Feature toggles
features = {
    'code_execution': st.checkbox("Enable Code Execution"),
    'web_search': st.checkbox("Enable Web Search"),
    'image_generation': st.checkbox("Enable Image Generation"),
    'voice_input': st.checkbox("Enable Voice Input")
}

# Conditional functionality
if features['code_execution']:
    # Add code execution capability
    pass

# Export settings
if st.button("Export Settings"):
    settings_json = json.dumps(features, indent=2)
    st.download_button(
        "Download Settings",
        settings_json,
        "chatbot_settings.json"
    )
""", language="python")

st.markdown("---")
st.info("✅ Create unique chatbot experiences!")

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
