import streamlit as st

st.logo(
    image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg",
    link="https://www.linkedin.com/in/mahantesh-hiremath/",
    icon_image="https://upload.wikimedia.org/wikipedia/en/4/41/Flag_of_India.svg"
)

st.set_page_config(
    page_title="Streamlit in 30 Days",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Section 1: The Basics - Your first LLM calls, streaming, and caching
day1 = st.Page("pages/01_Day1.py", title="Day 1", icon="1️⃣", default=True)
day2 = st.Page("pages/02_Day2.py", title="Day 2", icon="2️⃣")
day3 = st.Page("pages/03_Day3.py", title="Day 3", icon="3️⃣")
day4 = st.Page("pages/04_Day4.py", title="Day 4", icon="4️⃣")
day5 = st.Page("pages/05_Day5.py", title="Day 5", icon="5️⃣")
day6 = st.Page("pages/06_Day6.py", title="Day 6", icon="6️⃣")
day7 = st.Page("pages/07_Day7.py", title="Day 7", icon="7️⃣")

# Section 2: Building Chatbots - Chat interfaces and session state
day8 = st.Page("pages/08_Day8.py", title="Day 8", icon="8️⃣")
day9 = st.Page("pages/09_Day9.py", title="Day 9", icon="9️⃣")
day10 = st.Page("pages/10_Day10.py", title="Day 10", icon="🔟")
day11 = st.Page("pages/11_Day11.py", title="Day 11", icon="💬")
day12 = st.Page("pages/12_Day12.py", title="Day 12", icon="💭")
day13 = st.Page("pages/13_Day13.py", title="Day 13", icon="🗨️")
day14 = st.Page("pages/14_Day14.py", title="Day 14", icon="✅")

# Section 3: RAG Applications - Retrieval-Augmented Generation
day15 = st.Page("pages/15_Day15.py", title="Day 15", icon="📚")
day16 = st.Page("pages/16_Day16.py", title="Day 16", icon="📄")
day17 = st.Page("pages/17_Day17.py", title="Day 17", icon="🗄️")
day18 = st.Page("pages/18_Day18.py", title="Day 18", icon="🔢")
day19 = st.Page("pages/19_Day19.py", title="Day 19", icon="🔍")
day20 = st.Page("pages/20_Day20.py", title="Day 20", icon="⚡")
day21 = st.Page("pages/21_Day21.py", title="Day 21", icon="✨")

# Section 4: Advanced Features - Multimodal AI, Agents, and Deployment
day22 = st.Page("pages/22_Day22.py", title="Day 22", icon="🎨")
day23 = st.Page("pages/23_Day23.py", title="Day 23", icon="🤖")
day24 = st.Page("pages/24_Day24.py", title="Day 24", icon="🔗")
day25 = st.Page("pages/25_Day25.py", title="Day 25", icon="🧪")
day26 = st.Page("pages/26_Day26.py", title="Day 26", icon="⚙️")
day27 = st.Page("pages/27_Day27.py", title="Day 27", icon="🚀")
day28 = st.Page("pages/28_Day28.py", title="Day 28", icon="🎯")
day29 = st.Page("pages/29_Day29.py", title="Day 29", icon="🔗")



# Navigation with sections
pg = st.navigation(
    {
        "The Basics - Your first LLM calls, streaming, and caching": [
            day1, day2, day3, day4, day5, day6, day7
        ],
        "Building Chatbots - Chat interfaces and session state": [
            day8, day9, day10, day11, day12, day13, day14
        ],
        "RAG Applications - Retrieval-Augmented Generation": [
            day15, day16, day17, day18, day19, day20, day21
        ],
        "Advanced Features - Multimodal AI, Agents, and Deployment": [
            day22, day23, day24, day25, day26, day27, day28, day29
        ]
    }
)

pg.run()
