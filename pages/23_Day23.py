import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="Day 23 - LLM Evaluation & AI Observability", page_icon="2️⃣3️⃣", layout="wide")

st.title(":material/analytics: Day 23: LLM Evaluation & AI Observability")
st.caption("30 Days of AI")
st.write("Evaluate your RAG application quality using TruLens and Snowflake AI Observability.")
st.markdown("---")

# Default Connection
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code('''
    import streamlit as st
    from snowflake.snowpark.context import get_active_session

    # Get the current credentials
    session = get_active_session()

    # Initialize session state for run counter
    if "run_counter" not in st.session_state:
        st.session_state.run_counter = 1

    try:
        from trulens.connectors.snowflake import SnowflakeConnector
        from trulens.core.run import Run, RunConfig
        from trulens.core import TruSession
        from trulens.core.otel.instrument import instrument
        import pandas as pd
        import time
        trulens_available = True
    except ImportError as e:
        trulens_available = False
        trulens_error = str(e)

    st.title(":material/analytics: LLM Evaluation & AI Observability")
    st.write("Evaluate your RAG application quality using TruLens and Snowflake AI Observability.")

    with st.expander("Why Evaluate LLMs?", expanded=False):
        st.markdown("""
        After building a RAG application (Days 21-22), you need to measure its quality:

        **The RAG Triad Metrics:**
        1. **Context Relevance**
        2. **Groundedness**
        3. **Answer Relevance**
        """)

    if trulens_available:
        st.success(":material/check_circle: TruLens packages are installed and ready!")
    else:
        st.error(f":material/cancel: TruLens packages not found: {trulens_error}")
        st.info("""
        **Required packages:**
        - `trulens-core`
        - `trulens-providers-cortex`
        - `trulens-connectors-snowflake`
        """)

    with st.sidebar:
        st.header(":material/settings: Configuration")

        with st.expander("Search Service", expanded=True):
            search_service = st.text_input(
                "Cortex Search Service:",
                value="RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH",
                help="Format: database.schema.service_name (created in Day 19)"
            )

        with st.expander("Location", expanded=False):
            obs_database = st.text_input("Database:", value="RAG_DB")
            obs_schema = st.text_input("Schema:", value="RAG_SCHEMA")

        num_results = st.slider("Results to retrieve:", 1, 5, 3)

    if trulens_available:
        with st.container(border=True):
            st.markdown("##### :material/settings_suggest: Evaluation Configuration")

            app_name = st.text_input(
                "App Name:",
                value="customer_review_rag",
                help="Name for your RAG application"
            )

            app_version = st.text_input(
                "App Version:",
                value=f"v{st.session_state.run_counter}",
                help="Version identifier for this experiment"
            )

            rag_model = st.selectbox(
                "RAG Model:",
                ["claude-3-5-sonnet", "mixtral-8x7b", "llama3-70b", "llama3.1-8b"],
                help="Model for generating answers"
            )

            st.markdown("##### :material/dataset: Test Questions")
            test_questions_text = st.text_area(
                "Questions (one per line):",
                value=(
                    "What do customers say about thermal gloves?\n"
                    "Are there any durability complaints?\n"
                    "Which products get the best reviews?"
                ),
                height=150
            )

            run_evaluation = st.button(":material/science: Run TruLens Evaluation", type="primary")

        if run_evaluation:
            test_questions = [q.strip() for q in test_questions_text.split("\n") if q.strip()]

            if not test_questions:
                st.error("Please enter at least one question.")
                st.stop()

            with st.status("Running TruLens evaluation...", expanded=True) as status:
                st.write(":orange[:material/check:] Preparing test dataset...")

                session.use_database(obs_database)
                session.use_schema(obs_schema)

                test_data = [{"QUERY": q, "QUERY_ID": i + 1} for i, q in enumerate(test_questions)]
                test_df = pd.DataFrame(test_data)

                dataset_table = "CUSTOMER_REVIEW_TEST_QUESTIONS"
                session.sql(f"DROP TABLE IF EXISTS {dataset_table}").collect()
                session.create_dataframe(test_df).write.mode("overwrite").save_as_table(dataset_table)

                st.write(f":orange[:material/check:] Created dataset table: `{obs_database}.{obs_schema}.{dataset_table}`")

                class CustomerReviewRAG:
                    def __init__(self, snowpark_session):
                        self.session = snowpark_session
                        self.search_service = search_service
                        self.num_results = num_results
                        self.model = rag_model

                    @instrument()
                    def retrieve_context(self, query: str) -> str:
                        from snowflake.core import Root
                        root = Root(self.session)
                        parts = self.search_service.split(".")
                        svc = root.databases[parts[0]].schemas[parts[1]].cortex_search_services[parts[2]]
                        results = svc.search(query=query, columns=["CHUNK_TEXT"], limit=self.num_results)
                        return "\n\n".join([r["CHUNK_TEXT"] for r in results.results])

                    @instrument()
                    def generate_completion(self, query: str, context: str) -> str:
                        prompt = f"""Based on this context from customer reviews:

    {context}

    Question: {query}

    Provide a helpful answer based on the context above:"""
                        prompt_escaped = prompt.replace("'", "''")
                        response = self.session.sql(
                            f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{self.model}', '{prompt_escaped}')"
                        ).collect()[0][0]
                        return response.strip()

                    @instrument()
                    def query(self, query: str) -> str:
                        context = self.retrieve_context(query)
                        return self.generate_completion(query, context)

                st.write(":orange[:material/check:] Registering app with TruLens...")

                if hasattr(TruSession, "_singleton_instances"):
                    TruSession._singleton_instances.clear()

                tru_connector = SnowflakeConnector(snowpark_session=session)
                tru_session = TruSession(connector=tru_connector)

                rag_app = CustomerReviewRAG(session)
                unique_app_version = f"{app_version}_{st.session_state.run_counter}"

                tru_rag = tru_session.App(
                    rag_app,
                    app_name=app_name,
                    app_version=unique_app_version,
                    main_method=rag_app.query
                )

                run_config = RunConfig(
                    run_name=f"{unique_app_version}",
                    dataset_name=dataset_table,
                    description=f"Customer review RAG evaluation using {rag_model}",
                    label="customer_review_eval",
                    source_type="TABLE",
                    dataset_spec={"input": "QUERY"},
                )

                run: Run = tru_rag.add_run(run_config=run_config)
                run.start()

                generated_answers = {}
                for idx, question in enumerate(test_questions, 1):
                    st.write(
                        f"  :orange[:material/check:] Question {idx}/{len(test_questions)}: {question[:60]}"
                        f"{'...' if len(question) > 60 else ''}"
                    )
                    generated_answers[question] = rag_app.query(question)

                st.write(":orange[:material/check:] Computing RAG Triad metrics...")
                try:
                    run.compute_metrics(["answer_relevance", "context_relevance", "groundedness"])
                    st.write(":orange[:material/check:] Metrics computed successfully!")
                except Exception as e:
                    st.warning(f"Metrics computation: {str(e)}")

                st.write(":orange[:material/check:] Evaluation complete!")
                status.update(label="Evaluation complete", state="complete")

                st.session_state.run_counter += 1

            with st.container(border=True):
                st.markdown("#### :material/analytics: Evaluation Results")
                st.success(f"""
    :material/check: **Evaluation Run Complete!**

    **Run Details:**
    - App Name: **{app_name}**
    - App Version: **{unique_app_version}**
    - Questions Evaluated: **{len(test_questions)}**
    - Model: **{rag_model}**

    **View Results in Snowsight:**
    AI & ML → Evaluations → {app_name}
                """)

                with st.expander("Generated Answers", expanded=True):
                    for idx, question in enumerate(test_questions, 1):
                        st.markdown(f"**Question {idx}:** {question}")
                        st.info(generated_answers.get(question, "No answer generated"))
                        if idx < len(test_questions):
                            st.markdown("---")

    st.divider()
    st.caption("Day 23: LLM Evaluation & AI Observability | 30 Days of AI")
    ''', language="python")

