# 🎯 Streamlit in 30 Days

A comprehensive 30-day hands-on bootcamp to master Streamlit and AI application development. Learn to build production-ready AI apps from scratch!

[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📚 Course Structure

### Section 1: The Basics (Days 1-7)
**Your first LLM calls, streaming, and caching**
- **Day 1:** Introduction to Streamlit
- **Day 2:** Working with Text and Data
- **Day 3:** LLM Integration Basics
- **Day 4:** Streaming Responses
- **Day 5:** Caching Strategies
- **Day 6:** Session State Basics
- **Day 7:** Practice Project 1 - Simple LLM Chat

### Section 2: Building Chatbots (Days 8-14)
**Chat interfaces and session state**
- **Day 8:** Chat Interface Basics
- **Day 9:** Message History Management
- **Day 10:** Advanced Session State
- **Day 11:** User Input Handling
- **Day 12:** Conversation Context
- **Day 13:** Chatbot Customization
- **Day 14:** Practice Project 2 - Full-Featured Chatbot

### Section 3: RAG Applications (Days 15-21)
**Retrieval-Augmented Generation**
- **Day 15:** Introduction to RAG
- **Day 16:** Document Processing
- **Day 17:** Vector Databases
- **Day 18:** Embeddings
- **Day 19:** Retrieval Strategies
- **Day 20:** RAG Implementation
- **Day 21:** Practice Project 3 - Document Q&A System

### Section 4: Advanced Features (Days 22-28)
**Multimodal AI, Agents, and Deployment**
- **Day 22:** Multimodal AI Integration
- **Day 23:** Building AI Agents
- **Day 24:** Agent Workflows
- **Day 25:** Testing & Debugging
- **Day 26:** Performance Optimization
- **Day 27:** Deployment Strategies
- **Day 28:** Practice Project 4 - Production-Ready AI App

### Final Days (Days 29-30)
- **Day 29:** Final Project - Capstone
- **Day 30:** Review and Next Steps

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- Basic Python knowledge
- Understanding of APIs
- OpenAI API key (for LLM features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/mahanteshimath/Streamlit-in-30Days.git
   cd Streamlit-in-30Days
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API keys**
   ```bash
   # Copy the example secrets file
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   
   # Edit secrets.toml and add your API keys
   # IMPORTANT: Never commit secrets.toml to version control!
   ```

5. **Run the app**
   ```bash
   streamlit run Home.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:8501`
   - Start with Day 1 from the sidebar!

## 🛠️ Tech Stack

- **[Streamlit](https://streamlit.io)** - Web framework for ML/AI apps
- **[OpenAI](https://openai.com)** - LLM provider (GPT-3.5, GPT-4)
- **[LangChain](https://python.langchain.com)** - LLM application framework
- **[ChromaDB](https://www.trychroma.com)** - Vector database
- **[Pandas](https://pandas.pydata.org)** - Data manipulation
- **[tiktoken](https://github.com/openai/tiktoken)** - Token counting

## 📖 Learning Path

### Week 1: Foundations
- Master Streamlit basics
- Integrate LLMs
- Learn caching and state management

### Week 2: Chatbots
- Build chat interfaces
- Manage conversations
- Customize chatbot behavior

### Week 3: RAG Systems
- Implement document processing
- Work with vector databases
- Build semantic search

### Week 4: Production
- Add multimodal capabilities
- Create AI agents
- Optimize and deploy

## 💡 What You'll Build

### Practice Projects
1. **Simple LLM Chat** (Day 7) - Basic chatbot with streaming
2. **Full-Featured Chatbot** (Day 14) - Production chatbot with customization
3. **Document Q&A System** (Day 21) - RAG application with citations
4. **Production-Ready AI App** (Day 28) - Complete app with all features

### Final Project (Day 29)
Create your own AI application combining:
- Multi-page architecture
- LLM integration
- RAG or Agents
- Multimodal features
- Production deployment

## 📁 Project Structure

```
Streamlit-in-30Days/
├── Home.py                      # Landing page
├── pages/                       # Course days (auto-navigation)
│   ├── 01_Day1.py              # Day 1: Introduction
│   ├── 02_Day2.py              # Day 2: Text and Data
│   ├── ...
│   └── 30_Day30.py             # Day 30: Review
├── .streamlit/
│   ├── config.toml             # Streamlit configuration
│   └── secrets.toml.example    # API keys template
├── requirements.txt             # Python dependencies
├── LICENSE                      # MIT License
└── README.md                    # This file
```

## 🎓 Learning Outcomes

By the end of this course, you'll be able to:

- ✅ Build interactive Streamlit applications
- ✅ Integrate LLMs (OpenAI, Anthropic, etc.)
- ✅ Implement RAG systems with vector databases
- ✅ Create AI agents with tools
- ✅ Handle multimodal inputs (text, images, audio)
- ✅ Optimize app performance
- ✅ Deploy to production
- ✅ Follow best practices for AI app development

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Additional examples and tutorials
- Bug fixes and improvements
- Documentation enhancements
- New practice projects
- Translations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit Team** - For the amazing framework
- **OpenAI** - For LLM capabilities
- **LangChain Community** - For the excellent tools
- **All Contributors** - Thank you for your support!

## 📧 Contact

**Mahantesh Hiremath**
- GitHub: [@mahanteshimath](https://github.com/mahanteshimath)
- Repository: [Streamlit-in-30Days](https://github.com/mahanteshimath/Streamlit-in-30Days)

## 🌟 Support

If you find this course helpful:
- ⭐ Star this repository
- 🐛 Report issues
- 💡 Suggest improvements
- 📢 Share with others
- 🤝 Contribute

## 📚 Additional Resources

### Official Documentation
- [Streamlit Documentation](https://docs.streamlit.io)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [LangChain Documentation](https://python.langchain.com)

### Community
- [Streamlit Forum](https://discuss.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [LangChain Discord](https://discord.gg/langchain)

### Further Learning
- [DeepLearning.AI Courses](https://www.deeplearning.ai)
- [Streamlit Blog](https://blog.streamlit.io)
- [AI Alignment Newsletter](https://newsletter.alignmentforum.org)

---

**Ready to start?** Run `streamlit run Home.py` and begin your journey! 🚀

*Built with ❤️ for the AI developer community*
