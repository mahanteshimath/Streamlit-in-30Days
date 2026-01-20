import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete

st.set_page_config(page_title="Day 11 - Displaying Chat History", page_icon="1️⃣1️⃣", layout="wide")

st.title(":material/history: Day 11: Displaying Chat History")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")

st.code("""
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete

# Get the current credentials
session = get_active_session()

def call_llm(prompt_text: str) -> str:
    \"\"\"Call Snowflake Cortex LLM.\"\"\"
    df = session.range(1).select(
        ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
    )
    response = df.collect()[0][0]
    return response

st.title(":material/chat: Chatbot with History")

# Initialize messages with greeting
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
    ]

# Sidebar to show conversation stats
with st.sidebar:
    st.header("Conversation Stats")
    user_msgs = len([m for m in st.session_state.messages if m["role"] == "user"])
    assistant_msgs = len([m for m in st.session_state.messages if m["role"] == "assistant"])
    st.metric("Your Messages", user_msgs)
    st.metric("AI Responses", assistant_msgs)
    
    if st.button("Clear History"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
        st.rerun()

# Display all messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Build the full conversation history for context
            conversation = "\\n\\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            full_prompt = f"{conversation}\\n\\nAssistant:"
            
            response = call_llm(full_prompt)
        st.markdown(response)
    
    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()

st.divider()
st.caption("Day 11: Displaying Chat History | 30 Days of AI")
""", language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("💬 Try It Yourself!")
st.caption("Using default Snowflake connection - Chat with conversation history!")

try:
    # Get the current credentials
    if 'default_session' not in st.session_state:
        try:
            # Try Streamlit in Snowflake first
            st.session_state.default_session = get_active_session()
        except:
            # Fall back to secrets.toml for local development
            from snowflake.snowpark import Session
            if "connections" in st.secrets and "my_example_connection" in st.secrets["connections"]:
                st.session_state.default_session = Session.builder.configs(
                    st.secrets["connections"]["my_example_connection"]
                ).create()
            else:
                raise Exception("No Snowflake connection configured in secrets.toml")
    
    session = st.session_state.default_session
    st.success("✅ Connected to Snowflake!")
    
    # LLM Function
    def call_llm(prompt_text: str) -> str:
        """Call Snowflake Cortex LLM."""
        df = session.range(1).select(
            ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
        )
        # Get response (ai_complete returns plain text, not JSON)
        response = df.collect()[0][0]
        return response
    
    # Initialize messages with greeting
    if "default_messages_history" not in st.session_state:
        st.session_state.default_messages_history = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
    
    # Sidebar to show conversation stats
    with st.sidebar:
        st.header("📊 Conversation Stats")
        user_msgs = len([m for m in st.session_state.default_messages_history if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.default_messages_history if m["role"] == "assistant"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Messages", user_msgs, delta=None)
        with col2:
            st.metric("AI Responses", assistant_msgs, delta=None)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.default_messages_history = [
                {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
            ]
            st.rerun()
        
        st.markdown("---")
        st.info("💡 **Tip:** The bot remembers your entire conversation for context!")
    
    # Display all messages from history
    for message in st.session_state.default_messages_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        try:
            # Add and display user message
            st.session_state.default_messages_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Build the full conversation history for context
                    conversation = "\n\n".join([
                        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                        for msg in st.session_state.default_messages_history
                    ])
                    full_prompt = f"{conversation}\n\nAssistant:"
                    
                    response = call_llm(full_prompt)
                st.markdown(response)
            
            # Add assistant response to state
            st.session_state.default_messages_history.append({"role": "assistant", "content": response})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            
except Exception as e:
    st.error("""
    ❌ **Connection Failed**
    
    Please configure your Snowflake connection in `.streamlit/secrets.toml`:
    
    ```toml
    [connections.my_example_connection]
    account = "your-account-id"
    user = "your-username"
    password = "your-password"
    role = "ACCOUNTADMIN"
    warehouse = "COMPUTE_WH"
    database = "MH"
    schema = "PUBLIC"
    ```
    
    Or use the **Custom Connection** section below.
    """)
    with st.expander("See error details"):
        st.code(str(e))

st.markdown("---")

# Custom Connection Option
st.header("🔧 Custom Connection (Optional)")

with st.expander("Connect with your own Snowflake account"):
    st.markdown("Enter your Snowflake credentials to connect:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        account = st.text_input("Account", value="JDNLKWD-OZB14673", key="custom_account")
        user = st.text_input("User", value="MONTY", key="custom_user")
        password = st.text_input("Password", type="password", key="custom_password")
        role = st.text_input("Role", value="ACCOUNTADMIN", key="custom_role")
    
    with col2:
        warehouse = st.text_input("Warehouse", value="COMPUTE_WH", key="custom_warehouse")
        database = st.text_input("Database", value="MH", key="custom_database")
        schema = st.text_input("Schema", value="PUBLIC", key="custom_schema")
    
    if st.button("Connect", type="primary", key="custom_connect"):
        if account and user and password and warehouse and database:
            try:
                from snowflake.snowpark import Session
                
                connection_params = {
                    "account": account,
                    "user": user,
                    "password": password,
                    "role": role,
                    "warehouse": warehouse,
                    "database": database,
                    "schema": schema
                }
                
                custom_session = Session.builder.configs(connection_params).create()
                st.success(f"✅ Connected to Snowflake!")
                
                # Store session in session state for reuse
                st.session_state.custom_session = custom_session
                
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")

# Try It Yourself with Custom Connection
if 'custom_session' in st.session_state:
    st.subheader("💬 Try It Yourself!")
    st.caption("Using your custom connection")
    
    # LLM Function for custom session
    def call_llm_custom(prompt_text: str) -> str:
        """Call Snowflake Cortex LLM."""
        df = st.session_state.custom_session.range(1).select(
            ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
        )
        # Get response (ai_complete returns plain text, not JSON)
        response = df.collect()[0][0]
        return response
    
    # Initialize messages with greeting
    if "custom_messages_history" not in st.session_state:
        st.session_state.custom_messages_history = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
    
    # Show stats
    user_msgs = len([m for m in st.session_state.custom_messages_history if m["role"] == "user"])
    assistant_msgs = len([m for m in st.session_state.custom_messages_history if m["role"] == "assistant"])
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.caption(f"👤 Your Messages: {user_msgs}")
    with col2:
        st.caption(f"🤖 AI Responses: {assistant_msgs}")
    with col3:
        if st.button("🗑️ Clear", key="custom_clear"):
            st.session_state.custom_messages_history = [
                {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
            ]
            st.rerun()
    
    # Display all messages from history
    for message in st.session_state.custom_messages_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if custom_prompt := st.chat_input("Type your message...", key="custom_input"):
        try:
            # Add and display user message
            st.session_state.custom_messages_history.append({"role": "user", "content": custom_prompt})
            with st.chat_message("user"):
                st.markdown(custom_prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Build the full conversation history for context
                    conversation = "\n\n".join([
                        f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                        for msg in st.session_state.custom_messages_history
                    ])
                    full_prompt = f"{conversation}\n\nAssistant:"
                    
                    custom_response = call_llm_custom(full_prompt)
                st.markdown(custom_response)
            
            # Add assistant response to state
            st.session_state.custom_messages_history.append({"role": "assistant", "content": custom_response})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Footer
st.divider()
st.caption("Day 11: Displaying Chat History | 30 Days of AI")

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
