import streamlit as st

st.set_page_config(page_title="Day 27 - Deployment", page_icon="2️⃣7️⃣")

st.title("Day 27: Deployment Strategies")
st.markdown("**Section 4: Advanced Features**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Streamlit Cloud deployment
- Docker containerization
- Environment management
- Production best practices
""")

st.header("📖 Content")

st.subheader("Streamlit Cloud Deployment")
st.markdown("""
**Steps:**
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect repository
4. Configure secrets
5. Deploy!

**Requirements:**
- `requirements.txt` file
- `.streamlit/secrets.toml` (don't commit!)
- README.md (optional)
""")

st.code("""
# requirements.txt
streamlit>=1.28.0
openai>=1.0.0
langchain>=0.1.0
pandas>=2.0.0
""", language="text")

st.subheader("Managing Secrets")
st.code("""
# .streamlit/secrets.toml (local only)
OPENAI_API_KEY = "sk-..."
DATABASE_URL = "postgresql://..."

# In Streamlit Cloud:
# Add secrets via dashboard

# Access in code:
import streamlit as st
api_key = st.secrets["OPENAI_API_KEY"]
""", language="toml")

st.subheader("Docker Deployment")
st.code("""
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
""", language="dockerfile")

st.code("""
# docker-compose.yml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./data:/app/data
    restart: unless-stopped
""", language="yaml")

st.subheader("Environment Configuration")
st.code("""
# config.toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200

[browser]
gatherUsageStats = false

[runner]
fastReruns = true
""", language="toml")

st.subheader("Production Best Practices")
st.markdown("""
**Security:**
- ✅ Use secrets for API keys
- ✅ Validate all user inputs
- ✅ Implement rate limiting
- ✅ Enable HTTPS
- ✅ Set maxUploadSize

**Performance:**
- ✅ Use caching aggressively
- ✅ Implement pagination
- ✅ Optimize data loading
- ✅ Monitor resource usage

**Reliability:**
- ✅ Add error handling
- ✅ Implement logging
- ✅ Set up health checks
- ✅ Configure auto-restart

**Monitoring:**
- ✅ Track usage metrics
- ✅ Monitor errors
- ✅ Set up alerts
- ✅ Log important events
""")

st.subheader("Deployment Checklist")
checklist = {
    "Code": [
        "Remove debug code",
        "Add error handling",
        "Optimize performance",
        "Test edge cases"
    ],
    "Configuration": [
        "requirements.txt is complete",
        "Secrets configured",
        "Config.toml set",
        "Environment variables"
    ],
    "Security": [
        "API keys in secrets",
        "Input validation",
        "Rate limiting",
        "HTTPS enabled"
    ],
    "Documentation": [
        "README.md complete",
        "Usage instructions",
        "API documentation",
        "Troubleshooting guide"
    ]
}

for category, items in checklist.items():
    with st.expander(f"**{category}**"):
        for item in items:
            st.checkbox(item, key=f"deploy_{category}_{item}")

st.subheader("CI/CD Pipeline")
st.code("""
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Streamlit Cloud
        run: |
          # Trigger deployment
          curl -X POST ${{ secrets.DEPLOY_WEBHOOK }}
""", language="yaml")

st.subheader("Monitoring Setup")
st.code("""
# Simple analytics
import streamlit as st
from datetime import datetime

def log_usage(event_type, details=None):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'event': event_type,
        'details': details,
        'session_id': st.runtime.scriptrunner.get_script_run_ctx().session_id
    }
    
    # Log to file or database
    with open('usage.log', 'a') as f:
        f.write(json.dumps(log_entry) + '\\n')

# Track events
log_usage('page_view')
log_usage('button_click', {'button': 'generate'})
log_usage('query_submitted', {'query_length': len(query)})
""", language="python")

st.markdown("---")
st.info("✅ Deploy your apps!")

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