st.markdown("---")

# Working Demo with Default Connection
st.header("🧪 Try It Yourself!")
st.caption("Using default Snowflake connection - evaluate your RAG app with TruLens.")

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

    if "run_counter" not in st.session_state:
        st.session_state.run_counter = 1

    try:
        from trulens.connectors.snowflake import SnowflakeConnector
        from trulens.core.run import Run, RunConfig
        from trulens.core import TruSession
        from trulens.core.otel.instrument import instrument
        import pandas as pd
        import time
        trulens_available = True
    except ImportError as e:
        trulens_available = False
        trulens_error = str(e)

    with st.expander("Why Evaluate LLMs?", expanded=False):
        st.markdown("""
        **The RAG Triad Metrics:**
        1. Context Relevance : easures whether the search system (Cortex Search) retrieved documents that are actually related to the user's question. A low score means your search needs tuning.
        2. Groundedness: Checks if the LLM's answer comes from the provided context or if it's making things up (hallucinating). High groundedness = no hallucinations
        3. Answer Relevance: Evaluates whether the final answer actually addresses what the user asked. You can have great context and grounding but still give an irrelevant answer.
        """)

    if trulens_available:
        st.success(":material/check_circle: TruLens packages are installed and ready!")
    else:
        st.error(f":material/cancel: TruLens packages not found: {trulens_error}")
        st.info("""
        **Required packages:**
        - `trulens-core`
        - `trulens-providers-cortex`
        - `trulens-connectors-snowflake`
        """)

    with st.sidebar:
        st.header(":material/settings: Configuration")

        with st.expander("Search Service", expanded=True):
            search_service = st.text_input(
                "Cortex Search Service:",
                value="RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH",
                help="Format: database.schema.service_name (created in Day 19)"
            )

        with st.expander("Location", expanded=False):
            obs_database = st.text_input("Database:", value="RAG_DB")
            obs_schema = st.text_input("Schema:", value="RAG_SCHEMA")

        num_results = st.slider("Results to retrieve:", 1, 5, 3)

        with st.expander("Stage Status", expanded=False):
            full_stage_name = f"{obs_database}.{obs_schema}.TRULENS_STAGE"
            try:
                stage_info = session.sql(
                    f"SHOW STAGES LIKE 'TRULENS_STAGE' IN SCHEMA {obs_database}.{obs_schema}"
                ).collect()

                if stage_info:
                    session.sql(f"DROP STAGE IF EXISTS {full_stage_name}").collect()

                session.sql(f"""
                CREATE STAGE {full_stage_name}
                    DIRECTORY = ( ENABLE = true )
                    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' )
                """).collect()

                st.success(":material/check_box: TruLens stage ready")
            except Exception as e:
                st.error(f":material/cancel: Could not create stage: {str(e)}")

                with st.expander(":material/build: Manual Fix"):
                    st.code(f"""
DROP STAGE IF EXISTS {full_stage_name};
CREATE STAGE {full_stage_name}
    DIRECTORY = ( ENABLE = true )
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );
                    """, language="sql")

            if st.button(":material/autorenew: Recreate Stage"):
                try:
                    session.sql(f"DROP STAGE IF EXISTS {full_stage_name}").collect()
                    session.sql(f"""
                    CREATE STAGE {full_stage_name}
                        DIRECTORY = ( ENABLE = true )
                        ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' )
                    """).collect()
                    st.success(":material/check_circle: Stage recreated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to recreate stage: {str(e)}")

    if trulens_available:
        with st.container(border=True):
            st.markdown("##### :material/settings_suggest: Evaluation Configuration")

            app_name = st.text_input("App Name:", value="customer_review_rag")
            app_version = st.text_input("App Version:", value=f"v{st.session_state.run_counter}")
            rag_model = st.selectbox(
                "RAG Model:",
                ["claude-3-5-sonnet", "mixtral-8x7b", "llama3-70b", "llama3.1-8b"],
                key="trulens_model"
            )

            test_questions_text = st.text_area(
                "Questions (one per line):",
                value=(
                    "What do customers say about thermal gloves?\n"
                    "Are there any durability complaints?\n"
                    "Which products get the best reviews?"
                ),
                height=150
            )

            run_evaluation = st.button(":material/science: Run TruLens Evaluation", type="primary")

        if run_evaluation:
            test_questions = [q.strip() for q in test_questions_text.split("\n") if q.strip()]

            if not test_questions:
                st.error("Please enter at least one question.")
                st.stop()

            try:
                with st.status("Running TruLens evaluation...", expanded=True) as status:
                    session.use_database(obs_database)
                    session.use_schema(obs_schema)

                    test_data = [{"QUERY": q, "QUERY_ID": i + 1} for i, q in enumerate(test_questions)]
                    test_df = pd.DataFrame(test_data)

                    dataset_table = "CUSTOMER_REVIEW_TEST_QUESTIONS"
                    session.sql(f"DROP TABLE IF EXISTS {dataset_table}").collect()
                    session.create_dataframe(test_df).write.mode("overwrite").save_as_table(dataset_table)

                    class CustomerReviewRAG:
                        def __init__(self, snowpark_session):
                            self.session = snowpark_session
                            self.search_service = search_service
                            self.num_results = num_results
                            self.model = rag_model

                        @instrument()
                        def retrieve_context(self, query: str) -> str:
                            from snowflake.core import Root
                            root = Root(self.session)
                            parts = self.search_service.split(".")
                            svc = root.databases[parts[0]].schemas[parts[1]].cortex_search_services[parts[2]]
                            results = svc.search(query=query, columns=["CHUNK_TEXT"], limit=self.num_results)
                            return "\n\n".join([r["CHUNK_TEXT"] for r in results.results])

                        @instrument()
                        def generate_completion(self, query: str, context: str) -> str:
                            prompt = f"""Based on this context from customer reviews:

{context}

Question: {query}

Provide a helpful answer based on the context above:"""
                            prompt_escaped = prompt.replace("'", "''")
                            response = self.session.sql(
                                f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{self.model}', '{prompt_escaped}')"
                            ).collect()[0][0]
                            return response.strip()

                        @instrument()
                        def query(self, query: str) -> str:
                            context = self.retrieve_context(query)
                            return self.generate_completion(query, context)

                    if hasattr(TruSession, "_singleton_instances"):
                        TruSession._singleton_instances.clear()

                    tru_connector = SnowflakeConnector(snowpark_session=session)
                    tru_session = TruSession(connector=tru_connector)

                    rag_app = CustomerReviewRAG(session)
                    unique_app_version = f"{app_version}_{st.session_state.run_counter}"

                    tru_rag = tru_session.App(
                        rag_app,
                        app_name=app_name,
                        app_version=unique_app_version,
                        main_method=rag_app.query
                    )

                    run_config = RunConfig(
                        run_name=f"{unique_app_version}",
                        dataset_name=dataset_table,
                        description=f"Customer review RAG evaluation using {rag_model}",
                        label="customer_review_eval",
                        source_type="TABLE",
                        dataset_spec={"input": "QUERY"},
                    )

                    run: Run = tru_rag.add_run(run_config=run_config)
                    run.start()

                    generated_answers = {}
                    for idx, question in enumerate(test_questions, 1):
                        st.write(
                            f"  :orange[:material/check:] Question {idx}/{len(test_questions)}: {question[:60]}"
                            f"{'...' if len(question) > 60 else ''}"
                        )
                        generated_answers[question] = rag_app.query(question)

                    try:
                        run.compute_metrics(["answer_relevance", "context_relevance", "groundedness"])
                        st.write(":orange[:material/check:] Metrics computed successfully!")
                    except Exception as e:
                        st.warning(f"Metrics computation: {str(e)}")

                    st.write(":orange[:material/check:] Evaluation complete!")
                    status.update(label="Evaluation complete", state="complete")

                    st.session_state.run_counter += 1

                with st.container(border=True):
                    st.markdown("#### :material/analytics: Evaluation Results")
                    st.success(f"""
:material/check: **Evaluation Run Complete!**

**Run Details:**
- App Name: **{app_name}**
- App Version: **{unique_app_version}**
- Questions Evaluated: **{len(test_questions)}**
- Model: **{rag_model}**

**View Results in Snowsight:**
AI & ML → Evaluations → {app_name}
                    """)

                    with st.expander("Generated Answers", expanded=True):
                        for idx, question in enumerate(test_questions, 1):
                            st.markdown(f"**Question {idx}:** {question}")
                            st.info(generated_answers.get(question, "No answer generated"))
                            if idx < len(test_questions):
                                st.markdown("---")

                with st.expander(":material/help: Accessing Evaluation Results in Snowsight", expanded=False):
                    st.markdown("""
After the app shows the success message that the evaluation is complete, follow these steps to view detailed metrics:

**Step-by-Step Instructions:**

1. **Open Snowsight** and log in to your Snowflake account

2. **Navigate to the Evaluations page:**
   - In the left sidebar, click on **AI & ML**
   - Then click on **Evaluations**
   - Or use this direct link: [Snowflake AI Evaluations](https://app.snowflake.com/evaluations)

3. **Find your evaluation:**
   - In the displayed data table, look for the **Name** column
   - Find **CUSTOMER_REVIEW_RAG** (or your custom app name if you changed it)
   - Click on the app name to open the evaluation details

4. **View detailed results:**
   - **RAG Triad scores** for each question:
     - Context Relevance (retrieval quality)
     - Groundedness (hallucination detection)
     - Answer Relevance (answer quality)
   - **Response metrics:** Length and duration for each query
   - **Detailed traces:** Step-by-step view of retrieval and generation
   - **Version comparison:** Compare metrics across multiple runs/versions
   - **Individual query details:** Click on any question to see its full trace

5. **What to look for:**
   - Scores range from **0 to 1** (higher is better)
   - Scores below **0.7** indicate areas that need improvement
   - Compare scores across different versions to track improvements

---

**Key Concepts**

**Why Use TruLens?**
- **Automated evaluation:** No manual scoring required
- **Production-ready:** Scales to thousands of evaluations
- **Integrated storage:** Results stored in Snowflake automatically
- **Experiment tracking:** Compare different models, prompts, and configurations
- **Detailed tracing:** See exactly what happened at each step

**TruLens vs Manual Evaluation:**

| Aspect | TruLens | Manual LLM-as-a-Judge |
|--------|---------|----------------------|
| Setup | Requires instrumentation | Custom prompts needed |
| Metrics | RAG Triad built-in | Must define evaluation prompts |
| Storage | Automatic in Snowflake | Must implement yourself |
| Tracing | Automatic method tracking | Manual logging required |
| Comparison | Built-in UI in Snowsight | Must build dashboards |

**Best Practices:**
- **Unique app versions:** Use version numbers to track experiments
- **Representative questions:** Include edge cases in your test set
- **Regular evaluation:** Run before deploying changes
- **Analyze patterns:** Look for consistently low-scoring question types
- **Iterate based on metrics:** Use scores to guide improvements

**When to Run Evaluations:**
- **Development:** After changing prompts, models, or retrieval settings
- **Pre-deployment:** Before releasing to production
- **Regression testing:** Ensure quality doesn't degrade
- **A/B testing:** Compare different configurations

**Interpreting RAG Triad Scores:**

- **Context Relevance < 0.7:** Your search quality needs improvement
  - *Solution:* Tune chunk size, improve embeddings, or adjust search parameters

- **Groundedness < 0.7:** The LLM is hallucinating or extrapolating
  - *Solution:* Add stronger grounding instructions to your prompt

- **Answer Relevance < 0.7:** The answer doesn't address the question
  - *Solution:* Refine prompt instructions or provide examples
                    """)

            except Exception as e:
                st.error(f"Error during evaluation: {str(e)}")
                with st.expander("See full error details"):
                    st.exception(e)

                st.info("""
                **Troubleshooting:**
                - Ensure required packages are installed
                - Check that your Cortex Search service is accessible
                - Verify database and schema permissions
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
    st.subheader("🧪 Try It Yourself!")
    st.caption("Using your custom connection")

    session = st.session_state.custom_session

    if "run_counter" not in st.session_state:
        st.session_state.run_counter = 1

    try:
        from trulens.connectors.snowflake import SnowflakeConnector
        from trulens.core.run import Run, RunConfig
        from trulens.core import TruSession
        from trulens.core.otel.instrument import instrument
        import pandas as pd
        trulens_available = True
    except ImportError as e:
        trulens_available = False
        trulens_error = str(e)

    if trulens_available:
        st.success(":material/check_circle: TruLens packages are installed and ready!")
    else:
        st.error(f":material/cancel: TruLens packages not found: {trulens_error}")

# Footer
st.divider()
st.caption("Day 23: LLM Evaluation & AI Observability | 30 Days of AI with Streamlit")

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
