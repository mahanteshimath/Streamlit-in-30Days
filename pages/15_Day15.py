import streamlit as st
import time
import json
from snowflake.snowpark.functions import ai_complete

st.set_page_config(page_title="Day 15 - Model Comparison Arena", page_icon="1️⃣5️⃣", layout="wide")

st.title(":material/compare: Day 15: Model Comparison Arena")
st.caption("30 Days of AI")
st.markdown("---")

# Code example section
st.header("🚀 Quick Start - Model Comparison Arena")
with st.expander("View Code Snippet", expanded=False):
       st.code("""
       import streamlit as st
       import time
       import json
       from snowflake.snowpark.functions import ai_complete

       # Connect to Snowflake
       try:
       from snowflake.snowpark.context import get_active_session
       session = get_active_session()
       except:
       from snowflake.snowpark import Session
       session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

       # Session state initialization
       if "latest_results" not in st.session_state:
       st.session_state.latest_results = None

       def run_model(model: str, prompt: str) -> dict:
       start = time.time()
       
       # Call Cortex Complete function
       df = session.range(1).select(
              ai_complete(model=model, prompt=prompt).alias("response")
       )
       
       rows = df.collect()
       response_raw = rows[0][0]
       response_json = json.loads(response_raw)
       
       # Extract text from response
       text = response_json.get("choices", [{}])[0].get("messages", "") if isinstance(response_json, dict) else str(response_json)
       
       latency = time.time() - start
       tokens = int(len(text.split()) * 4/3)  # Estimate tokens
       
       return {"latency": latency, "tokens": tokens, "response_text": text}

       def display_metrics(results: dict, model_key: str):
       latency_col, tokens_col = st.columns(2)
       latency_col.metric("Latency (s)", f"{results[model_key]['latency']:.1f}")
       tokens_col.metric("Tokens", results[model_key]['tokens'])

       def display_response(container, results: dict, model_key: str):
       with container:
              with st.chat_message("user"):
              st.write(results["prompt"])
              with st.chat_message("assistant"):
              st.write(results[model_key]["response_text"])

       # Model selection
       llm_models = ["llama3-8b", "llama3-70b", "mistral-7b", "mixtral-8x7b",
                     "claude-3-5-sonnet", "claude-haiku-4-5", "openai-gpt-5", "openai-gpt-5-mini"]

       st.title(":material/compare: Select Models")
       col_a, col_b = st.columns(2)

       col_a.write("**Model A**")
       model_a = col_a.selectbox("Model A", llm_models, key="model_a", label_visibility="collapsed")

       col_b.write("**Model B**")
       model_b = col_b.selectbox("Model B", llm_models, key="model_b", index=1, label_visibility="collapsed")

       # Response containers
       st.divider()
       col_a, col_b = st.columns(2)
       results = st.session_state.latest_results

       for col, model_name, model_key in [(col_a, model_a, "model_a"), (col_b, model_b, "model_b")]:
       with col:
              st.subheader(model_name)
              container = st.container(height=400, border=True)
              
              if results:
              display_response(container, results, model_key)
              
              st.caption("Performance Metrics")
              if results:
              display_metrics(results, model_key)
              else:
              latency_col, tokens_col = st.columns(2)
              latency_col.metric("Latency (s)", "—")
              tokens_col.metric("Tokens", "—")

       # Chat input and execution
       st.divider()
       if prompt := st.chat_input("Enter your message to compare models"):
       with st.status(f"Running {model_a}..."):
              result_a = run_model(model_a, prompt)
       with st.status(f"Running {model_b}..."):
              result_b = run_model(model_b, prompt)
       
       st.session_state.latest_results = {"prompt": prompt, "model_a": result_a, "model_b": result_b}
       st.rerun()

       st.divider()
       st.caption("Day 15: Model Comparison Arena | 30 Days of AI")
       """, language="python")

st.markdown("---")

# Working Demo
st.header("💬 Try It Yourself!")
st.caption("Using Snowflake connection to compare AI models side-by-side")

with st.expander("⚠️ Troubleshooting: Cross-Region Error", expanded=False):
    st.warning("**If you see a cross-region error like this**, you need to enable cross-region access in your Snowflake account.")
    st.image("resources/error.JPG", caption="Example cross-region error", use_container_width=True)
    st.markdown("**Solution:** Run the following SQL command in your Snowflake worksheet:")
    st.code("ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';  ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'ANY_REGION';", language="sql")
    st.info("💡 This command enables Cortex AI to access models across different AWS regions.")

