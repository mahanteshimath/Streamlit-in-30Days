import streamlit as st

st.set_page_config(page_title="Day 9 - Understanding Session State", page_icon="9️⃣", layout="wide")

st.title(":material/memory: Day 9: Understanding Session State")
st.caption("30 Days of AI")
st.markdown("---")

# Quick Start
st.header("🚀 Quick Start - Session State Basics")
with st.expander("View Code Snippet", expanded=False):
    st.code("""
    import streamlit as st

    st.title(":material/memory: Understanding Session State")

    # Create two columns for side-by-side comparison
    col1, col2 = st.columns(2)

    # --- COLUMN 1: THE WRONG WAY ---
    with col1:
        st.header(":material/cancel: Standard Variable")
        st.write("This resets on every click.")
        
        # This line runs every time you click ANY button on the page.
        # It effectively erases your progress immediately.
        count_wrong = 0
        
        subcol_left, subcol_right = st.columns(2)
        
        with subcol_left:
            if st.button(":material/add:", key="std_plus"):
                count_wrong += 1
        
        with subcol_right:
            if st.button(":material/remove:", key="std_minus"):
                count_wrong -= 1
        
        st.metric("Standard Count", count_wrong)
        st.caption("It never gets past 1 or -1 because `count_wrong` resets to 0 before the math happens.")

    # --- COLUMN 2: THE RIGHT WAY ---
    with col2:
        st.header(":material/check_circle: Session State")
        st.write("This memory persists.")
        
        # 1. Initialization: Create the key only if it doesn't exist yet
        if "counter" not in st.session_state:
            st.session_state.counter = 0
        
        subcol_left_2, subcol_right_2 = st.columns(2)
        
        with subcol_left_2:
            # 2. Modification: Update the dictionary value (Increment)
            if st.button(":material/add:", key="state_plus"):
                st.session_state.counter += 1
        
        with subcol_right_2:
            # 2. Modification: Update the dictionary value (Decrement)
            if st.button(":material/remove:", key="state_minus"):
                st.session_state.counter -= 1
        
        # 3. Read: Display the value
        st.metric("State Count", st.session_state.counter)
        st.caption("This works because we only set the counter to 0 if it doesn't exist.")

    # Footer
    st.divider()
    st.caption("Day 9: Understanding Session State | 30 Days of AI")
    """, language="python")

st.markdown("---")

# Working Demo
st.header("💬 Try It Yourself!")
st.caption("Click the + and - buttons in both columns to see the difference")

st.warning("**Instructions:** Try clicking the + and - buttons in both columns to see the difference.")

# Create two columns for side-by-side comparison
col1, col2 = st.columns(2)

# --- COLUMN 1: THE WRONG WAY ---
with col1:
    st.header(":material/cancel: Standard Variable")
    st.write("This resets on every click.")

    # This line runs every time you click ANY button on the page.
    # It effectively erases your progress immediately.
    count_wrong = 0
    
    # We use nested columns here to put the + and - buttons side-by-side
    subcol_left, subcol_right = st.columns(2)
    
    with subcol_left:
        # Note: We must give every button a unique 'key'
        if st.button(":material/add:", key="std_plus"):
            count_wrong += 1

    with subcol_right:
        if st.button(":material/remove:", key="std_minus"):
            count_wrong -= 1
    
    st.metric("Standard Count", count_wrong)
    st.caption("❌ It never gets past 1 or -1 because `count_wrong` resets to 0 before the math happens.")


# --- COLUMN 2: THE RIGHT WAY ---
with col2:
    st.header(":material/check_circle: Session State")
    st.write("This memory persists.")

    # 1. Initialization: Create the key only if it doesn't exist yet
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    
    # We use nested columns here as well
    subcol_left_2, subcol_right_2 = st.columns(2)

    with subcol_left_2:
        # 2. Modification: Update the dictionary value (Increment)
        if st.button(":material/add:", key="state_plus"):
            st.session_state.counter += 1

    with subcol_right_2:
        # 2. Modification: Update the dictionary value (Decrement)
        if st.button(":material/remove:", key="state_minus"):
            st.session_state.counter -= 1
    
    # 3. Read: Display the value
    st.metric("State Count", st.session_state.counter)
    st.caption("✅ This works because we only set the counter to 0 if it doesn't exist.")

st.markdown("---")

# Key Concepts
st.header("🔑 Key Concepts")

with st.expander("📚 Why Session State Matters"):
    st.markdown("""
    **The Problem:**
    - Streamlit reruns your entire script on every interaction
    - Regular variables get reset to their initial values
    - You lose data between interactions
    
    **The Solution:**
    - `st.session_state` is a dictionary-like object
    - Values persist across reruns for each user session
    - Perfect for storing conversation history, user inputs, or app state
    """)

with st.expander("🎯 Three-Step Pattern"):
    st.markdown("""
    1. **Initialize:** Check if key exists, create if not
       ```python
       if "my_var" not in st.session_state:
           st.session_state.my_var = initial_value
       ```
    
    2. **Modify:** Update the value when needed
       ```python
       if st.button("Update"):
           st.session_state.my_var = new_value
       ```
    
    3. **Read:** Access the value anywhere
       ```python
       st.write(st.session_state.my_var)
       ```
    """)

with st.expander("💡 Common Use Cases"):
    st.markdown("""
    - **Chat Applications:** Store message history
    - **Multi-Page Apps:** Share data between pages
    - **Form Wizards:** Remember previous steps
    - **API Results:** Cache expensive operations
    - **User Preferences:** Remember settings
    - **Authentication:** Store login status
    """)

st.markdown("---")

# Advanced Example
st.header("🚀 Advanced Example: Message History")

st.code("""
import streamlit as st

# Initialize message history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display all messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Add new message
if prompt := st.chat_input("Your message"):
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    st.rerun()

# Clear history
if st.button("Clear History"):
    st.session_state.messages = []
    st.rerun()
""", language="python")

st.info("💡 **Pro Tip:** Session state is perfect for building chatbots! You'll use this pattern extensively in the coming days.")

# Footer
st.divider()
st.caption("Day 9: Understanding Session State | 30 Days of AI")

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
