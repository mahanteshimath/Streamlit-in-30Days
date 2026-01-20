import streamlit as st

st.set_page_config(page_title="Day 23 - AI Agents", page_icon="2️⃣3️⃣")

st.title("Day 23: Building AI Agents")
st.markdown("**Section 4: Advanced Features**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Introduction to AI agents
- Agent frameworks (LangChain, CrewAI)
- Tool integration
- Agent decision making
""")

st.header("📖 Content")

st.subheader("What are AI Agents?")
st.markdown("""
AI agents are systems that can:
- **Perceive** their environment
- **Reason** about what to do
- **Act** using tools
- **Learn** from results

**Key Components:**
1. LLM as the "brain"
2. Tools for actions
3. Memory for context
4. Planning for complex tasks
""")

st.subheader("Simple Agent with LangChain")
st.code("""
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

# Define tools
def search_wikipedia(query):
    # Implement Wikipedia search
    return f"Wikipedia result for: {query}"

def calculate(expression):
    try:
        return eval(expression)
    except:
        return "Invalid expression"

tools = [
    Tool(
        name="Wikipedia",
        func=search_wikipedia,
        description="Search Wikipedia for information"
    ),
    Tool(
        name="Calculator",
        func=calculate,
        description="Perform calculations. Input should be a math expression."
    )
]

# Initialize agent
llm = ChatOpenAI(temperature=0)
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Run agent
response = agent.run("What is 25 * 4?")
st.write(response)
""", language="python")

st.subheader("ReAct Agent Pattern")
st.markdown("""
**ReAct** = Reasoning + Acting

The agent follows this loop:
1. **Thought:** What should I do?
2. **Action:** Use a tool
3. **Observation:** See the result
4. **Repeat** until done
""")

st.code("""
# Example ReAct trace
Thought: I need to find the population of France
Action: search_wikipedia("France population")
Observation: France has 67 million people
Thought: I have the answer
Final Answer: France has approximately 67 million people
""", language="text")

st.subheader("Custom Tools")
st.code("""
from langchain.tools import BaseTool

class CustomSearchTool(BaseTool):
    name = "custom_search"
    description = "Search for information in custom database"
    
    def _run(self, query: str) -> str:
        # Your custom logic
        results = search_database(query)
        return results
    
    async def _arun(self, query: str) -> str:
        # Async version
        raise NotImplementedError()

# Use custom tool
tools = [CustomSearchTool()]
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION)
""", language="python")

st.subheader("Agent with Memory")
st.code("""
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True
)

# Agent remembers previous conversations
agent.run("My name is John")
agent.run("What's my name?")  # Will remember "John"
""", language="python")

st.subheader("Streamlit Integration")
st.code("""
st.title("AI Agent Demo")

if 'agent_memory' not in st.session_state:
    st.session_state.agent_memory = ConversationBufferMemory()

query = st.text_input("Ask the agent:")

if st.button("Run"):
    with st.spinner("Agent thinking..."):
        # Initialize agent with memory
        agent = initialize_agent(
            tools,
            llm,
            memory=st.session_state.agent_memory,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION
        )
        
        # Run and display
        response = agent.run(query)
        st.write(response)
        
        # Show agent's thoughts
        with st.expander("See agent's reasoning"):
            st.write(agent.agent.llm_chain.memory.chat_memory)
""", language="python")

st.markdown("---")
st.info("✅ Build intelligent agents!")

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
