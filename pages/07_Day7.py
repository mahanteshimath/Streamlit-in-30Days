import streamlit as st
import time
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import ai_complete

st.set_page_config(page_title="Day 7 - Theming and Layout", page_icon="7️⃣", layout="wide")

st.title(":material/palette: Day 7: Theming and Layout")
st.caption("30 Days of AI")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
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

    # Input widgets
    st.subheader(":material/input: Input content")
    content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")

    with st.sidebar:
        st.title(":material/post: LinkedIn Post Generator v3")
        st.success("An app for generating LinkedIn post using content from input link.")
        tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
        word_count = st.slider("Approximate word count:", 50, 300, 100)

    # Generate button
    if st.button("Generate Post"):
        
        # Initialize the status container
        with st.status("Starting engine...", expanded=True) as status:
            
            # Step 1: Construct Prompt
            st.write(":material/psychology: Thinking: Analyzing constraints and tone...")
            time.sleep(2)
            
            prompt = f\"\"\"
            You are an expert social media manager. Generate a LinkedIn post based on the following:

            Tone: {tone}
            Desired Length: Approximately {word_count} words
            Use content from this URL: {content}

            Generate only the LinkedIn post text. Use dash for bullet points.
            \"\"\"
            
            # Step 2: Call API
            st.write(":material/flash_on: Generating: contacting Snowflake Cortex...")
            time.sleep(2)
            
            # This is the blocking call that takes time
            response = call_cortex_llm(prompt)
            
            # Step 3: Update Status to Complete
            st.write(":material/check_circle: Post generation completed!")
            status.update(label="Post Generated Successfully!", state="complete", expanded=False)

        # Display Result
        with st.container(border=True):
            st.subheader(":material/output: Generated post:")
            st.markdown(response)

    # Footer
    st.divider()
    st.caption("Day 7: Theming and Layout | 30 Days of AI")
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
    st.subheader(":material/input: Input content")
    content = st.text_input(
        "Content URL:", 
        "https://docs.snowflake.com/en/user-guide/views-semantic/overview",
        key="default_content"
    )
    
    with st.sidebar:
        st.title(":material/post: LinkedIn Post Generator v3")
        st.success("An app for generating LinkedIn post using content from input link.")
        st.markdown("**🎨 Theme (demo)**")
        theme_choice = st.selectbox(
            "Theme",
            ["Default", "Light", "Elegant", "Ocean", "Sunset", "Forest", "Midnight", "Minimal"],
            key="default_theme"
        )
        font_choice = st.selectbox(
            "Font",
            ["System", "Georgia", "Trebuchet MS", "Arial", "Times New Roman", "Courier New", "Verdana"],
            key="default_font"
        )
        st.caption("Tip: These controls only change the page styling via CSS.")
        st.markdown("---")
        tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"], key="default_tone")
        word_count = st.slider("Approximate word count:", 50, 300, 100, key="default_word_count")

    if theme_choice == "Light":
        theme_css = """
        <style>
        .stApp { background: #f7f7fb; color: #1f2937; }
        .stApp h1, .stApp h2, .stApp h3 { color: #111827; }
        .stButton>button { background: #2563eb; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif theme_choice == "Elegant":
        theme_css = """
        <style>
        .stApp { background: linear-gradient(180deg, #2c1e5b 0%, #1a1336 100%); color: #e5e7eb; }
        .stApp h1, .stApp h2, .stApp h3 { color: #f9fafb; }
        .stButton>button { background: #7c3aed; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif theme_choice == "Ocean":
        theme_css = """
        <style>
        .stApp { background: #0b1220; color: #e2e8f0; }
        .stApp h1, .stApp h2, .stApp h3 { color: #bae6fd; }
        .stButton>button { background: #0ea5e9; color: #0b1220; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif theme_choice == "Sunset":
        theme_css = """
        <style>
        .stApp { background: linear-gradient(180deg, #2b1b2f 0%, #3b1f2b 100%); color: #fde68a; }
        .stApp h1, .stApp h2, .stApp h3 { color: #fcd34d; }
        .stButton>button { background: #f97316; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif theme_choice == "Forest":
        theme_css = """
        <style>
        .stApp { background: #0f1e17; color: #d1fae5; }
        .stApp h1, .stApp h2, .stApp h3 { color: #a7f3d0; }
        .stButton>button { background: #10b981; color: #0f1e17; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif theme_choice == "Midnight":
        theme_css = """
        <style>
        .stApp { background: #0b0f1a; color: #e5e7eb; }
        .stApp h1, .stApp h2, .stApp h3 { color: #c7d2fe; }
        .stButton>button { background: #6366f1; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif theme_choice == "Minimal":
        theme_css = """
        <style>
        .stApp { background: #ffffff; color: #111827; }
        .stApp h1, .stApp h2, .stApp h3 { color: #111827; }
        .stButton>button { background: #111827; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    else:
        theme_css = ""

    if font_choice == "Georgia":
        font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: Georgia, serif !important; }</style>"
    elif font_choice == "Trebuchet MS":
        font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: 'Trebuchet MS', sans-serif !important; }</style>"
    elif font_choice == "Arial":
        font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: Arial, sans-serif !important; }</style>"
    elif font_choice == "Times New Roman":
        font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: 'Times New Roman', serif !important; }</style>"
    elif font_choice == "Courier New":
        font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: 'Courier New', monospace !important; }</style>"
    elif font_choice == "Verdana":
        font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: Verdana, sans-serif !important; }</style>"
    else:
        font_css = ""

    if theme_css or font_css:
        st.markdown(theme_css + font_css, unsafe_allow_html=True)
    
    # Generate button
    if st.button("Generate Post", type="primary"):
        if content:
            try:
                # Initialize the status container
                with st.status("Starting engine...", expanded=True) as status:
                    
                    # Step 1: Construct Prompt
                    st.write(":material/psychology: **Thinking:** Analyzing constraints and tone...")
                    time.sleep(1)
                    
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
                # Display Result
                display_response = str(response).replace("\\n", "\n")
                with st.container(border=True):
                    st.subheader(":material/output: Generated post:")
                    st.markdown(display_response)
                

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
    st.caption("Using your custom connection")
    
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
    st.subheader(":material/input: Input content")
    custom_content = st.text_input(
        "Content URL:", 
        "https://docs.snowflake.com/en/user-guide/views-semantic/overview",
        key="custom_content"
    )
    
    with st.sidebar:
        st.title(":material/post: LinkedIn Post Generator v3")
        st.success("An app for generating LinkedIn post using content from input link.")
        st.markdown("**🎨 Theme (demo)**")
        custom_theme_choice = st.selectbox(
            "Theme",
            ["Default", "Light", "Elegant", "Ocean", "Sunset", "Forest", "Midnight", "Minimal"],
            key="custom_theme"
        )
        custom_font_choice = st.selectbox(
            "Font",
            ["System", "Georgia", "Trebuchet MS", "Arial", "Times New Roman", "Courier New", "Verdana"],
            key="custom_font"
        )
        st.caption("Tip: These controls only change the page styling via CSS.")
        st.markdown("---")
        custom_tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"], key="custom_tone")
        custom_word_count = st.slider("Approximate word count:", 50, 300, 100, key="custom_word_count")

    if custom_theme_choice == "Light":
        custom_theme_css = """
        <style>
        .stApp { background: #f7f7fb; color: #1f2937; }
        .stApp h1, .stApp h2, .stApp h3 { color: #111827; }
        .stButton>button { background: #2563eb; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif custom_theme_choice == "Elegant":
        custom_theme_css = """
        <style>
        .stApp { background: linear-gradient(180deg, #2c1e5b 0%, #1a1336 100%); color: #e5e7eb; }
        .stApp h1, .stApp h2, .stApp h3 { color: #f9fafb; }
        .stButton>button { background: #7c3aed; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif custom_theme_choice == "Ocean":
        custom_theme_css = """
        <style>
        .stApp { background: #0b1220; color: #e2e8f0; }
        .stApp h1, .stApp h2, .stApp h3 { color: #bae6fd; }
        .stButton>button { background: #0ea5e9; color: #0b1220; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif custom_theme_choice == "Sunset":
        custom_theme_css = """
        <style>
        .stApp { background: linear-gradient(180deg, #2b1b2f 0%, #3b1f2b 100%); color: #fde68a; }
        .stApp h1, .stApp h2, .stApp h3 { color: #fcd34d; }
        .stButton>button { background: #f97316; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif custom_theme_choice == "Forest":
        custom_theme_css = """
        <style>
        .stApp { background: #0f1e17; color: #d1fae5; }
        .stApp h1, .stApp h2, .stApp h3 { color: #a7f3d0; }
        .stButton>button { background: #10b981; color: #0f1e17; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif custom_theme_choice == "Midnight":
        custom_theme_css = """
        <style>
        .stApp { background: #0b0f1a; color: #e5e7eb; }
        .stApp h1, .stApp h2, .stApp h3 { color: #c7d2fe; }
        .stButton>button { background: #6366f1; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    elif custom_theme_choice == "Minimal":
        custom_theme_css = """
        <style>
        .stApp { background: #ffffff; color: #111827; }
        .stApp h1, .stApp h2, .stApp h3 { color: #111827; }
        .stButton>button { background: #111827; color: white; border: none; }
        [data-testid="stExpander"] { background: transparent !important; }
        </style>
        """
    else:
        custom_theme_css = ""

    if custom_font_choice == "Georgia":
        custom_font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: Georgia, serif !important; }</style>"
    elif custom_font_choice == "Trebuchet MS":
        custom_font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: 'Trebuchet MS', sans-serif !important; }</style>"
    elif custom_font_choice == "Arial":
        custom_font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: Arial, sans-serif !important; }</style>"
    elif custom_font_choice == "Times New Roman":
        custom_font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: 'Times New Roman', serif !important; }</style>"
    elif custom_font_choice == "Courier New":
        custom_font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: 'Courier New', monospace !important; }</style>"
    elif custom_font_choice == "Verdana":
        custom_font_css = "<style>.stMarkdown p, .stMarkdown span, .stMarkdown div:not([data-testid='stExpander']) { font-family: Verdana, sans-serif !important; }</style>"
    else:
        custom_font_css = ""

    if custom_theme_css or custom_font_css:
        st.markdown(custom_theme_css + custom_font_css, unsafe_allow_html=True)
    
    # Generate button
    if st.button("Generate Post", type="primary", key="custom_generate"):
        if custom_content:
            try:
                # Initialize the status container
                with st.status("Starting engine...", expanded=True) as status:
                    
                    # Step 1: Construct Prompt
                    st.write(":material/psychology: **Thinking:** Analyzing constraints and tone...")
                    time.sleep(1)
                    
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
                display_response = str(custom_response).replace("\\n", "\n")
                with st.container(border=True):
                    st.subheader(":material/output: Generated post:")
                    st.markdown(display_response)

                
                # Show raw response in expander
                with st.expander("See raw text"):
                    st.code(display_response)
                        
            except Exception as e:
                st.error(f"Error generating post: {str(e)}")
        else:
            st.warning("⚠️ Please enter a content URL")

# Footer
st.divider()
st.caption("Day 7: Theming and Layout | 30 Days of AI")

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
