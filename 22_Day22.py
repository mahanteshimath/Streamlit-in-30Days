import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Day 22 - Chat with Your Documents", page_icon="2️⃣2️⃣", layout="wide")

st.title(":material/chat: Day 22: Chat with Your Documents")
st.caption("30 Days of AI")
st.write("A conversational RAG chatbot powered by Cortex Search.")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code('''
    import streamlit as st
    from snowflake.snowpark.context import get_active_session

    st.title(":material/chat: Chat with Your Documents")
    st.write("A conversational RAG chatbot powered by Cortex Search.")

    # Get the current credentials
    session = get_active_session()

    # Initialize state
    if "doc_messages" not in st.session_state:
        st.session_state.doc_messages = []

    # Sidebar
    with st.sidebar:
        st.header(":material/settings: Settings")
        default_service = st.session_state.get("search_service", "RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH")

        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [
                f"{row['database_name']}.{row['schema_name']}.{row['name']}"
                for row in services_result
            ] if services_result else []
        except:
            available_services = []

        if default_service:
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
            search_service = st.text_input(
                "Cortex Search Service:",
                value=default_service,
                placeholder="database.schema.service_name"
            )

        num_chunks = st.slider("Context chunks:", 1, 5, 3)

        st.divider()

        if st.button(":material/delete: Clear Chat", use_container_width=True):
            st.session_state.doc_messages = []
            st.rerun()

    def search_documents(query, service_path, limit):
        from snowflake.core import Root
        root = Root(session)
        parts = service_path.split(".")
        if len(parts) != 3:
            raise ValueError("Service path must be in format: database.schema.service_name")
        svc = root.databases[parts[0]].schemas[parts[1]].cortex_search_services[parts[2]]
        results = svc.search(query=query, columns=["CHUNK_TEXT", "FILE_NAME"], limit=limit)

        chunks_data = []
        for item in results.results:
            chunks_data.append({
                "text": item.get("CHUNK_TEXT", ""),
                "source": item.get("FILE_NAME", "Unknown")
            })
        return chunks_data

    if not search_service:
        st.info(":material/arrow_back: Configure a Cortex Search service to start chatting!")
    else:
        for msg in st.session_state.doc_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask about your documents..."):
            st.session_state.doc_messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Searching and thinking..."):
                    chunks_data = search_documents(prompt, search_service, num_chunks)
                    context = "\n\n---\n\n".join([c["text"] for c in chunks_data])

                    rag_prompt = f"""You are a customer review analysis assistant. Your role is to ONLY answer questions about customer reviews and feedback.

    STRICT GUIDELINES:
    1. ONLY use information from the provided customer review context below
    2. If asked about topics unrelated to customer reviews (e.g., general knowledge, coding, math, news), respond: "I can only answer questions about customer reviews. Please ask about product feedback, customer experiences, or review insights."
    3. If the context doesn't contain relevant information, say: "I don't have enough information in the customer reviews to answer that."
    4. Stay focused on: product features, customer satisfaction, complaints, praise, quality, pricing, shipping, or customer service mentioned in reviews
    5. Do NOT make up information or use knowledge outside the provided reviews

    CONTEXT FROM CUSTOMER REVIEWS:
    {context}

    USER QUESTION: {prompt}

    Provide a clear, helpful answer based ONLY on the customer reviews above. If you cite information, mention it naturally."""

                    sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', '{rag_prompt.replace("'", "''")}')"
                    response = session.sql(sql).collect()[0][0]

                st.markdown(response)

                with st.expander(f":material/library_books: Sources ({len(chunks_data)} reviews used)"):
                    for i, chunk_info in enumerate(chunks_data, 1):
                        st.caption(f"**[{i}] {chunk_info['source']}**")
                        st.write(chunk_info["text"][:200] + "..." if len(chunk_info["text"]) > 200 else chunk_info["text"])

                st.session_state.doc_messages.append({"role": "assistant", "content": response})

    st.divider()
    st.caption("Day 22: Chat with Your Documents | 30 Days of AI")
    ''', language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("💬 Try It Yourself!")
st.caption("Using default Snowflake connection - conversational RAG with document grounding.")

try:
    if "default_session" not in st.session_state:
        try:
            st.session_state.default_session = get_active_session()
        except:
            from snowflake.snowpark import Session
            if "connections" in st.secrets and "my_example_connection" in st.secrets["connections"]:
                st.session_state.default_session = Session.builder.configs(
                    st.secrets["connections"]["my_example_connection"]
                ).create()
            else:
                raise Exception("No Snowflake connection configured in secrets.toml")

    session = st.session_state.default_session
    st.success("✅ Connected to Snowflake!")

    if "doc_messages" not in st.session_state:
        st.session_state.doc_messages = []

    with st.sidebar:
        st.header(":material/settings: Settings")

        default_service = st.session_state.get("search_service", "RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH")

        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [
                f"{row['database_name']}.{row['schema_name']}.{row['name']}"
                for row in services_result
            ] if services_result else []
        except:
            available_services = []

        if default_service:
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
                "Cortex Search Service:",
                value=default_service,
                placeholder="database.schema.service_name"
            )

        num_chunks = st.slider("Context chunks:", 1, 5, 3,
                               help="Number of relevant chunks to retrieve per question")

        st.divider()

        if st.button(":material/delete: Clear Chat", use_container_width=True):
            st.session_state.doc_messages = []
            st.rerun()

    def search_documents(query, service_path, limit):
        from snowflake.core import Root
        root = Root(session)
        parts = service_path.split(".")
        if len(parts) != 3:
            raise ValueError("Service path must be in format: database.schema.service_name")
        svc = root.databases[parts[0]].schemas[parts[1]].cortex_search_services[parts[2]]
        results = svc.search(query=query, columns=["CHUNK_TEXT", "FILE_NAME"], limit=limit)

        chunks_data = []
        for item in results.results:
            chunks_data.append({
                "text": item.get("CHUNK_TEXT", ""),
                "source": item.get("FILE_NAME", "Unknown")
            })
        return chunks_data

    if not search_service:
        st.info(":material/arrow_back: Configure a Cortex Search service to start chatting!")
        st.caption(":material/lightbulb: **Need a search service?**\n- Complete Day 19 to create `CUSTOMER_REVIEW_SEARCH`\n- The service will automatically appear in the dropdown above")
    else:
        for msg in st.session_state.doc_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask about your documents..."):
            st.session_state.doc_messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Searching and thinking..."):
                        chunks_data = search_documents(prompt, search_service, num_chunks)
                        context = "\n\n---\n\n".join([c["text"] for c in chunks_data])

                        rag_prompt = f"""You are a customer review analysis assistant. Your role is to ONLY answer questions about customer reviews and feedback.

STRICT GUIDELINES:
1. ONLY use information from the provided customer review context below
2. If asked about topics unrelated to customer reviews (e.g., general knowledge, coding, math, news), respond: "I can only answer questions about customer reviews. Please ask about product feedback, customer experiences, or review insights."
3. If the context doesn't contain relevant information, say: "I don't have enough information in the customer reviews to answer that."
4. Stay focused on: product features, customer satisfaction, complaints, praise, quality, pricing, shipping, or customer service mentioned in reviews
5. Do NOT make up information or use knowledge outside the provided reviews

CONTEXT FROM CUSTOMER REVIEWS:
{context}

USER QUESTION: {prompt}

Provide a clear, helpful answer based ONLY on the customer reviews above. If you cite information, mention it naturally."""

                        sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', '{rag_prompt.replace("'", "''")}')"
                        response = session.sql(sql).collect()[0][0]

                    st.markdown(response)

                    with st.expander(f":material/library_books: Sources ({len(chunks_data)} reviews used)"):
                        for i, chunk_info in enumerate(chunks_data, 1):
                            st.caption(f"**[{i}] {chunk_info['source']}**")
                            st.write(chunk_info["text"][:200] + "..." if len(chunk_info["text"]) > 200 else chunk_info["text"])

                    st.session_state.doc_messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info(":material/lightbulb: **Troubleshooting:**\n- Make sure the search service exists (check Day 19)\n- Verify the service has finished indexing\n- Check your permissions")

    st.markdown("---")

    with st.expander(":material/info: See the explanation"):
        st.markdown("""
        **How It Works: Step-by-Step**

        1. **Initialize Conversation State**
           - `st.session_state.doc_messages` stores the full chat history.

        2. **Smart Service Selection**
           - Auto-detects Cortex Search services.
           - Default service is always first and manual entry is supported.

        3. **Retrieval per Question**
           - Each user message triggers a fresh search for best relevance.

        4. **Guardrails in the Prompt**
           - Restricts answers to customer reviews only.
           - Prevents off-topic responses.

        5. **Answer + Sources**
           - Returns a grounded response.
           - Shows expandable sources with file names.
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
    st.subheader("💬 Try It Yourself!")
    st.caption("Using your custom connection")

    session = st.session_state.custom_session

    if "custom_doc_messages" not in st.session_state:
        st.session_state.custom_doc_messages = []

    with st.sidebar:
        st.header(":material/settings: Custom Settings")

        default_service = st.session_state.get("search_service", "RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH")

        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [
                f"{row['database_name']}.{row['schema_name']}.{row['name']}"
                for row in services_result
            ] if services_result else []
        except:
            available_services = []

        if default_service:
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
                "Cortex Search Service:",
                value=default_service,
                placeholder="database.schema.service_name",
                key="custom_service_input"
            )

        num_chunks = st.slider("Context chunks:", 1, 5, 3,
                               help="Number of relevant chunks to retrieve per question",
                               key="custom_num_chunks")

        st.divider()

        if st.button(":material/delete: Clear Chat", use_container_width=True, key="custom_clear"):
            st.session_state.custom_doc_messages = []
            st.rerun()

    def search_documents_custom(query, service_path, limit):
        from snowflake.core import Root
        root = Root(session)
        parts = service_path.split(".")
        if len(parts) != 3:
            raise ValueError("Service path must be in format: database.schema.service_name")
        svc = root.databases[parts[0]].schemas[parts[1]].cortex_search_services[parts[2]]
        results = svc.search(query=query, columns=["CHUNK_TEXT", "FILE_NAME"], limit=limit)

        chunks_data = []
        for item in results.results:
            chunks_data.append({
                "text": item.get("CHUNK_TEXT", ""),
                "source": item.get("FILE_NAME", "Unknown")
            })
        return chunks_data

    if not search_service:
        st.info(":material/arrow_back: Configure a Cortex Search service to start chatting!")
    else:
        for msg in st.session_state.custom_doc_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt := st.chat_input("Ask about your documents...", key="custom_prompt"):
            st.session_state.custom_doc_messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                try:
                    with st.spinner("Searching and thinking..."):
                        chunks_data = search_documents_custom(prompt, search_service, num_chunks)
                        context = "\n\n---\n\n".join([c["text"] for c in chunks_data])

                        rag_prompt = f"""You are a customer review analysis assistant. Your role is to ONLY answer questions about customer reviews and feedback.

STRICT GUIDELINES:
1. ONLY use information from the provided customer review context below
2. If asked about topics unrelated to customer reviews (e.g., general knowledge, coding, math, news), respond: "I can only answer questions about customer reviews. Please ask about product feedback, customer experiences, or review insights."
3. If the context doesn't contain relevant information, say: "I don't have enough information in the customer reviews to answer that."
4. Stay focused on: product features, customer satisfaction, complaints, praise, quality, pricing, shipping, or customer service mentioned in reviews
5. Do NOT make up information or use knowledge outside the provided reviews

CONTEXT FROM CUSTOMER REVIEWS:
{context}

USER QUESTION: {prompt}

Provide a clear, helpful answer based ONLY on the customer reviews above. If you cite information, mention it naturally."""

                        sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('claude-3-5-sonnet', '{rag_prompt.replace("'", "''")}')"
                        response = session.sql(sql).collect()[0][0]

                    st.markdown(response)

                    with st.expander(f":material/library_books: Sources ({len(chunks_data)} reviews used)"):
                        for i, chunk_info in enumerate(chunks_data, 1):
                            st.caption(f"**[{i}] {chunk_info['source']}**")
                            st.write(chunk_info["text"][:200] + "..." if len(chunk_info["text"]) > 200 else chunk_info["text"])

                    st.session_state.custom_doc_messages.append({"role": "assistant", "content": response})

                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info(":material/lightbulb: **Troubleshooting:**\n- Make sure the search service exists (check Day 19)\n- Verify the service has finished indexing\n- Check your permissions")

# Footer
st.divider()
st.caption("Day 22: Chat with Your Documents | 30 Days of AI")

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
