import streamlit as st

st.set_page_config(
    page_title="Day 29: LangChain Basics",
    page_icon=":material/link:",
    layout="wide",
)

st.title(":material/link: Day 29: LangChain Basics")
st.write(
    "Rebuild Day 5's LinkedIn Post Generator using LangChain—a framework that makes LLM applications cleaner, more reusable, and easier to extend."
)

# Sidebar
with st.sidebar:
    st.header(":material/info: What is LangChain?")
    st.info(
        "LangChain is a framework for building LLM applications with reusable, composable components.",
        icon=":material/info:",
    )

    st.divider()

    st.header(":material/package: Prerequisites")
    st.code("""pip install langchain-core langchain-snowflake snowflake-snowpark-python streamlit""", language="bash")
    
    st.markdown("**Required Packages:**")
    st.write("• `langchain-core` - Core functionality")
    st.write("• `langchain-snowflake` - Cortex integration")
    st.write("• `snowflake-snowpark-python` - Connection")
    st.write("• `streamlit` - Web framework")

    st.divider()

    st.header(":material/lightbulb: Why LangChain?")
    st.success(
        "✅ Cleaner, more readable code\n\n✅ No manual JSON parsing\n\n✅ Easy to extend and compose\n\n✅ Works with multiple LLM providers",
        icon=":material/check_circle:",
    )

    st.divider()

    st.header(":material/link: Resources")
    st.page_link(
        "https://python.langchain.com/docs/introduction/",
        label="LangChain Documentation",
        icon=":material/book:",
    )
    st.page_link(
        "https://python.langchain.com/docs/integrations/chat/snowflake/",
        label="LangChain Snowflake Integration",
        icon=":material/cloud:",
    )

# Main Content
st.subheader(":material/code: Complete Working App")

with st.expander("📱 View Full Code", expanded=True):
    st.code('''import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_snowflake import ChatSnowflake

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Create prompt template
template = PromptTemplate.from_template(
    """You are an expert social media manager. Generate a LinkedIn post based on:

    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL: {content}

    Generate only the LinkedIn post text. Use dash for bullet points."""
)

# Create LLM and chain
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
chain = template | llm

# UI
st.title(":material/post: LinkedIn Post Generator")
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)

if st.button("Generate Post"):
    result = chain.invoke({"content": content, "tone": tone, "word_count": word_count})
    st.subheader("Generated Post:")
    st.markdown(result.content)

st.divider()
st.caption("Day 29: LangChain Basics | 30 Days of AI with Streamlit")
''', language="python")

st.markdown("---")

# Step-by-Step Explanation
st.subheader(":material/school: How It Works: Step-by-Step")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    ":material/settings: 1. Setup",
    ":material/description: 2. Template",
    ":material/link: 3. Chain",
    ":material/web: 4. UI",
    ":material/play_arrow: 5. Invoke"
])

with tab1:
    st.markdown("### :material/settings: Step 1: Snowflake Connection Setup")
    
    st.code('''import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_snowflake import ChatSnowflake

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
''', language="python")
    
    st.info("""
    **What's happening:**
    - Import `PromptTemplate` for creating reusable prompt templates
    - Import `ChatSnowflake` as the LangChain wrapper for Snowflake Cortex
    - Universal connection pattern works in both SiS and external environments
    """, icon=":material/info:")

with tab2:
    st.markdown("### :material/description: Step 2: Creating a PromptTemplate")
    
    st.code('''# Create prompt template
template = PromptTemplate.from_template(
    """You are an expert social media manager. Generate a LinkedIn post based on:

    Tone: {tone}
    Desired Length: Approximately {word_count} words
    Use content from this URL: {content}

    Generate only the LinkedIn post text. Use dash for bullet points."""
)
''', language="python")
    
    st.success("""
    **Benefits:**
    - `PromptTemplate.from_template(...)` creates a reusable template
    - Placeholders `{tone}`, `{word_count}`, `{content}` filled at runtime
    - No messy f-strings!
    - Templates can be stored, shared, and tested independently
    """, icon=":material/check_circle:")

with tab3:
    st.markdown("### :material/link: Step 3: Creating the LLM and Chain")
    
    st.code('''# Create LLM and chain
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
chain = template | llm
''', language="python")
    
    st.info("""
    **LCEL (LangChain Expression Language):**
    - `ChatSnowflake(...)` creates a LangChain-compatible LLM using Cortex
    - `chain = template | llm` uses the pipe operator to create a chain
    - **Flow:** Template formats prompt → LLM generates response
    """, icon=":material/info:")
    
    st.markdown("**Available Cortex Models:**")
    models_col1, models_col2 = st.columns(2)
    with models_col1:
        st.write("• claude-3-5-sonnet")
        st.write("• llama3-70b")
    with models_col2:
        st.write("• mistral-large")
        st.write("• And more!")

