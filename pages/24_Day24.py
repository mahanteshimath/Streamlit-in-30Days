import streamlit as st

st.set_page_config(page_title="Day 24 - Agent Workflows", page_icon="2️⃣4️⃣")

st.title("Day 24: Agent Workflows")
st.markdown("**Section 4: Advanced Features**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Multi-step workflows
- Agent orchestration
- Error handling in agents
- Monitoring agent actions
""")

st.header("📖 Content")

st.subheader("Sequential Workflows")
st.code("""
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts import PromptTemplate

# Step 1: Analyze
analyze_prompt = PromptTemplate(
    input_variables=["text"],
    template="Analyze this text: {text}"
)
analyze_chain = LLMChain(llm=llm, prompt=analyze_prompt, output_key="analysis")

# Step 2: Summarize
summarize_prompt = PromptTemplate(
    input_variables=["analysis"],
    template="Summarize: {analysis}"
)
summarize_chain = LLMChain(llm=llm, prompt=summarize_prompt, output_key="summary")

# Combine
workflow = SequentialChain(
    chains=[analyze_chain, summarize_chain],
    input_variables=["text"],
    output_variables=["analysis", "summary"]
)

result = workflow({"text": "Your input text"})
""", language="python")

st.subheader("Conditional Workflows")
st.code("""
def conditional_workflow(user_input):
    # Step 1: Classify intent
    intent = classify_intent(user_input)
    
    if intent == "question":
        # Route to Q&A agent
        response = qa_agent.run(user_input)
    elif intent == "task":
        # Route to task agent
        response = task_agent.run(user_input)
    elif intent == "creative":
        # Route to creative agent
        response = creative_agent.run(user_input)
    else:
        response = "I'm not sure how to help with that."
    
    return response
""", language="python")

st.subheader("Parallel Agent Execution")
st.code("""
import concurrent.futures

def run_agents_parallel(query):
    agents = [agent1, agent2, agent3]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit all agents
        futures = [
            executor.submit(agent.run, query)
            for agent in agents
        ]
        
        # Collect results
        results = [f.result() for f in futures]
    
    # Aggregate results
    final_answer = aggregate_responses(results)
    return final_answer
""", language="python")

st.subheader("Error Handling")
st.code("""
from langchain.callbacks import StdOutCallbackHandler

class ErrorHandlingCallback(StdOutCallbackHandler):
    def on_tool_error(self, error, **kwargs):
        st.error(f"Tool error: {error}")
    
    def on_chain_error(self, error, **kwargs):
        st.error(f"Chain error: {error}")

def safe_agent_run(agent, query, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = agent.run(
                query,
                callbacks=[ErrorHandlingCallback()]
            )
            return result
        except Exception as e:
            st.warning(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return f"Failed after {max_retries} attempts"
""", language="python")

st.subheader("Monitoring Agent Actions")
st.code("""
class MonitoringCallback:
    def __init__(self):
        self.steps = []
    
    def on_tool_start(self, tool, input_str, **kwargs):
        self.steps.append({
            "action": "tool_start",
            "tool": tool.name if hasattr(tool, 'name') else str(tool),
            "input": input_str
        })
    
    def on_tool_end(self, output, **kwargs):
        self.steps.append({
            "action": "tool_end",
            "output": str(output)
        })

# Use in Streamlit
monitor = MonitoringCallback()
result = agent.run(query, callbacks=[monitor])

# Display steps
with st.expander("Agent Steps"):
    for step in monitor.steps:
        st.json(step)
""", language="python")

st.subheader("Complex Workflow Example")
st.code("""
def research_workflow(topic):
    progress = st.progress(0)
    status = st.empty()
    
    # Step 1: Research
    status.text("Step 1/4: Researching...")
    research = research_agent.run(f"Research: {topic}")
    progress.progress(25)
    
    # Step 2: Analyze
    status.text("Step 2/4: Analyzing...")
    analysis = analysis_agent.run(f"Analyze: {research}")
    progress.progress(50)
    
    # Step 3: Synthesize
    status.text("Step 3/4: Synthesizing...")
    synthesis = synthesis_agent.run(f"Synthesize: {analysis}")
    progress.progress(75)
    
    # Step 4: Format
    status.text("Step 4/4: Formatting...")
    final = format_agent.run(f"Format: {synthesis}")
    progress.progress(100)
    
    status.text("Complete!")
    return final

# Use it
if st.button("Start Research"):
    result = research_workflow(user_topic)
    st.write(result)
""", language="python")

st.subheader("Agent State Management")
st.code("""
class AgentState:
    def __init__(self):
        self.memory = []
        self.context = {}
        self.tools_used = []
    
    def add_memory(self, item):
        self.memory.append(item)
    
    def update_context(self, key, value):
        self.context[key] = value
    
    def log_tool_use(self, tool_name):
        self.tools_used.append(tool_name)

# Initialize in session state
if 'agent_state' not in st.session_state:
    st.session_state.agent_state = AgentState()

# Display state
with st.sidebar:
    st.subheader("Agent State")
    st.json(st.session_state.agent_state.__dict__)
""", language="python")

st.markdown("---")
st.info("✅ Master agent workflows!")

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
