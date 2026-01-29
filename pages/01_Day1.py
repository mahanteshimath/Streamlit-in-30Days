import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Day 1 - Connect to Snowflake", page_icon="1️⃣", layout="wide")

st.title(":material/vpn_key: Day 1: Connect with Snowflake")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code("""
    # Import python packages
    import streamlit as st
    from snowflake.snowpark.context import get_active_session

    # Get the current credentials
    session = get_active_session()

    # Query and display Snowflake version
    version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]

    # Show results
    st.success(f"Successfully connected! Snowflake Version: {version}")
    """, language="python")

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
    
    # Query and display Snowflake version
    version = session.sql("SELECT CURRENT_VERSION()").collect()[0][0]
    
    # Show results
    st.success(f"✅ Successfully connected! Snowflake Version: {version}")
    
    # Additional info
    col1, col2, col3 = st.columns(3)
    with col1:
        current_user = session.sql("SELECT CURRENT_USER()").collect()[0][0]
        st.metric("User", current_user)
    with col2:
        current_role = session.sql("SELECT CURRENT_ROLE()").collect()[0][0]
        st.metric("Role", current_role)
    with col3:
        current_warehouse = session.sql("SELECT CURRENT_WAREHOUSE()").collect()[0][0]
        st.metric("Warehouse", current_warehouse)
        
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
        account = st.text_input("Account", value="JDNLKWD-OZB14673")
        user = st.text_input("User", value="Monty")
        password = st.text_input("Password", type="password")
        role = st.text_input("Role", value="ACCOUNTADMIN")
    
    with col2:
        warehouse = st.text_input("Warehouse", value="COMPUTE_WH")
        database = st.text_input("Database", value="MH")
        schema = st.text_input("Schema", value="PUBLIC")
    
    if st.button("Connect", type="primary"):
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
                
                # Query version
                version = custom_session.sql("SELECT CURRENT_VERSION()").collect()[0][0]
                st.success(f"✅ Connected! Snowflake Version: {version}")
                
                # Show connection info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("User", user)
                with col2:
                    st.metric("Role", role)
                with col3:
                    st.metric("Warehouse", warehouse)
                
                custom_session.close()
                
            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")

# Footer
st.divider()
st.caption("Day 1: Connect with Snowflake | 30 Days of AI")

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
