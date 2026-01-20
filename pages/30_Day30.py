import streamlit as st

st.set_page_config(page_title="Day 30 - Review & Next Steps", page_icon="🎓")

st.title("Day 30: Review and Next Steps")
st.markdown("---")

st.balloons()
st.snow()

st.header("🎉 Congratulations!")
st.markdown("""
You've completed the **Streamlit in 30 Days** challenge! 

You've transformed from a beginner to someone capable of building production-ready AI applications with Streamlit.
""")

st.header("📚 Your Learning Journey")

sections = {
    "Section 1: The Basics (Days 1-7)": {
        "Topics": [
            "Introduction to Streamlit",
            "Working with Text and Data",
            "LLM Integration Basics",
            "Streaming Responses",
            "Caching Strategies",
            "Session State Basics",
            "Practice Project 1: Simple LLM Chat"
        ],
        "Key Skills": "Streamlit fundamentals, API integration, state management"
    },
    "Section 2: Building Chatbots (Days 8-14)": {
        "Topics": [
            "Chat Interface Basics",
            "Message History Management",
            "Advanced Session State",
            "User Input Handling",
            "Conversation Context",
            "Chatbot Customization",
            "Practice Project 2: Full-Featured Chatbot"
        ],
        "Key Skills": "Chat interfaces, conversation management, user experience"
    },
    "Section 3: RAG Applications (Days 15-21)": {
        "Topics": [
            "Introduction to RAG",
            "Document Processing",
            "Vector Databases",
            "Embeddings",
            "Retrieval Strategies",
            "RAG Implementation",
            "Practice Project 3: Document Q&A System"
        ],
        "Key Skills": "RAG architecture, vector search, document analysis"
    },
    "Section 4: Advanced Features (Days 22-28)": {
        "Topics": [
            "Multimodal AI Integration",
            "Building AI Agents",
            "Agent Workflows",
            "Testing & Debugging",
            "Performance Optimization",
            "Deployment Strategies",
            "Practice Project 4: Production-Ready AI App"
        ],
        "Key Skills": "Advanced AI features, production deployment, optimization"
    },
    "Final Days (Days 29-30)": {
        "Topics": [
            "Capstone Project",
            "Course Review",
            "Future Learning Paths"
        ],
        "Key Skills": "End-to-end application development, best practices"
    }
}

for section, details in sections.items():
    with st.expander(f"**{section}**"):
        st.markdown("**Topics Covered:**")
        for topic in details["Topics"]:
            st.markdown(f"- {topic}")
        st.info(f"💡 **{details['Key Skills']}**")

st.header("🛠️ Skills You've Acquired")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Technical Skills")
    st.markdown("""
    - ✅ Streamlit development
    - ✅ LLM API integration
    - ✅ RAG systems
    - ✅ Vector databases
    - ✅ AI agents
    - ✅ Multimodal AI
    - ✅ Docker deployment
    - ✅ Performance optimization
    """)

with col2:
    st.subheader("Development Skills")
    st.markdown("""
    - ✅ State management
    - ✅ Error handling
    - ✅ Testing
    - ✅ Debugging
    - ✅ Code organization
    - ✅ Documentation
    - ✅ Version control
    - ✅ CI/CD basics
    """)

with col3:
    st.subheader("Soft Skills")
    st.markdown("""
    - ✅ Problem solving
    - ✅ System design
    - ✅ UX thinking
    - ✅ Performance mindset
    - ✅ Security awareness
    - ✅ Best practices
    - ✅ Production readiness
    - ✅ Continuous learning
    """)

st.header("🚀 Next Steps")

st.subheader("1. Continue Building")
st.markdown("""
**Practice Projects:**
- Build variations of the practice projects
- Create apps for your personal use
- Contribute to open-source Streamlit apps
- Participate in hackathons

**Ideas:**
- Personal finance tracker with AI insights
- Learning assistant for a topic you're studying
- Data visualization dashboard with AI narration
- Automation tool for repetitive tasks
""")

st.subheader("2. Deepen Your Knowledge")
st.markdown("""
**Advanced Topics:**
- Fine-tuning LLMs
- Custom embeddings
- Advanced agent architectures (AutoGPT, BabyAGI)
- LangGraph for complex workflows
- Prompt engineering mastery
- AI safety and alignment

**Related Technologies:**
- FastAPI for APIs
- PostgreSQL with pgvector
- Redis for caching
- Kubernetes for orchestration
""")

