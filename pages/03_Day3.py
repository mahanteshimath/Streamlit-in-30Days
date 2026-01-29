import streamlit as st
import time
from snowflake.snowpark.context import get_active_session
from snowflake.cortex import complete

st.set_page_config(page_title="Day 3 - Write Streams", page_icon="3️⃣", layout="wide")

st.title(":material/stream: Day 3: Write Streams")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code("""
    # Import python packages
    import streamlit as st
    import time
    from snowflake.snowpark.context import get_active_session
    from snowflake.cortex import complete

    # Get the current credentials
    session = get_active_session()

    llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
    model = st.selectbox("Select a model", llm_models)

    example_prompt = "What is Python?"
    prompt = st.text_area("Enter prompt", example_prompt)

    # Choose streaming method
    streaming_method = st.radio(
        "Streaming Method:",
        ["Direct (stream=True)", "Custom Generator"],
        help="Choose how to stream the response"
    )

    if st.button("Generate Response"):
        # Method 1: Direct streaming with stream=True
        if streaming_method == "Direct (stream=True)":
            with st.spinner(f"Generating response with `{model}`"):
                stream_generator = complete(
                    session=session,
                    model=model,
                    prompt=prompt,
                    stream=True,
                )
                st.write_stream(stream_generator)
        
        else:
            # Method 2: Custom generator (for compatibility)
            def custom_stream_generator():
                output = complete(
                    session=session,
                    model=model,
                    prompt=prompt
                )
                for chunk in output:
                    yield chunk
                    time.sleep(0.01)  # Small delay for smooth streaming
            
            with st.spinner(f"Generating response with `{model}`"):
                st.write_stream(custom_stream_generator)

    # Footer
    st.divider()
    st.caption("Day 3: Write streams | 30 Days of AI")
    """, language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("💬 Try It Yourself!")
st.caption("Using default Snowflake connection")

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
    
    # Model selection
    llm_models = ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
    model = st.selectbox("Select a model", llm_models, index=0)
    
    # Prompt input
    example_prompt = "What is Python?"
    prompt = st.text_area("Enter prompt", example_prompt, height=100)
    
    # Choose streaming method
    streaming_method = st.radio(
        "Streaming Method:",
        ["Direct (stream=True)", "Custom Generator"],
        help="Choose how to stream the response"
    )
    
    # Generate response
    if st.button("Generate Response", type="primary"):
        if prompt:
            try:
                # Method 1: Direct streaming with stream=True
                if streaming_method == "Direct (stream=True)":
                    with st.spinner(f"Generating response with `{model}`"):
                        stream_generator = complete(
                            session=session,
                            model=model,
                            prompt=prompt,
                            stream=True,
                        )
                        
                        st.subheader("Response:")
                        st.write_stream(stream_generator)
                
                else:
                    # Method 2: Custom generator (for compatibility)
                    def custom_stream_generator():
                        """
                        Alternative streaming method for cases where
                        the generator is not compatible with st.write_stream
                        """
                        output = complete(
                            session=session,
                            model=model,
                            prompt=prompt
                        )
                        for chunk in output:
                            yield chunk
                            time.sleep(0.01)  # Small delay for smooth streaming
                    
                    with st.spinner(f"Generating response with `{model}`"):
                        st.subheader("Response:")
                        st.write_stream(custom_stream_generator)
                        
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt")
            
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
    
    # Model selection for custom
    custom_model = st.selectbox(
        "Select a model",
        ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"],
        index=0,
        key="custom_model"
    )
    
    # Prompt input for custom
    custom_prompt = st.text_area("Enter prompt", "What is Python?", height=100, key="custom_prompt")
    
    # Streaming method for custom
    custom_streaming_method = st.radio(
        "Streaming Method:",
        ["Direct (stream=True)", "Custom Generator"],
        help="Choose how to stream the response",
        key="custom_streaming_method"
    )
    
    # Generate response
    if st.button("Generate Response", type="primary", key="custom_generate"):
        if custom_prompt:
            try:
                if custom_streaming_method == "Direct (stream=True)":
                    with st.spinner(f"Generating response with `{custom_model}`"):
                        custom_stream_generator = complete(
                            session=st.session_state.custom_session,
                            model=custom_model,
                            prompt=custom_prompt,
                            stream=True,
                        )
                        
                        st.subheader("Response:")
                        st.write_stream(custom_stream_generator)
                
                else:
                    def custom_generator():
                        output = complete(
                            session=st.session_state.custom_session,
                            model=custom_model,
                            prompt=custom_prompt
                        )
                        for chunk in output:
                            yield chunk
                            time.sleep(0.01)
                    
                    with st.spinner(f"Generating response with `{custom_model}`"):
                        st.subheader("Response:")
                        st.write_stream(custom_generator)
                        
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt")

# Footer
st.divider()
st.caption("Day 3: Write streams | 30 Days of AI")

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
