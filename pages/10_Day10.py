import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete

st.set_page_config(page_title="Day 10 - Your First Chatbot", page_icon="🔟", layout="wide")

st.title(":material/chat: Day 10: Your First Chatbot")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    snippet = '''
import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

def call_llm(prompt_text: str) -> str:
    # Call Snowflake Cortex LLM.
    df = session.range(1).select(
        ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
    )
    response_raw = df.collect()[0][0]
    try:
        response_json = json.loads(response_raw)
        if isinstance(response_json, dict):
            return response_json.get("choices", [{}])[0].get("messages", "")
        return str(response_json)
    except Exception:
        return str(response_raw)

st.title(":material/chat: My First Chatbot")

# Initialize the messages list in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display all messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Generate and display assistant response
    with st.chat_message("assistant"):
        response = call_llm(prompt)
        st.write(response)
    
    # Add assistant response to state
    st.session_state.messages.append({"role": "assistant", "content": response})

st.divider()
st.caption("Day 10: Your First Chatbot (with State) | 30 Days of AI")
    '''
    st.code(snippet, language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("💬 Try It Yourself!")
st.caption("Using default Snowflake connection - Your messages persist in session state!")

try:
    # Get the current credentials (Snowflake first, then secrets fallback)
    if "default_session" not in st.session_state:
        try:
            from snowflake.snowpark.context import get_active_session
            st.session_state.default_session = get_active_session()
        except Exception:
            from snowflake.snowpark import Session
            st.session_state.default_session = Session.builder.configs(
                st.secrets["connections"]["snowflake"]
            ).create()

    session = st.session_state.default_session
    st.success("✅ Connected to Snowflake!")

    def call_llm(prompt_text: str) -> str:
        """Call Snowflake Cortex LLM with JSON-safe parsing."""
        df = session.range(1).select(
            ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
        )
        response_raw = df.collect()[0][0]
        try:
            response_json = json.loads(response_raw)
            if isinstance(response_json, dict):
                return response_json.get("choices", [{}])[0].get("messages", "")
            return str(response_json)
        except Exception:
            return str(response_raw)

    # Initialize the messages list in session state
    if "default_messages" not in st.session_state:
        st.session_state.default_messages = []
    
    # Sidebar with controls
    with st.sidebar:
        st.header("🎛️ Chat Controls")
        st.metric("Messages", len(st.session_state.default_messages))
        
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.default_messages = []
            st.rerun()
        
        st.markdown("---")
        st.info("💡 **Tip:** Your chat history is stored in session state and persists across interactions!")
    
    # Display all messages from history
    for message in st.session_state.default_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        try:
            # Add user message to state
            st.session_state.default_messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user"):
                st.write(prompt)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = call_llm(prompt)
                st.write(response)
            
            # Add assistant response to state
            st.session_state.default_messages.append({"role": "assistant", "content": response})
            
            # Rerun to update message count in sidebar
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
        response_raw = df.collect()[0][0]
        try:
            response_json = json.loads(response_raw)
            if isinstance(response_json, dict):
                return response_json.get("choices", [{}])[0].get("messages", "")
            return str(response_json)
        except Exception:
            return str(response_raw)
    
    # Initialize the messages list in session state
    if "custom_messages" not in st.session_state:
        st.session_state.custom_messages = []
    
    # Display all messages
    for message in st.session_state.custom_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if custom_prompt := st.chat_input("What would you like to know?", key="custom_input"):
        try:
            st.session_state.custom_messages.append({"role": "user", "content": custom_prompt})
            with st.chat_message("user"):
                st.write(custom_prompt)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    custom_response = call_llm_custom(custom_prompt)
                st.write(custom_response)
            st.session_state.custom_messages.append({"role": "assistant", "content": custom_response})
            st.rerun()
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Footer
st.divider()
st.caption("Day 10: Your First Chatbot (with State) | 30 Days of AI")