st.subheader("3. Join the Community")
st.markdown("""
**Get Involved:**
- [Streamlit Forum](https://discuss.streamlit.io) - Ask questions, share projects
- [Streamlit GitHub](https://github.com/streamlit/streamlit) - Contribute code
- [Discord Communities](https://discord.gg/streamlit) - Connect with developers
- [Twitter/X](https://twitter.com/streamlit) - Follow updates
- [LinkedIn](https://www.linkedin.com/company/streamlit) - Professional networking

**Share Your Work:**
- Post your projects on social media
- Write blog posts about your learning
- Create video tutorials
- Speak at meetups
""")

st.subheader("4. Career Opportunities")
st.markdown("""
**Roles You're Ready For:**
- AI Application Developer
- Full-Stack ML Engineer
- RAG System Engineer
- Chatbot Developer
- Data Science Tool Builder
- AI Product Developer

**Freelance Opportunities:**
- Build custom AI dashboards
- Create chatbots for businesses
- Develop RAG systems
- Consulting on AI implementation
""")

st.header("📖 Recommended Resources")

resources = {
    "Documentation": [
        "[Streamlit API Reference](https://docs.streamlit.io/library/api-reference)",
        "[LangChain Docs](https://python.langchain.com/docs/get_started/introduction)",
        "[OpenAI Cookbook](https://cookbook.openai.com/)",
        "[Vector Database Guides](https://www.pinecone.io/learn/)"
    ],
    "Courses": [
        "DeepLearning.AI - LangChain courses",
        "Andrew Ng's Machine Learning",
        "FastAPI tutorials",
        "Docker mastery courses"
    ],
    "Books": [
        "Building LLM Apps (by OpenAI)",
        "Designing Data-Intensive Applications",
        "The Pragmatic Programmer",
        "Clean Code by Robert Martin"
    ],
    "Blogs & Newsletters": [
        "Streamlit Blog",
        "Towards Data Science",
        "AI Alignment Newsletter",
        "The Batch by DeepLearning.AI"
    ]
}

for category, links in resources.items():
    with st.expander(f"**{category}**"):
        for link in links:
            st.markdown(f"- {link}")

st.header("💝 Final Tips")

st.markdown("""
### Keep Learning
- Technology evolves fast - stay curious
- Follow AI research and new models
- Experiment with new Streamlit features
- Learn from others' code

### Build in Public
- Share your progress and projects
- Document your learnings
- Help others who are learning
- Gather feedback early and often

### Focus on Value
- Build apps that solve real problems
- Prioritize user experience
- Optimize for performance
- Think about scale from day one

### Stay Connected
- Join developer communities
- Attend conferences and meetups
- Contribute to open source
- Network with other builders

### Never Stop Building
- The best way to learn is by doing
- Start small, iterate quickly
- Don't be afraid to fail
- Celebrate small wins
""")

st.header("🌟 Showcase Your Achievement")

st.markdown("""
**Share Your Success:**
- Post on LinkedIn with #StreamlitIn30Days
- Tweet your final project with @streamlit
- Add projects to your portfolio
- Update your resume with new skills

**Certificate Ideas:**
- Create a personal certificate
- Share your completion post
- Write a reflection blog post
- Record a project demo video
""")

st.code("""
🎓 Certificate of Completion
━━━━━━━━━━━━━━━━━━━━━━━━━

This certifies that [Your Name]
has successfully completed

STREAMLIT IN 30 DAYS

Mastering AI Application Development

Skills Acquired:
✅ Streamlit Development
✅ LLM Integration
✅ RAG Systems
✅ AI Agents
✅ Production Deployment

Date: [Today's Date]
━━━━━━━━━━━━━━━━━━━━━━━━━
""", language="text")

st.header("🎯 30-Day Challenge Complete!")

st.markdown("""
### You've:
- ✅ Completed 30 days of intensive learning
- ✅ Built 4 major practice projects
- ✅ Created a capstone project
- ✅ Learned production deployment
- ✅ Mastered Streamlit and AI integration

### Now Go Build Something Amazing! 🚀

Remember: **The journey doesn't end here.** This is just the beginning of your AI development career.

Keep building, keep learning, and most importantly, keep shipping! 🎉
""")

st.markdown("---")

# Final celebration
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🎉 Celebrate!"):
        st.balloons()
with col2:
    if st.button("❄️ More Celebration!"):
        st.snow()
with col3:
    if st.button("🎊 Even More!"):
        st.balloons()
        st.snow()

st.markdown("---")

st.success("""
### 🎓 You're now a Streamlit expert! 
Thank you for completing this journey. We can't wait to see what you build next!

**Stay in touch:** Share your projects, ask questions, and help others learn.

**Happy Building! 🚀**
""")

st.info("💡 **Tip:** Bookmark this course as a reference and revisit specific days when needed!")

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
