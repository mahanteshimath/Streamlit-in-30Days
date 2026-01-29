import streamlit as st

st.set_page_config(page_title="Day 8 - Meet the Chat Elements", page_icon="8️⃣", layout="wide")

st.title(":material/chat: Day 8: Meet the Chat Elements")
st.caption("30 Days of AI")
st.markdown("---")

# Week 2 Introduction
st.subheader("Welcome to Week 2!")
st.markdown(
    """
In Week 1, we built linear apps: Input → Process → Output.
Now, we start exploring chat elements to build a chatbot UI.

Today's goal: focus purely on the chat user interface — no memory and no APIs yet.
We'll render a visual chat conversation using Streamlit's chat components,
giving us the visual skeleton of a future chatbot.
    """
)

st.markdown("---")

# Quick Start - Visual Chat UI
st.header("🚀 Quick Start - Visual Chat UI")
with st.expander("View Code Snippet", expanded=False):
    st.code(
        """
import streamlit as st

st.title(":material/chat: Meet the Chat Elements")

# 1. Displaying Static Messages
with st.chat_message("user"):
    st.write("Hello! Can you explain what Streamlit is?")

with st.chat_message("assistant"):
    st.write("Streamlit is an open-source Python framework for building data apps.")
    st.bar_chart([10, 20, 30, 40]) # You can even put charts inside chat messages!

# 2. Chat Input
prompt = st.chat_input("Type a message here...")

# 3. Reacting to Input
if prompt:
    # Display the user's new message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display a mock assistant response
    with st.chat_message("assistant"):
        st.write(f"You just said:\n\n '{prompt}' \n\n(I don't have memory yet!)")

# Footer
st.divider()
st.caption("Day 8: Meet the Chat Elements | 30 Days of AI")
        """,
        language="python",
    )

st.markdown("---")

# Live Demo - Try It Yourself!
st.header("💬 Try It Yourself!")
st.caption("Focus on the chat UI — no memory yet")

# 1. Displaying Static Messages
with st.chat_message("user"):
    st.write("Hello! Can you explain what Streamlit is?")

with st.chat_message("assistant"):
    st.write("Streamlit is an open-source Python framework for building data apps.")
    st.bar_chart([10, 20, 30, 40])

# 2. Chat Input
prompt = st.chat_input("Type a message here...")

# 3. Reacting to Input
if prompt:
    # Display the user's new message
    with st.chat_message("user"):
        st.write(prompt)
    
    # Display a mock assistant response
    with st.chat_message("assistant"):
        st.write(f"You just said:\n\n '{prompt}' \n\n(I don't have memory yet!)")

# Footer
st.divider()
st.caption("Day 8: Meet the Chat Elements | 30 Days of AI")