with tab4:
    st.markdown("### :material/web: Step 4: Building the Streamlit UI")
    
    st.code('''# UI
st.title(":material/post: LinkedIn Post Generator")
content = st.text_input("Content URL:", "https://docs.snowflake.com/en/user-guide/views-semantic/overview")
tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"])
word_count = st.slider("Approximate word count:", 50, 300, 100)
''', language="python")
    
    st.write("**UI Components:**")
    st.write("• `st.title(...)` - App title with Material icon")
    st.write("• `st.text_input(...)` - Content URL input with default")
    st.write("• `st.selectbox(...)` - Tone selection dropdown")
    st.write("• `st.slider(...)` - Word count adjustment")

with tab5:
    st.markdown("### :material/play_arrow: Step 5: Invoking the Chain")
    
    st.code('''if st.button("Generate Post"):
    result = chain.invoke({"content": content, "tone": tone, "word_count": word_count})
    st.subheader("Generated Post:")
    st.markdown(result.content)
''', language="python")
    
    st.success("""
    **Magic of LangChain:**
    - `chain.invoke({...})` calls the chain with template variables
    - `result.content` contains the generated text
    - **No JSON parsing needed!** LangChain handles response structure automatically
    """, icon=":material/auto_awesome:")

st.markdown("---")

# Comparison Section
st.subheader(":material/compare_arrows: Day 5 vs Day 29 Comparison")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❌ Day 5: Raw Cortex API")
    st.code('''prompt = f"""You are an expert social media manager.
Tone: {tone}
Desired Length: {word_count} words
Use content from: {content}"""

df = session.range(1).select(
    ai_complete(model="claude-3-5-sonnet", prompt=prompt)
)
response_raw = df.collect()[0][0]
response = json.loads(response_raw)
text = response.get("choices", [{}])[0].get("messages", "")
''', language="python")
    
    st.error("""
    **Issues:**
    - Manual f-string formatting
    - Multiple lines of JSON parsing
    - Error-prone nested response extraction
    """, icon=":material/cancel:")

with col2:
    st.markdown("### ✅ Day 29: LangChain")
    st.code('''template = PromptTemplate.from_template(
    """You are an expert social media manager.
    Tone: {tone}
    Desired Length: {word_count} words
    Use content from: {content}"""
)

chain = template | llm
result = chain.invoke({
    "tone": tone, 
    "word_count": word_count, 
    "content": content
})
text = result.content
''', language="python")
    
    st.success("""
    **Benefits:**
    - Cleaner, more readable code
    - No manual JSON parsing
    - Reusable template object
    - Easy to extend with more chain steps
    """, icon=":material/check_circle:")

st.markdown("---")

# Key Concepts Section
st.subheader(":material/key: Key LangChain Concepts")

concept_tab1, concept_tab2, concept_tab3 = st.tabs([
    ":material/description: PromptTemplate",
    ":material/link: LCEL",
    ":material/cloud: ChatSnowflake"
])

with concept_tab1:
    st.markdown("### :material/description: PromptTemplate")
    st.write("Replace messy f-strings with reusable templates:")
    
    st.code('''# Create once, use many times
template = PromptTemplate.from_template(
    "Generate a {tone} post about {topic} in {word_count} words"
)

# Use with different inputs
result1 = chain.invoke({"tone": "professional", "topic": "AI", "word_count": 100})
result2 = chain.invoke({"tone": "casual", "topic": "Coffee", "word_count": 50})
''', language="python")

with concept_tab2:
    st.markdown("### :material/link: LCEL (LangChain Expression Language)")
    st.write("Chain components with the pipe operator (|):")
    
    st.code('''# Simple chain: template → LLM
chain = template | llm

# Extended chain: template → LLM → output parser
chain = template | llm | output_parser

# What happens:
# 1. Template formats the input variables
# 2. LLM generates a response
# 3. Output parser structures the result
''', language="python")
    
    st.info("The `|` operator creates a pipeline where output of one component flows to the next!", icon=":material/info:")

with concept_tab3:
    st.markdown("### :material/cloud: ChatSnowflake")
    st.write("LangChain wrapper for Snowflake Cortex models:")
    
    st.code('''# Create the LLM wrapper
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)

# Available models:
# - claude-3-5-sonnet
# - llama3-70b
# - mistral-large
# - And more Cortex models
''', language="python")

