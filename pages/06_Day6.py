import streamlit as st
import time
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete

st.set_page_config(page_title="Day 6 - Status UI", page_icon="6️⃣", layout="wide")

st.title(":material/pending_actions: Day 6: Status UI for Long-Running Tasks")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")

st.code("""
import streamlit as st
import time
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete

# Get the current credentials
session = get_active_session()

# Cached LLM Function
@st.cache_data
def call_cortex_llm(prompt_text):
    \"\"\"Makes a call to Cortex AI with the given prompt.\"\"\"
    model = "claude-3-5-sonnet"
    df = session.range(1).select(
        ai_complete(model=model, prompt=prompt_text).alias("response")
    )
    
    # Get response (ai_complete returns plain text)
    response = df.collect()[0][0]
    return response

# --- App UI ---
st.title(":material/post_add: LinkedIn Post Generator v2")

# Input widgets
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

# Generate button
if st.button("Generate Post"):
    
    # Initialize the status container
    with st.status("Starting engine...", expanded=True) as status:
        
        # Step 1: Construct Prompt
        st.write(":material/psychology: Thinking: Analyzing constraints and tone...")
        prompt = f\"\"\"
        You are an expert social media manager. Generate a LinkedIn post based on the following:

        Tone: {tone}
        Desired Length: Approximately {word_count} words
        Use content from this URL: {content}

        Generate only the LinkedIn post text. Use dash for bullet points.
        \"\"\"
        
        # Step 2: Call API
        st.write(":material/flash_on: Generating: contacting Snowflake Cortex...")
        
        # This is the blocking call that takes time
        response = call_cortex_llm(prompt)
        
        # Step 3: Update Status to Complete
        st.write(":material/check_circle: Post generation completed!")
        status.update(label="Post Generated Successfully!", state="complete", expanded=False)

    # Display Result
    st.subheader("Generated Post:")
    st.markdown(response)

# Footer
st.divider()
st.caption("Day 6: Status UI for Long-Running Task | 30 Days of AI")
""", language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("💬 Try It Yourself!")
st.caption("Using default Snowflake connection - Watch the status updates!")

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
    
    # Cached LLM Function
    @st.cache_data
    def call_cortex_llm(prompt_text):
        """Makes a call to Cortex AI with the given prompt."""
        model = "claude-3-5-sonnet"
        df = session.range(1).select(
            ai_complete(model=model, prompt=prompt_text).alias("response")
        )
        
        # Get response (ai_complete returns plain text, not JSON)
        response = df.collect()[0][0]
        return response
    
    # Input widgets
    col1, col2 = st.columns([2, 1])
    
    with col1:
        content = st.text_input(
            "Content URL:", 
            "https://docs.snowflake.com/en/user-guide/views-semantic/overview",
            key="default_content"
        )
    
    with col2:
        tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"], key="default_tone")
    
    word_count = st.slider("Approximate word count:", 50, 300, 100, key="default_word_count")
    
    # Generate button
    if st.button("Generate Post", type="primary"):
        if content:
            try:
                # Initialize the status container
                with st.status("Starting engine...", expanded=True) as status:
                    
                    # Step 1: Construct Prompt
                    st.write(":material/psychology: **Thinking:** Analyzing constraints and tone...")
                    time.sleep(0.5)  # Brief pause for UX
                    
                    prompt = f"""
    You are an expert social media manager. Generate a LinkedIn post based on the following:

    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL: {content}

    Generate only the LinkedIn post text. Use dash for bullet points.
    """
                    
                    # Step 2: Call API
                    st.write(":material/flash_on: **Generating:** Contacting Snowflake Cortex...")
                    start_time = time.time()
                    
                    # This is the blocking call that takes time
                    response = call_cortex_llm(prompt)
                    
                    end_time = time.time()
                    
                    # Step 3: Update Status to Complete
                    st.write(f":material/check_circle: **Complete:** Post generated in {end_time - start_time:.2f} seconds!")
                    status.update(label="Post Generated Successfully!", state="complete", expanded=False)
                
                # Display Result
                st.subheader("Generated Post:")
                st.markdown(response)
                
                # Easy copy text area
                st.markdown("**📋 Copy from here:**")
                st.text_area(
                    "Click inside and press Ctrl+A to select all, then Ctrl+C to copy",
                    value=response,
                    height=200,
                    key="copy_area_default",
                    label_visibility="collapsed"
                )
                
                # Show raw response in expander
                with st.expander("See raw text"):
                    st.code(response)
                        
            except Exception as e:
                st.error(f"Error generating post: {str(e)}")
        else:
            st.warning("⚠️ Please enter a content URL")
            
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
    st.caption("Using your custom connection - Watch the status updates!")
    
    # Cached LLM Function for custom session
    @st.cache_data
    def call_cortex_llm_custom(prompt_text):
        """Makes a call to Cortex AI with the given prompt."""
        model = "claude-3-5-sonnet"
        df = st.session_state.custom_session.range(1).select(
            ai_complete(model=model, prompt=prompt_text).alias("response")
        )
        
        # Get response (ai_complete returns plain text, not JSON)
        response = df.collect()[0][0]
        return response
    
    # Input widgets for custom
    col1, col2 = st.columns([2, 1])
    
    with col1:
        custom_content = st.text_input(
            "Content URL:", 
            "https://docs.snowflake.com/en/user-guide/views-semantic/overview",
            key="custom_content"
        )
    
    with col2:
        custom_tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"], key="custom_tone")
    
    custom_word_count = st.slider("Approximate word count:", 50, 300, 100, key="custom_word_count")
    
    # Generate button
    if st.button("Generate Post", type="primary", key="custom_generate"):
        if custom_content:
            try:
                # Initialize the status container
                with st.status("Starting engine...", expanded=True) as status:
                    
                    # Step 1: Construct Prompt
                    st.write(":material/psychology: **Thinking:** Analyzing constraints and tone...")
                    time.sleep(0.5)  # Brief pause for UX
                    
                    custom_prompt = f"""
    You are an expert social media manager. Generate a LinkedIn post based on the following:

    Tone: {custom_tone}
    Desired Length: Approximately {custom_word_count} words
    Use content from this URL: {custom_content}

    Generate only the LinkedIn post text. Use dash for bullet points.
    """
                    
                    # Step 2: Call API
                    st.write(":material/flash_on: **Generating:** Contacting Snowflake Cortex...")
                    start_time = time.time()
                    
                    # This is the blocking call that takes time
                    custom_response = call_cortex_llm_custom(custom_prompt)
                    
                    end_time = time.time()
                    
                    # Step 3: Update Status to Complete
                    st.write(f":material/check_circle: **Complete:** Post generated in {end_time - start_time:.2f} seconds!")
                    status.update(label="Post Generated Successfully!", state="complete", expanded=False)
                
                # Display Result
                st.subheader("Generated Post:")
                st.markdown(custom_response)
                
                # Easy copy text area
                st.markdown("**📋 Copy from here:**")
                st.text_area(
                    "Click inside and press Ctrl+A to select all, then Ctrl+C to copy",
                    value=custom_response,
                    height=200,
                    key="copy_area_custom",
                    label_visibility="collapsed"
                )
                
                # Show raw response in expander
                with st.expander("See raw text"):
                    st.code(custom_response)
                        
            except Exception as e:
                st.error(f"Error generating post: {str(e)}")
        else:
            st.warning("⚠️ Please enter a content URL")

# Footer
st.divider()
st.caption("Day 6: Status UI for Long-Running Task | 30 Days of AI")
with col3:
    if st.button("🔄 Reset"):
        st.session_state.demo_counter = 0

st.metric("Counter Value", st.session_state.demo_counter)

st.subheader("Common Patterns")
st.code("""
# Dictionary initialization
defaults = {
    'username': '',
    'messages': [],
    'logged_in': False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Callback functions
def on_submit():
    st.session_state.submitted = True
    st.session_state.form_data = get_form_data()

st.button("Submit", on_click=on_submit)

# Delete from session state
if st.button("Logout"):
    del st.session_state['username']
    # or: st.session_state.pop('username', None)
""", language="python")

st.subheader("Widget State")
st.markdown("Widgets can automatically use session state with the `key` parameter:")

name = st.text_input("Name:", key="user_name")
st.write(f"Stored in session state: {st.session_state.user_name}")

st.markdown("---")
st.info("✅ Practice using session state in your apps!")

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
