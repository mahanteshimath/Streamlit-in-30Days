import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete
import time

st.set_page_config(page_title="Day 12 - Streaming Responses", page_icon="1️⃣2️⃣", layout="wide")

st.title(":material/stream: Day 12: Streaming Responses")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code("""
    import streamlit as st
    from snowflake.snowpark.context import get_active_session
    from snowflake.snowpark.functions import ai_complete
    import time

    # Get the current credentials
    session = get_active_session()

    def call_llm(prompt_text: str) -> str:
        \"\"\"Call Snowflake Cortex LLM.\"\"\"
        df = session.range(1).select(
            ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
        )
        response = df.collect()[0][0]
        return response

    st.title(":material/chat: Chatbot with Streaming")

    # Initialize messages
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
        
        # Build the full conversation history for context
        conversation = "\\n\\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
            for msg in st.session_state.messages
        ])
        full_prompt = f"{conversation}\\n\\nAssistant:"
        
        # Generate stream
        def stream_generator():
            response_text = call_llm(full_prompt)
            for word in response_text.split(" "):
                yield word + " "
                time.sleep(0.02)
        
        # Display assistant response with streaming
        with st.chat_message("assistant"):
            with st.spinner("Processing"):
                response = st.write_stream(stream_generator)
        
        # Add assistant response to state
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.divider()
    st.caption("Day 12: Streaming Responses | 30 Days of AI")
    """, language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("💬 Try It Yourself!")
st.caption("Using default Snowflake connection - Chat with streaming responses!")

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
        # Clean up response: remove escaped newlines and surrounding quotes
        response = str(response).replace("\\n", "\n").strip()
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        return response
    
    # Initialize messages
    if "default_messages_stream" not in st.session_state:
        st.session_state.default_messages_stream = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
    
    # Sidebar to show conversation stats
    with st.sidebar:
        st.header("📊 Conversation Stats")
        user_msgs = len([m for m in st.session_state.default_messages_stream if m["role"] == "user"])
        assistant_msgs = len([m for m in st.session_state.default_messages_stream if m["role"] == "assistant"])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Your Messages", user_msgs, delta=None)
        with col2:
            st.metric("AI Responses", assistant_msgs, delta=None)
        
        st.markdown("---")
        
        if st.button("🗑️ Clear History", type="secondary"):
            st.session_state.default_messages_stream = [
                {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
            ]
            st.rerun()
        
        st.markdown("---")
        st.info("💡 **Tip:** Watch the responses stream word by word for a better UX!")
    
    # Display all messages from history
    for message in st.session_state.default_messages_stream:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message..."):
        try:
            # Add and display user message
            st.session_state.default_messages_stream.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Build the full conversation history for context
            conversation = "\n\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in st.session_state.default_messages_stream
            ])
            full_prompt = f"{conversation}\n\nAssistant:"
            
            # Generate stream
            def stream_generator():
                response_text = call_llm(full_prompt)
                for word in response_text.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            
            # Display assistant response with streaming
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    response = st.write_stream(stream_generator)
            
            # Clean up response before storing
            response = str(response).replace("\\n", "\n").strip()
            if response.startswith('"') and response.endswith('"'):
                response = response[1:-1]
            
            # Add assistant response to state
            st.session_state.default_messages_stream.append({"role": "assistant", "content": response})
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
        # Clean up response: remove escaped newlines and surrounding quotes
        response = str(response).replace("\\n", "\n").strip()
        if response.startswith('"') and response.endswith('"'):
            response = response[1:-1]
        return response
    
    # Initialize messages
    if "custom_messages_stream" not in st.session_state:
        st.session_state.custom_messages_stream = [
            {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
        ]
    
    # Show stats
    user_msgs = len([m for m in st.session_state.custom_messages_stream if m["role"] == "user"])
    assistant_msgs = len([m for m in st.session_state.custom_messages_stream if m["role"] == "assistant"])
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.caption(f"👤 Your Messages: {user_msgs}")
    with col2:
        st.caption(f"🤖 AI Responses: {assistant_msgs}")
    with col3:
        if st.button("🗑️ Clear", key="custom_clear"):
            st.session_state.custom_messages_stream = [
                {"role": "assistant", "content": "Hello! I'm your AI assistant. How can I help you today?"}
            ]
            st.rerun()
    
    # Display all messages from history
    for message in st.session_state.custom_messages_stream:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if custom_prompt := st.chat_input("Type your message...", key="custom_input"):
        try:
            # Add and display user message
            st.session_state.custom_messages_stream.append({"role": "user", "content": custom_prompt})
            with st.chat_message("user"):
                st.markdown(custom_prompt)
            
            # Build the full conversation history for context
            conversation = "\n\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in st.session_state.custom_messages_stream
            ])
            full_prompt = f"{conversation}\n\nAssistant:"
            
            # Generate stream
            def stream_generator_custom():
                response_text = call_llm_custom(full_prompt)
                for word in response_text.split(" "):
                    yield word + " "
                    time.sleep(0.02)
            
            # Display assistant response with streaming
            with st.chat_message("assistant"):
                with st.spinner("Processing..."):
                    custom_response = st.write_stream(stream_generator_custom)
            
            # Clean up response before storing
            custom_response = str(custom_response).replace("\\n", "\n").strip()
            if custom_response.startswith('"') and custom_response.endswith('"'):
                custom_response = custom_response[1:-1]
            
            # Add assistant response to state
            st.session_state.custom_messages_stream.append({"role": "assistant", "content": custom_response})
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Footer
st.divider()
st.caption("Day 12: Streaming Responses | 30 Days of AI")