try:
    # Connect to Snowflake
    if 'session' not in st.session_state:
        try:
            from snowflake.snowpark.context import get_active_session
            st.session_state.session = get_active_session()
        except:
            from snowflake.snowpark import Session
            if "connections" in st.secrets and "snowflake" in st.secrets["connections"]:
                st.session_state.session = Session.builder.configs(
                    st.secrets["connections"]["snowflake"]
                ).create()
            else:
                raise Exception("No Snowflake connection configured in secrets.toml")
    
    session = st.session_state.session

    # Session state initialization
    if "latest_results" not in st.session_state:
        st.session_state.latest_results = None

    def run_model(model: str, prompt: str) -> dict:
        """Execute model and collect metrics."""
        start = time.time()

        # Call Cortex Complete function
        df = session.range(1).select(
            ai_complete(model=model, prompt=prompt).alias("response")
        )

        # Get response from dataframe
        rows = df.collect()
        response_raw = rows[0][0]
        response_json = json.loads(response_raw)

        # Extract text from response
        text = response_json.get("choices", [{}])[0].get("messages", "") if isinstance(response_json, dict) else str(response_json)

        latency = time.time() - start
        tokens = int(len(text.split()) * 4/3)  # Estimate tokens (1 token ˜ 0.75 words)

        return {
            "latency": latency,
            "tokens": tokens,
            "response_text": text
        }

    def display_metrics(results: dict, model_key: str):
        """Display metrics for a model."""
        latency_col, tokens_col = st.columns(2)  # Create 2 equal columns

        latency_col.metric("Latency (s)", f"{results[model_key]['latency']:.1f}")  # 1 decimal for seconds
        tokens_col.metric("Tokens", results[model_key]['tokens'])

    def display_response(container, results: dict, model_key: str):
        """Display chat messages in container."""
        with container:
            with st.chat_message("user"):
                st.write(results["prompt"])
            with st.chat_message("assistant"):
                st.write(results[model_key]["response_text"])

    # Model selection
    llm_models = [
        "llama3-8b",
        "llama3-70b",
        "mistral-7b",
        "mixtral-8x7b",
        "claude-3-5-sonnet",
        "claude-haiku-4-5",
        "openai-gpt-5",
        "openai-gpt-5-mini"
    ]
    st.title(":material/compare: Select Models")
    col_a, col_b = st.columns(2)  # Create two columns for side-by-side dropdowns

    col_a.write("**Model A**")
    model_a = col_a.selectbox("Model A", llm_models, key="model_a", label_visibility="collapsed")

    col_b.write("**Model B**")
    model_b = col_b.selectbox("Model B", llm_models, key="model_b", index=1, label_visibility="collapsed")  # Default to second model

    # Response containers
    st.divider()
    col_a, col_b = st.columns(2)  # Create two columns for side-by-side responses
    results = st.session_state.latest_results

    # Loop through both models to avoid code duplication
    for col, model_name, model_key in [(col_a, model_a, "model_a"), (col_b, model_b, "model_b")]:
        with col:
            st.subheader(model_name)
            container = st.container(height=400, border=True)  # Fixed height, scrollable container

            if results:
                display_response(container, results, model_key)

            st.caption("Performance Metrics")
            if results:
                display_metrics(results, model_key)
            else:  # Show placeholders when no results yet
                latency_col, tokens_col = st.columns(2)
                latency_col.metric("Latency (s)", "—")
                tokens_col.metric("Tokens", "—")

    # Chat input and execution
    st.divider()
    if prompt := st.chat_input("Enter your message to compare models"):  # Walrus operator: assign and check
        # Run models sequentially (Model A, then Model B)
        with st.status(f"Running {model_a}..."):
            result_a = run_model(model_a, prompt)
        with st.status(f"Running {model_b}..."):
            result_b = run_model(model_b, prompt)

        # Store results in session state (replaces previous results)
        st.session_state.latest_results = {"prompt": prompt, "model_a": result_a, "model_b": result_b}
        st.rerun()  # Trigger rerun to display results

    st.divider()
    st.caption("Day 15: Model Comparison Arena | 30 Days of AI")

except Exception as e:
    st.error(f"❌ Connection Error: {str(e)}")
    st.info("💡 Make sure your Snowflake connection is properly configured in secrets.toml")

st.markdown(
    '''
    <style>
    .streamlit-expanderHeader {
        background-color: blue;
        color: white;
    }
    .streamlit-expanderContent {
        background-color: blue;
        color: white;
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
