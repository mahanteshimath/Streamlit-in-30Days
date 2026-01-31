import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Day 21 - RAG with Cortex Search", page_icon="2️⃣1️⃣", layout="wide")

st.title(":material/link: Day 21: RAG with Cortex Search")
st.caption("30 Days of AI")
st.write("Combine search results with LLM generation for grounded answers.")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code('''
    import streamlit as st
    from snowflake.snowpark.context import get_active_session

    st.title(":material/link: RAG with Cortex Search")

    # Get the current credentials
    session = get_active_session()

    st.subheader(":material/menu_book: How RAG Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("**:material/looks_one: Retrieve**")
            st.markdown("Cortex Search finds relevant document chunks based on your question.")

    with col2:
        with st.container(border=True):
            st.markdown("**:material/looks_two: Augment**")
            st.markdown("Retrieved chunks are added to the prompt as context for the LLM.")

    with col3:
        with st.container(border=True):
            st.markdown("**:material/looks_3: Generate**")
            st.markdown("The LLM generates an answer grounded in the retrieved documents.")

    # Sidebar configuration
    with st.sidebar:
        st.header(":material/settings: Settings")
        default_service = "RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH"

        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [
                f"{row['database_name']}.{row['schema_name']}.{row['name']}"
                for row in services_result
            ] if services_result else []
        except:
            available_services = []

        if default_service in available_services:
            available_services.remove(default_service)
        available_services.insert(0, default_service)

        if available_services:
            available_services.append("-- Enter manually --")
            search_service_option = st.selectbox("Search Service:", options=available_services, index=0)

            if search_service_option == "-- Enter manually --":
                search_service = st.text_input("Enter service path:", placeholder="database.schema.service_name")
            else:
                search_service = search_service_option
        else:
            search_service = st.text_input("Search Service:", value=default_service)

        num_chunks = st.slider("Context chunks:", 1, 10, 3)

        model = st.selectbox(
            "LLM Model:",
            ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"]
        )

        show_context = st.checkbox("Show retrieved context", value=True)

    st.subheader(":material/help: Ask a Question")

    question = st.text_input(
        "Your question:",
        value="Are the thermal gloves warm enough for winter?",
        placeholder="e.g., Which products have durability issues?"
    )

    if st.button(":material/search: Search & Answer", type="primary"):
        if question and search_service:
            with st.status("Processing...", expanded=True) as status:
                st.write(":material/search: **Step 1:** Searching documents...")

                try:
                    from snowflake.core import Root

                    root = Root(session)
                    parts = search_service.split(".")

                    if len(parts) != 3:
                        st.error("Service path must be in format: database.schema.service_name")
                        st.stop()

                    svc = (
                        root
                        .databases[parts[0]]
                        .schemas[parts[1]]
                        .cortex_search_services[parts[2]]
                    )

                    search_results = svc.search(
                        query=question,
                        columns=["CHUNK_TEXT", "FILE_NAME"],
                        limit=num_chunks
                    )

                    context_chunks = []
                    sources = []
                    for item in search_results.results:
                        context_chunks.append(item.get("CHUNK_TEXT", ""))
                        sources.append(item.get("FILE_NAME", "Unknown"))

                    context = "\n\n---\n\n".join(context_chunks)

                    st.write(f"   :material/check_circle: Found {len(context_chunks)} relevant chunks")
                    st.write(":material/smart_toy: **Step 2:** Generating answer...")

                    rag_prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the provided context.
    If the context doesn't contain enough information to answer, say "I don't have enough information to answer that based on the available documents."

    CONTEXT FROM DOCUMENTS:
    {context}

    USER QUESTION: {question}

    Provide a clear, accurate answer based on the context. If you use information from the context, mention it naturally."""

                    response_sql = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        '{model}',
                        '{rag_prompt.replace("'", "''")}'
                    ) as response
                    """

                    response = session.sql(response_sql).collect()[0][0]

                    st.write("   :material/check_circle: Answer generated")
                    status.update(label="Complete!", state="complete", expanded=True)

                    st.divider()

                    st.subheader(":material/lightbulb: Answer")
                    with st.container(border=True):
                        st.markdown(response)

                    if show_context:
                        st.subheader(":material/library_books: Retrieved Context")
                        st.caption(f"Used {len(context_chunks)} chunks from customer reviews")
                        for i, (chunk, source) in enumerate(zip(context_chunks, sources), 1):
                            with st.expander(f":material/description: Chunk {i} - {source}"):
                                st.write(chunk)

                except Exception as e:
                    status.update(label="Error", state="error")
                    st.error(f"Error: {str(e)}")
                    st.info(":material/lightbulb: **Troubleshooting:**\n- Make sure the search service exists (check Day 19)\n- Verify the service has finished indexing\n- Check your permissions")
        else:
            st.warning(":material/warning: Please enter a question and configure a search service.")
            st.info(":material/lightbulb: **Need a search service?**\n- Complete Day 19 to create `CUSTOMER_REVIEW_SEARCH`\n- The service will automatically appear in the dropdown above")

    st.divider()
    st.caption("Day 21: RAG with Cortex Search | 30 Days of AI")
    ''', language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("🔎 Try It Yourself!")
st.caption("Using default Snowflake connection - Retrieve, augment, and answer with Cortex Search.")

try:
    if "default_session" not in st.session_state:
        try:
            st.session_state.default_session = get_active_session()
        except:
            from snowflake.snowpark import Session
            if "connections" in st.secrets and "snowflake" in st.secrets["connections"]:
                st.session_state.default_session = Session.builder.configs(
                    st.secrets["connections"]["snowflake"]
                ).create()
            else:
                raise Exception("No Snowflake connection configured in secrets.toml")

    session = st.session_state.default_session
    st.success("✅ Connected to Snowflake!")

    st.divider()
    st.subheader(":material/menu_book: How RAG Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("**:material/looks_one: Retrieve**")
            st.markdown("""
            Cortex Search finds
            relevant document
            chunks based on
            your question.
            """)

    with col2:
        with st.container(border=True):
            st.markdown("**:material/looks_two: Augment**")
            st.markdown("""
            Retrieved chunks
            are added to the
            prompt as context
            for the LLM.
            """)

    with col3:
        with st.container(border=True):
            st.markdown("**:material/looks_3: Generate**")
            st.markdown("""
            The LLM generates
            an answer grounded
            in the retrieved
            documents.
            """)

    st.divider()

    with st.sidebar:
        st.header(":material/settings: Settings")

        default_service = "RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH"

        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [
                f"{row['database_name']}.{row['schema_name']}.{row['name']}"
                for row in services_result
            ] if services_result else []
        except:
            available_services = []

        if default_service in available_services:
            available_services.remove(default_service)
        available_services.insert(0, default_service)

        if available_services:
            available_services.append("-- Enter manually --")

            search_service_option = st.selectbox(
                "Search Service:",
                options=available_services,
                index=0,
                help="Select your Cortex Search service from Day 19"
            )

            if search_service_option == "-- Enter manually --":
                search_service = st.text_input(
                    "Enter service path:",
                    placeholder="database.schema.service_name"
                )
            else:
                search_service = search_service_option

                if search_service == st.session_state.get("search_service"):
                    st.caption(":material/check_circle: Using service from Day 19")
        else:
            search_service = st.text_input(
                "Search Service:",
                value=default_service,
                placeholder="database.schema.service_name",
                help="Full path to your Cortex Search service"
            )

        num_chunks = st.slider("Context chunks:", 1, 10, 3,
                               help="Number of relevant chunks to retrieve")

        model = st.selectbox(
            "LLM Model:",
            ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"],
            help="Model to generate the answer"
        )

        show_context = st.checkbox("Show retrieved context", value=True)

    st.subheader(":material/help: Ask a Question")

    question = st.text_input(
        "Your question:",
        value="Are the thermal gloves warm enough for winter?",
        placeholder="e.g., Which products have durability issues?"
    )

    if st.button(":material/search: Search & Answer", type="primary"):
        if question and search_service:
            with st.status("Processing...", expanded=True) as status:
                st.write(":material/search: **Step 1:** Searching documents...")

                try:
                    from snowflake.core import Root

                    root = Root(session)
                    parts = search_service.split(".")

                    if len(parts) != 3:
                        st.error("Service path must be in format: database.schema.service_name")
                        st.stop()

                    svc = (
                        root
                        .databases[parts[0]]
                        .schemas[parts[1]]
                        .cortex_search_services[parts[2]]
                    )

                    search_results = svc.search(
                        query=question,
                        columns=["CHUNK_TEXT", "FILE_NAME"],
                        limit=num_chunks
                    )

                    context_chunks = []
                    sources = []
                    for item in search_results.results:
                        context_chunks.append(item.get("CHUNK_TEXT", ""))
                        sources.append(item.get("FILE_NAME", "Unknown"))

                    context = "\n\n---\n\n".join(context_chunks)

                    st.write(f"   :material/check_circle: Found {len(context_chunks)} relevant chunks")
                    st.write(":material/smart_toy: **Step 2:** Generating answer...")

                    rag_prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the provided context.
If the context doesn't contain enough information to answer, say "I don't have enough information to answer that based on the available documents."

CONTEXT FROM DOCUMENTS:
{context}

USER QUESTION: {question}

Provide a clear, accurate answer based on the context. If you use information from the context, mention it naturally."""

                    response_sql = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        '{model}',
                        '{rag_prompt.replace("'", "''")}'
                    ) as response
                    """

                    response = session.sql(response_sql).collect()[0][0]

                    st.write("   :material/check_circle: Answer generated")
                    status.update(label="Complete!", state="complete", expanded=True)

                    st.divider()

                    st.subheader(":material/lightbulb: Answer")
                    with st.container(border=True):
                        st.markdown(response)

                    if show_context:
                        st.subheader(":material/library_books: Retrieved Context")
                        st.caption(f"Used {len(context_chunks)} chunks from customer reviews")
                        for i, (chunk, source) in enumerate(zip(context_chunks, sources), 1):
                            with st.expander(f":material/description: Chunk {i} - {source}"):
                                st.write(chunk)

                except Exception as e:
                    status.update(label="Error", state="error")
                    st.error(f"Error: {str(e)}")
                    st.info(":material/lightbulb: **Troubleshooting:**\n- Make sure the search service exists (check Day 19)\n- Verify the service has finished indexing\n- Check your permissions")
        else:
            st.warning(":material/warning: Please enter a question and configure a search service.")
            st.info(":material/lightbulb: **Need a search service?**\n- Complete Day 19 to create `CUSTOMER_REVIEW_SEARCH`\n- The service will automatically appear in the dropdown above")

    st.markdown("---")

    with st.expander(":material/info: See the explanation"):
        st.markdown("""
        **How It Works: Step-by-Step**

        1. **Visual RAG Guide**
           - Three-column layout shows Retrieve → Augment → Generate.
           - Helps users understand the pipeline before interaction.

        2. **Smart Service Selection**
           - Default service: `RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH`.
           - Auto-detects services and supports manual entry.

        3. **Retrieval with Cortex Search**
           - Uses `Root(session)` and a dynamic service path.
           - Extracts `CHUNK_TEXT` and `FILE_NAME` for context + sources.

        4. **RAG Prompt**
           - Instructs the LLM to answer strictly from context.
           - Prompts to admit when context is insufficient.

        5. **Generate with Cortex LLM**
           - Uses SQL `SNOWFLAKE.CORTEX.COMPLETE()` for safer escaping.
           - `st.status()` shows step-by-step progress.

        6. **Display Results**
           - Answer displayed in a bordered container.
           - Optional expandable context chunks with sources.

        **Why RAG > Plain LLM**
        - Uses *your* documents for grounded answers.
        - Reduces hallucinations and improves accuracy.

        **Tuning Tips**
        - Increase chunks for more context; reduce for focus.
        - Better questions lead to better retrieval.
        - Try different models for speed vs quality.
        """)

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
                st.success("✅ Connected to Snowflake!")

                st.session_state.custom_session = custom_session

            except Exception as e:
                st.error(f"❌ Connection failed: {str(e)}")
        else:
            st.warning("⚠️ Please fill in all required fields")

if "custom_session" in st.session_state:
    st.subheader("🔎 Try It Yourself!")
    st.caption("Using your custom connection")

    session = st.session_state.custom_session

    with st.sidebar:
        st.header(":material/settings: Custom Settings")

        default_service = "RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH"

        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [
                f"{row['database_name']}.{row['schema_name']}.{row['name']}"
                for row in services_result
            ] if services_result else []
        except:
            available_services = []

        if default_service in available_services:
            available_services.remove(default_service)
        available_services.insert(0, default_service)

        if available_services:
            available_services.append("-- Enter manually --")

            search_service_option = st.selectbox(
                "Search Service:",
                options=available_services,
                index=0,
                help="Select your Cortex Search service from Day 19",
                key="custom_service_select"
            )

            if search_service_option == "-- Enter manually --":
                search_service = st.text_input(
                    "Enter service path:",
                    placeholder="database.schema.service_name",
                    key="custom_service_input"
                )
            else:
                search_service = search_service_option
        else:
            search_service = st.text_input(
                "Search Service:",
                value=default_service,
                placeholder="database.schema.service_name",
                help="Full path to your Cortex Search service",
                key="custom_service_input"
            )

        num_chunks = st.slider("Context chunks:", 1, 10, 3,
                               help="Number of relevant chunks to retrieve",
                               key="custom_num_chunks")

        model = st.selectbox(
            "LLM Model:",
            ["claude-3-5-sonnet", "mistral-large", "llama3.1-8b"],
            help="Model to generate the answer",
            key="custom_model"
        )

        show_context = st.checkbox("Show retrieved context", value=True, key="custom_show_context")

    st.subheader(":material/help: Ask a Question")

    question = st.text_input(
        "Your question:",
        value="Are the thermal gloves warm enough for winter?",
        placeholder="e.g., Which products have durability issues?",
        key="custom_question"
    )

    if st.button(":material/search: Search & Answer", type="primary", key="custom_search"):
        if question and search_service:
            with st.status("Processing...", expanded=True) as status:
                st.write(":material/search: **Step 1:** Searching documents...")

                try:
                    from snowflake.core import Root

                    root = Root(session)
                    parts = search_service.split(".")

                    if len(parts) != 3:
                        st.error("Service path must be in format: database.schema.service_name")
                        st.stop()

                    svc = (
                        root
                        .databases[parts[0]]
                        .schemas[parts[1]]
                        .cortex_search_services[parts[2]]
                    )

                    search_results = svc.search(
                        query=question,
                        columns=["CHUNK_TEXT", "FILE_NAME"],
                        limit=num_chunks
                    )

                    context_chunks = []
                    sources = []
                    for item in search_results.results:
                        context_chunks.append(item.get("CHUNK_TEXT", ""))
                        sources.append(item.get("FILE_NAME", "Unknown"))

                    context = "\n\n---\n\n".join(context_chunks)

                    st.write(f"   :material/check_circle: Found {len(context_chunks)} relevant chunks")
                    st.write(":material/smart_toy: **Step 2:** Generating answer...")

                    rag_prompt = f"""You are a helpful assistant. Answer the user's question based ONLY on the provided context.
If the context doesn't contain enough information to answer, say "I don't have enough information to answer that based on the available documents."

CONTEXT FROM DOCUMENTS:
{context}

USER QUESTION: {question}

Provide a clear, accurate answer based on the context. If you use information from the context, mention it naturally."""

                    response_sql = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE(
                        '{model}',
                        '{rag_prompt.replace("'", "''")}'
                    ) as response
                    """

                    response = session.sql(response_sql).collect()[0][0]

                    st.write("   :material/check_circle: Answer generated")
                    status.update(label="Complete!", state="complete", expanded=True)

                    st.divider()

                    st.subheader(":material/lightbulb: Answer")
                    with st.container(border=True):
                        st.markdown(response)

                    if show_context:
                        st.subheader(":material/library_books: Retrieved Context")
                        st.caption(f"Used {len(context_chunks)} chunks from customer reviews")
                        for i, (chunk, source) in enumerate(zip(context_chunks, sources), 1):
                            with st.expander(f":material/description: Chunk {i} - {source}"):
                                st.write(chunk)

                except Exception as e:
                    status.update(label="Error", state="error")
                    st.error(f"Error: {str(e)}")
                    st.info(":material/lightbulb: **Troubleshooting:**\n- Make sure the search service exists (check Day 19)\n- Verify the service has finished indexing\n- Check your permissions")
        else:
            st.warning(":material/warning: Please enter a question and configure a search service.")
            st.info(":material/lightbulb: **Need a search service?**\n- Complete Day 19 to create `CUSTOMER_REVIEW_SEARCH`\n- The service will automatically appear in the dropdown above")

# Footer
st.divider()
st.caption("Day 21: RAG with Cortex Search | 30 Days of AI")

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
