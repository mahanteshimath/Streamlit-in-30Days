import streamlit as st

st.set_page_config(page_title="Day 26 - Performance Optimization", page_icon="2️⃣6️⃣")

st.title("Day 26: Performance Optimization")
st.markdown("**Section 4: Advanced Features**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Profile Streamlit apps
- Optimization strategies
- Lazy loading techniques
- Resource management
""")

st.header("📖 Content")

st.subheader("Caching Strategies")
st.code("""
# Cache data loading
@st.cache_data(ttl=3600)
def load_large_dataset():
    return pd.read_csv("large_file.csv")

# Cache resource connections
@st.cache_resource
def get_database_connection():
    return connect_to_db()

# Cache with dependencies
@st.cache_data
def process_data(df, filter_value):
    # Cache invalidates when filter_value changes
    return df[df['column'] == filter_value]

# Selective caching
@st.cache_data(show_spinner="Loading data...")
def expensive_computation(params):
    # Only cache if params are hashable
    if isinstance(params, dict):
        params = tuple(sorted(params.items()))
    return compute(params)
""", language="python")

st.subheader("Lazy Loading")
st.code("""
# Load data only when needed
def lazy_load_model():
    if 'model' not in st.session_state:
        with st.spinner("Loading model..."):
            st.session_state.model = load_ml_model()
    return st.session_state.model

# Use tabs to defer loading
tab1, tab2, tab3 = st.tabs(["Light", "Medium", "Heavy"])

with tab1:
    st.write("Quick content")

with tab2:
    # Only loads when tab is selected
    if st.session_state.get('tab2_loaded') is None:
        data = load_medium_data()
        st.session_state.tab2_loaded = True

with tab3:
    # Heavy computation
    if st.button("Load Heavy Data"):
        heavy_data = load_heavy_data()
        st.write(heavy_data)
""", language="python")

st.subheader("Pagination")
st.code("""
def paginate_dataframe(df, page_size=20):
    # Initialize page number
    if 'page' not in st.session_state:
        st.session_state.page = 0
    
    # Calculate pagination
    total_pages = len(df) // page_size + (1 if len(df) % page_size else 0)
    start_idx = st.session_state.page * page_size
    end_idx = start_idx + page_size
    
    # Display current page
    st.dataframe(df.iloc[start_idx:end_idx])
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous") and st.session_state.page > 0:
            st.session_state.page -= 1
            st.rerun()
    with col2:
        st.write(f"Page {st.session_state.page + 1} of {total_pages}")
    with col3:
        if st.button("Next") and st.session_state.page < total_pages - 1:
            st.session_state.page += 1
            st.rerun()

# Usage
paginate_dataframe(large_df)
""", language="python")

st.subheader("Reducing Reruns")
st.code("""
# Use callbacks instead of if statements
def update_value():
    st.session_state.result = process(st.session_state.input_value)

st.text_input("Input", key="input_value", on_change=update_value)

# Use forms to batch updates
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        # Only runs when form is submitted
        process_data(name, age)

# Use fragments (Streamlit 1.33+)
@st.experimental_fragment
def update_chart():
    # This fragment reruns independently
    data = get_realtime_data()
    st.line_chart(data)

# Main app doesn't rerun when fragment updates
st.title("Dashboard")
update_chart()
""", language="python")

st.subheader("Optimize Data Display")
st.code("""
# Use st.dataframe instead of st.write for large data
st.dataframe(large_df, use_container_width=True)

# Limit displayed rows
st.dataframe(df.head(100))

# Use column_config for better performance
st.dataframe(
    df,
    column_config={
        "image": st.column_config.ImageColumn("Preview"),
        "link": st.column_config.LinkColumn("URL")
    }
)

# For very large datasets, use pagination or filtering
filtered_df = df[df['category'] == selected_category]
st.dataframe(filtered_df)
""", language="python")

st.subheader("Memory Management")
st.code("""
# Clear cache when needed
if st.button("Clear Cache"):
    st.cache_data.clear()
    st.cache_resource.clear()

# Remove large objects from session state
def cleanup_session():
    keys_to_remove = []
    for key in st.session_state:
        obj = st.session_state[key]
        # Remove large objects
        if isinstance(obj, pd.DataFrame) and len(obj) > 10000:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del st.session_state[key]

# Call periodically
if len(st.session_state) > 50:
    cleanup_session()

# Use generators for large data processing
def process_chunks(data, chunk_size=1000):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

for chunk in process_chunks(large_dataset):
    process(chunk)
""", language="python")

st.subheader("Performance Profiling")
st.code("""
import cProfile
import pstats
from io import StringIO

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Your code here
    expensive_operation()
    
    profiler.disable()
    
    # Display results
    s = StringIO()
    ps = pstats.Stats(profiler, stream=s)
    ps.sort_stats('cumulative')
    ps.print_stats(20)
    
    st.code(s.getvalue())

if st.checkbox("Profile Performance"):
    profile_function()
""", language="python")

st.markdown("---")
st.info("✅ Optimize your apps!")

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