st.markdown("---")

# Try It Out Section
st.subheader(":material/science: Try It Out")

st.info("""
**Live Demo:** Test the LangChain-powered LinkedIn Post Generator below!
""", icon=":material/lightbulb:")

# Actual working implementation
try:
    from langchain_core.prompts import PromptTemplate
    from langchain_snowflake import ChatSnowflake
    
    # Connect to Snowflake
    try:
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
    except:
        from snowflake.snowpark import Session
        session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
    
    # Create prompt template
    template = PromptTemplate.from_template(
        """You are an expert social media manager. Generate a LinkedIn post based on:

        Tone: {tone}
        Desired Length: Approximately {word_count} words
        Use content from this URL: {content}

        Generate only the LinkedIn post text. Use dash for bullet points."""
    )
    
    # Create LLM and chain
    llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
    chain = template | llm
    
    # UI
    with st.container(border=True):
        st.markdown("### :material/post: LinkedIn Post Generator")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            content = st.text_input(
                "Content URL:", 
                "https://docs.snowflake.com/en/user-guide/views-semantic/overview",
                key="demo_content"
            )
        with col2:
            tone = st.selectbox("Tone:", ["Professional", "Casual", "Funny"], key="demo_tone")
        
        word_count = st.slider("Approximate word count:", 50, 300, 100, key="demo_word_count")
        
        if st.button("Generate Post", type="primary", use_container_width=True):
            with st.spinner("Generating your LinkedIn post..."):
                result = chain.invoke({"content": content, "tone": tone, "word_count": word_count})
                st.success("Post generated successfully!", icon=":material/check_circle:")
                st.markdown("---")
                st.markdown("**Generated Post:**")
                st.markdown(result.content)

except ImportError as e:
    st.error(f"""
    **LangChain packages not installed!**
    
    Install required packages:
    ```bash
    pip install langchain-core langchain-snowflake snowflake-snowpark-python
    ```
    """, icon=":material/error:")
except Exception as e:
    st.error(f"""
    **Error:** {str(e)}
    
    Make sure you have:
    - Valid Snowflake connection configured in secrets
    - Required packages installed
    - Cortex AI enabled in your Snowflake account
    """, icon=":material/error:")

st.markdown("---")

# When to Use LangChain
st.subheader(":material/checklist: When to Use LangChain?")

advantage_col1, advantage_col2 = st.columns(2)

with advantage_col1:
    st.markdown("### :material/check_circle: Advantages")
    st.success("""
    • **Cleaner code** - No f-strings or JSON parsing
    • **Composable** - Chain multiple components
    • **Reusable** - Templates can be shared and tested
    • **Extensible** - Easy to add parsers, memory, tools
    • **Provider-agnostic** - Switch LLMs easily
    """)

with advantage_col2:
    st.markdown("### :material/workspace_premium: Best Use Cases")
    st.info("""
    • Building complex LLM applications
    • Need structured outputs (Day 30!)
    • Want maintainable, clean code
    • May need to switch LLM providers
    • Building production applications
    """)

st.markdown("---")

# Resources
st.subheader(":material/link: Resources & Next Steps")

resource_col1, resource_col2 = st.columns(2)

with resource_col1:
    st.markdown("### :material/book: Documentation")
    st.page_link("https://python.langchain.com/docs/introduction/", label="LangChain Documentation", icon=":material/book:")
    st.page_link("https://python.langchain.com/docs/integrations/chat/snowflake/", label="LangChain Snowflake Integration", icon=":material/cloud:")
    st.page_link("https://python.langchain.com/docs/concepts/prompt_templates/", label="PromptTemplate Documentation", icon=":material/description:")
    st.page_link("https://python.langchain.com/docs/concepts/lcel/", label="LCEL (LangChain Expression Language)", icon=":material/link:")
    st.page_link("https://docs.snowflake.com/en/user-guide/snowflake-cortex/overview", label="Snowflake Cortex AI", icon=":material/ac_unit:")

with resource_col2:
    st.markdown("### :material/next_plan: Next Steps")
    st.success("""
    **Day 30:** Take LangChain further with structured output using Pydantic!
    
    **Try These:**
    • Add more steps to the chain (output parsers, validators)
    • Experiment with different Cortex models
    • Build more complex chains with multiple LLM calls
    """, icon=":material/rocket:")

st.divider()
st.caption("Day 29: LangChain Basics | 30 Days of AI with Streamlit")
