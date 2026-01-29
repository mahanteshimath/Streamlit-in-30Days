import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete

st.set_page_config(page_title="Day 2 - Hello, Cortex!", page_icon="2️⃣", layout="wide")

st.title(":material/smart_toy: Day 2: Hello, Cortex!")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code("""
    # Import python packages
    import streamlit as st
    from snowflake.snowpark.context import get_active_session
    from snowflake.snowpark.functions import ai_complete

    # Get the current credentials
    session = get_active_session()

    st.title(":material/smart_toy: Hello, Cortex!")

    # Model and prompt
    model = "claude-3-5-sonnet"
    prompt = st.text_input("Enter your prompt:")

    # Run LLM inference
    if st.button("Generate Response"):
        df = session.range(1).select(
            ai_complete(model=model, prompt=prompt).alias("response")
        )
        
        # Get and display response
        response = df.collect()[0][0]
        st.write(response)

    # Footer
    st.divider()
    st.caption("Day 2: Hello, Cortex! | 30 Days of AI")
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
    model = st.selectbox(
        "Select Model",
        ["claude-3-5-sonnet", "llama3.1-70b", "mistral-large2", "llama3.1-8b"],
        index=0
    )
    
    # Prompt input
    prompt = st.text_input("Enter your prompt:", placeholder="Tell me a joke about data science")
    
    # Generate response
    if st.button("Generate Response", type="primary"):
        if prompt:
            with st.spinner("Generating response..."):
                try:
                    df = session.range(1).select(
                        ai_complete(model=model, prompt=prompt).alias("response")
                    )
                    
                    # Get and display response (ai_complete returns plain text, not JSON)
                    response = df.collect()[0][0]
                    
                    display_response = str(response).replace("\\n", "\n")
                    st.subheader("Response:")
                    with st.container(border=True):
                        st.markdown(display_response)
                    st.text_area("Copy response", value=display_response, height=200)
                    
                    # Show raw response in expander
                    with st.expander("See raw response"):
                        st.code(response)
                        
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
        "Select Model",
        ["claude-3-5-sonnet", "llama3.1-70b", "mistral-large2", "llama3.1-8b"],
        index=0,
        key="custom_model"
    )
    
    # Prompt input for custom
    custom_prompt = st.text_input("Enter your prompt:", placeholder="Tell me a joke about data science", key="custom_prompt")
    
    # Generate response
    if st.button("Generate Response", type="primary", key="custom_generate"):
        if custom_prompt:
            with st.spinner("Generating response..."):
                try:
                    custom_df = st.session_state.custom_session.range(1).select(
                        ai_complete(model=custom_model, prompt=custom_prompt).alias("response")
                    )
                    custom_response = custom_df.collect()[0][0]
                    
                    display_custom_response = str(custom_response).replace("\\n", "\n")
                    st.subheader("Response:")
                    with st.container(border=True):
                        st.markdown(display_custom_response)
                    st.text_area("Copy response", value=display_custom_response, height=200, key="custom_copy")
                    
                    # Show raw response in expander
                    with st.expander("See raw response"):
                        st.code(custom_response)
                        
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
        else:
            st.warning("⚠️ Please enter a prompt")

# Footer
st.divider()
st.caption("Day 2: Hello, Cortex! | 30 Days of AI")

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
