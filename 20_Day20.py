import streamlit as st
from snowflake.core import Root

st.set_page_config(page_title="Day 20 - Querying Cortex Search", page_icon="2️⃣0️⃣", layout="wide")

st.title(":material/search: Day 20: Querying Cortex Search")
st.caption("30 Days of AI")
st.markdown("---")

# Code example section
st.header("🚀 Quick Start - Query Cortex Search")
with st.expander("View Code Snippet", expanded=False):
    st.code("""
    import streamlit as st
    from snowflake.core import Root

    # Connect to Snowflake
    try:
        from snowflake.snowpark.context import get_active_session
        session = get_active_session()
    except:
        from snowflake.snowpark import Session
        session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

    st.title(":material/search: Querying Cortex Search")
    st.write("Search and retrieve relevant text chunks using Cortex Search Service.")

    # Configure search
    search_service = 'RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH'
    query = st.text_input("Enter your search query:", value="warm thermal gloves")
    num_results = st.slider("Number of results:", 1, 20, 5)

    if st.button("Search"):
        root = Root(session)
        parts = search_service.split(".")
        
        svc = (root
            .databases[parts[0]]
            .schemas[parts[1]]
            .cortex_search_services[parts[2]])
        
        results = svc.search(
            query=query,
            columns=["CHUNK_TEXT", "FILE_NAME", "CHUNK_TYPE", "CHUNK_ID"],
            limit=num_results
        )
        
        st.success(f"Found {len(results.results)} result(s)!")
        
        # Display results
        for i, item in enumerate(results.results, 1):
            st.markdown(f"**Result {i}** - {item.get('FILE_NAME', 'N/A')}")
            st.write(item.get("CHUNK_TEXT", "No text found"))
            st.divider()

    st.divider()
    st.caption("Day 20: Querying Cortex Search | 30 Days of AI")
    """, language="python")

st.markdown("---")

# Working Demo
st.header("💬 Try It Yourself!")
st.caption("Using Cortex Search to find relevant customer reviews")

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

    st.write("Search and retrieve relevant text chunks using Cortex Search Service.")

    # Input Container
    with st.container(border=True):
        st.subheader(":material/search: Search Configuration and Query")
        
        # Default search service from Day 19
        default_service = 'RAG_DB.RAG_SCHEMA.CUSTOMER_REVIEW_SEARCH'
        
        # Try to get available services
        try:
            services_result = session.sql("SHOW CORTEX SEARCH SERVICES").collect()
            available_services = [f"{row['database_name']}.{row['schema_name']}.{row['name']}" 
                                for row in services_result] if services_result else []
        except:
            available_services = []
        
        # Ensure default service is always first
        if default_service in available_services:
            available_services.remove(default_service)
        available_services.insert(0, default_service)
        
        # Add manual entry option
        if available_services:
            available_services.append("-- Enter manually --")
            
            search_service_option = st.selectbox(
                "Search Service:",
                options=available_services,
                index=0,
                help="Select your Cortex Search service from Day 19"
            )
            
            # If manual entry selected, show text input
            if search_service_option == "-- Enter manually --":
                search_service = st.text_input(
                    "Enter service path:",
                    placeholder="database.schema.service_name"
                )
            else:
                search_service = search_service_option
                
                # Show status if this is the Day 19 service
                if search_service == st.session_state.get('search_service'):
                    st.success(":material/check_circle: Using service from Day 19")
        else:
            # Fallback to text input if no services found
            search_service = st.text_input(
                "Search Service:",
                value=default_service,
                placeholder="database.schema.service_name",
                help="Full path to your Cortex Search service"
            )
        
        st.code(search_service, language="sql")
        st.caption(":material/lightbulb: This should point to your CUSTOMER_REVIEW_SEARCH service from Day 19")

        st.divider()

        # Search query input
        query = st.text_input(
            "Enter your search query:",
            value="warm thermal gloves",
            placeholder="e.g., durability issues, comfortable helmet"
        )

        num_results = st.slider("Number of results:", 1, 20, 5)
        
        search_clicked = st.button(":material/search: Search", type="primary", use_container_width=True)

    # Output Container
    with st.container(border=True):
        st.subheader(":material/analytics: Search Results")
        
        if search_clicked:
            if query and search_service:
                try:
                    root = Root(session)
                    parts = search_service.split(".")
                    
                    if len(parts) != 3:
                        st.error("Service path must be in format: database.schema.service_name")
                    else:
                        svc = (root
                            .databases[parts[0]]
                            .schemas[parts[1]]
                            .cortex_search_services[parts[2]])
                        
                        with st.spinner("Searching..."):
                            results = svc.search(
                                query=query,
                                columns=["CHUNK_TEXT", "FILE_NAME", "CHUNK_TYPE", "CHUNK_ID"],
                                limit=num_results
                            )
                        
                        st.success(f":material/check_circle: Found {len(results.results)} result(s)!")
                        
                        # Display results
                        for i, item in enumerate(results.results, 1):
                            with st.container(border=True):
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col1:
                                    st.markdown(f"**Result {i}** - {item.get('FILE_NAME', 'N/A')}")
                                with col2:
                                    st.caption(f"Type: {item.get('CHUNK_TYPE', 'N/A')}")
                                with col3:
                                    st.caption(f"Chunk: {item.get('CHUNK_ID', 'N/A')}")
                                
                                st.write(item.get("CHUNK_TEXT", "No text found"))
                                
                                # Show relevance score if available
                                if hasattr(item, 'score') or 'score' in item:
                                    score = item.get('score', item.score if hasattr(item, 'score') else None)
                                    if score is not None:
                                        st.caption(f"Relevance Score: {score:.4f}")
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    st.info(":material/lightbulb: **Troubleshooting:**\n- Make sure the search service exists (check Day 19)\n- Verify the service has finished indexing\n- Check that you have access permissions")
            else:
                st.warning(":material/warning: Please enter a query and configure a search service.")
                st.info(":material/lightbulb: **Need a search service?**\n- Complete Day 19 to create `CUSTOMER_REVIEW_SEARCH`\n- The service will automatically appear in the dropdown above")
        else:
            st.info(":material/arrow_upward: Configure your search service and enter a query above, then click Search to see results.")

    st.divider()
    st.caption("Day 20: Querying Cortex Search | 30 Days of AI")

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
