import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_snowflake import ChatSnowflake
from pydantic import BaseModel, Field
from typing import Literal
import json

st.set_page_config(
    page_title="Day 30: Structured Output with Pydantic",
    page_icon=":material/schema:",
    layout="wide",
)

st.title(":material/schema: Day 30: Structured Output with Pydantic")
st.write(
    "Take LangChain to the next level with structured output using Pydantic. Get type-safe, validated objects instead of plain text that needs manual parsing."
)

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    try:
        # Works locally and on Streamlit Community Cloud
        from snowflake.snowpark import Session
        session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
    except Exception as e:
        session = None
        # st.warning(f"Snowflake session could not be established: {e}")

# Define output schema
class PlantRecommendation(BaseModel):
    name: str = Field(description="Plant name")
    water: Literal["Low", "Medium", "High"] = Field(description="Water requirement")
    light: Literal["Low", "Medium", "High"] = Field(description="Light requirement")
    difficulty: Literal["Beginner", "Intermediate", "Expert"] = Field(description="Care difficulty level")
    care_tips: str = Field(description="Brief care instructions")

# Create parser
parser = PydanticOutputParser(pydantic_object=PlantRecommendation)

# Create template with format instructions
template = ChatPromptTemplate.from_messages([
    ("system", "You are a plant expert. {format_instructions}"),
    ("human", "Recommend a plant for: {location}, {experience} experience, {space} space")
])

if session:
    # Create LLM and chain
    llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
    chain = template | llm | parser
else:
    chain = None

# Sidebar
with st.sidebar:
    st.header(":material/info: What is Structured Output?")
    st.info(
        "Structured output means getting LLM responses as typed Python objects instead of plain text strings.",
        icon=":material/info:",
    )

    st.divider()

    st.header(":material/package: Prerequisites")
    st.code("""pip install langchain-core langchain-snowflake pydantic snowflake-snowpark-python streamlit""", language="bash")
    
    st.markdown("**Required Packages:**")
    st.write("• `langchain-core` - ChatPromptTemplate, Parser")
    st.write("• `langchain-snowflake` - Cortex integration")
    st.write("• `pydantic` - Data validation")
    st.write("• `snowflake-snowpark-python` - Connection")
    st.write("• `streamlit` - Web framework")

    st.divider()

    st.header(":material/lightbulb: Why Structured Output?")
    st.success(
        "✅ Type-safe field access\n\n✅ IDE autocomplete works\n\n✅ Automatic validation\n\n✅ No manual JSON parsing\n\n✅ Guaranteed field existence",
        icon=":material/check_circle:",
    )

    st.divider()

    st.header(":material/link: Resources")
    st.page_link(
        "https://docs.pydantic.dev/latest/",
        label="Pydantic Documentation",
        icon=":material/book:",
    )
    st.page_link(
        "https://python.langchain.com/docs/how_to/output_parser_structured/",
        label="LangChain Output Parsers",
        icon=":material/code:",
    )

# Main Content
st.subheader(":material/code: Complete Working App")

with st.expander("🌱 View Full Code", expanded=True):
    st.code('''import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_snowflake import ChatSnowflake
from pydantic import BaseModel, Field
from typing import Literal

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

# Define output schema
class PlantRecommendation(BaseModel):
    name: str = Field(description="Plant name")
    water: Literal["Low", "Medium", "High"] = Field(description="Water requirement")
    light: Literal["Low", "Medium", "High"] = Field(description="Light requirement")
    difficulty: Literal["Beginner", "Intermediate", "Expert"] = Field(description="Care difficulty level")
    care_tips: str = Field(description="Brief care instructions")

# Create parser
parser = PydanticOutputParser(pydantic_object=PlantRecommendation)

# Create template with format instructions
template = ChatPromptTemplate.from_messages([
    ("system", "You are a plant expert. {format_instructions}"),
    ("human", "Recommend a plant for: {location}, {experience} experience, {space} space")
])

# Create LLM and chain
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
chain = template | llm | parser

# UI
st.title(":material/potted_plant: Plant Recommender")
location = st.text_input("Location:", "Apartment in Seattle")
experience = st.selectbox("Experience:", ["Beginner", "Intermediate", "Expert"])
space = st.text_input("Space:", "Small desk")

if st.button("Get Recommendation"):
    result = chain.invoke({
        "location": location,
        "experience": experience,
        "space": space,
        "format_instructions": parser.get_format_instructions()
    })

    st.subheader(f":material/eco: {result.name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Water", result.water)
    col2.metric("Light", result.light)
    col3.metric("Difficulty", result.difficulty)
    st.info(f"**Care:** {result.care_tips}")

    with st.expander(":material/description: See raw JSON response"):
        st.json(result.model_dump())

st.divider()
st.caption("Day 30: Structured Output with Pydantic | 30 Days of AI with Streamlit")
''', language="python")

st.markdown("---")

# Before/After Comparison
st.subheader(":material/auto_fix_high: The Problem vs The Solution")

prob_col1, prob_col2 = st.columns(2)

with prob_col1:
    st.markdown("### ❌ Without Structured Output")
    st.code('''response = "The plant is called Pothos. It needs low water..."
# How do you extract the plant name? 😰
# How do you get the water level? 🤔
# What if the format changes? 💔
''', language="python")
    
    st.error("""
    **Issues:**
    - Plain text response
    - Manual parsing required
    - No guarantees about format
    - Error-prone extraction
    """, icon=":material/cancel:")

with prob_col2:
    st.markdown("### ✅ With Structured Output")
    st.code('''response.name       # "Pothos"
response.water      # "Low"
response.light      # "Medium"
response.care_tips  # "Water when soil is dry..."
# Type-safe, IDE autocomplete! 🎉
''', language="python")
    
    st.success("""
    **Benefits:**
    - Typed Python objects
    - IDE autocomplete works
    - Guaranteed fields
    - Validated values
    """, icon=":material/check_circle:")

st.markdown("---")

# Step-by-Step Explanation
st.subheader(":material/school: How It Works: Step-by-Step")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    ":material/settings: 1. Imports",
    ":material/schema: 2. Schema",
    ":material/transform: 3. Parser",
    ":material/chat: 4. Template",
    ":material/link: 5. Chain",
    ":material/web: 6. UI",
    ":material/play_arrow: 7. Invoke"
])

with tab1:
    st.markdown("### :material/settings: Step 1: Imports and Connection")
    
    st.code('''import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_snowflake import ChatSnowflake
from pydantic import BaseModel, Field
from typing import Literal

# Connect to Snowflake
try:
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()
''', language="python")
    
    st.info("""
    **Key Imports:**
    - `PydanticOutputParser` - Converts LLM text to Pydantic objects
    - `BaseModel, Field` - Define typed data models
    - `Literal` - Constrain values to specific options
    - `ChatPromptTemplate` - Chat-style prompts
    """, icon=":material/info:")

with tab2:
    st.markdown("### :material/schema: Step 2: Defining the Output Schema")
    
    st.code('''# Define output schema
class PlantRecommendation(BaseModel):
    name: str = Field(description="Plant name")
    water: Literal["Low", "Medium", "High"] = Field(description="Water requirement")
    light: Literal["Low", "Medium", "High"] = Field(description="Light requirement")
    difficulty: Literal["Beginner", "Intermediate", "Expert"] = Field(description="Care difficulty level")
    care_tips: str = Field(description="Brief care instructions")
''', language="python")
    
    st.success("""
    **Pydantic Schema Benefits:**
    - `class PlantRecommendation(BaseModel)` - Defines expected response structure
    - `name: str` - Required string field
    - `Literal["Low", "Medium", "High"]` - Only these exact values allowed!
    - `Field(description="...")` - Helps LLM understand each field
    """, icon=":material/check_circle:")
    
    st.warning("""
    **🔑 Key Insight:** Using `Literal` types ensures the LLM can only return exact values. 
    If it tries "Very Low" or "low" (wrong case), Pydantic validation will fail!
    """, icon=":material/key:")

with tab3:
    st.markdown("### :material/transform: Step 3: Creating the Parser")
    
    st.code('''# Create parser
parser = PydanticOutputParser(pydantic_object=PlantRecommendation)
''', language="python")
    
    st.info("""
    **What the Parser Does:**
    1. ✅ Generates JSON schema instructions for the LLM
    2. ✅ Parses the LLM's JSON response
    3. ✅ Validates against your Pydantic schema
    4. ✅ Returns a type-safe Python object
    """, icon=":material/transform:")

with tab4:
    st.markdown("### :material/chat: Step 4: Creating the Prompt Template")
    
    st.code('''# Create template with format instructions
template = ChatPromptTemplate.from_messages([
    ("system", "You are a plant expert. {format_instructions}"),
    ("human", "Recommend a plant for: {location}, {experience} experience, {space} space")
])
''', language="python")
    
    st.success("""
    **Chat Template Structure:**
    - `ChatPromptTemplate.from_messages([...])` - Chat-style template
    - `{format_instructions}` - Parser injects JSON schema instructions
    - `("system", "...")` - Sets assistant persona + format rules
    - `("human", "...")` - User's request with variables
    """, icon=":material/chat:")

with tab5:
    st.markdown("### :material/link: Step 5: Building the Chain")
    
    st.code('''# Create LLM and chain
llm = ChatSnowflake(model="claude-3-5-sonnet", session=session)
chain = template | llm | parser
''', language="python")
    
    st.info("""
    **Three-Step Chain:**
    
    `template` → `llm` → `parser`
    
    1. **Template** - Formats prompt with variables + format instructions
    2. **LLM** - Generates JSON response
    3. **Parser** - Parses JSON into typed Pydantic object
    """, icon=":material/info:")

with tab6:
    st.markdown("### :material/web: Step 6: Building the Streamlit UI")
    
    st.code('''# UI
st.title(":material/potted_plant: Plant Recommender")
location = st.text_input("Location:", "Apartment in Seattle")
experience = st.selectbox("Experience:", ["Beginner", "Intermediate", "Expert"])
space = st.text_input("Space:", "Small desk")
''', language="python")
    
    st.write("**UI Components:**")
    st.write("• `st.title(...)` - App title with plant icon")
    st.write("• `st.text_input(...)` - Location input with default")
    st.write("• `st.selectbox(...)` - Experience level dropdown")
    st.write("• `st.text_input(...)` - Space description")

with tab7:
    st.markdown("### :material/play_arrow: Step 7: Invoking and Displaying")
    
    st.code('''if st.button("Get Recommendation"):
    result = chain.invoke({
        "location": location,
        "experience": experience,
        "space": space,
        "format_instructions": parser.get_format_instructions()
    })

    st.subheader(f":material/eco: {result.name}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Water", result.water)
    col2.metric("Light", result.light)
    col3.metric("Difficulty", result.difficulty)
    st.info(f"**Care:** {result.care_tips}")

    with st.expander(":material/description: See raw JSON response"):
        st.json(result.model_dump())
''', language="python")
    
    st.success("""
    **Type-Safe Access:**
    - `result.name`, `result.water` - Type-safe with IDE autocomplete!
    - No string key lookups, no KeyError exceptions
    - `parser.get_format_instructions()` - Generates JSON schema for LLM
    - `result.model_dump()` - Converts back to dict for JSON display
    """, icon=":material/auto_awesome:")

st.markdown("---")

# Comparison Section
st.subheader(":material/compare_arrows: Manual Parsing vs Structured Output")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### ❌ Before: Manual JSON Parsing")
    st.code('''response_raw = df.collect()[0][0]
response = json.loads(response_raw)  # Manual parsing
plant_name = response["name"]  # No type safety, could crash
water_level = response["water"]  # Hope it's spelled right!

# What if the key is missing? KeyError!
# What if the value is "very low"? String mismatch!
''', language="python")
    
    st.error("""
    **Problems:**
    - ❌ Manual JSON parsing
    - ❌ No type safety
    - ❌ No IDE autocomplete
    - ❌ Runtime errors if keys are wrong
    - ❌ No validation of values
    """, icon=":material/cancel:")

with col2:
    st.markdown("### ✅ After: Structured Output")
    st.code('''parser = PydanticOutputParser(pydantic_object=PlantRecommendation)
chain = template | llm | parser
result = chain.invoke({
    ..., 
    "format_instructions": parser.get_format_instructions()
})

plant_name = result.name  # Type-safe, IDE autocomplete!
water_level = result.water  # Guaranteed: "Low", "Medium", or "High"
''', language="python")
    
    st.success("""
    **Benefits:**
    - ✅ Automatic JSON parsing
    - ✅ Full type safety
    - ✅ IDE autocomplete works
    - ✅ Validation ensures correct values
    - ✅ Compile-time error checking
    """, icon=":material/check_circle:")

st.markdown("---")

# Key Pydantic Concepts
st.subheader(":material/key: Key Pydantic Concepts")

concept_tab1, concept_tab2, concept_tab3 = st.tabs([
    ":material/rule: Type Safety with Literal",
    ":material/description: Field Descriptions",
    ":material/settings: Format Instructions"
])

with concept_tab1:
    st.markdown("### :material/rule: Type Safety with Literal")
    st.write("Using `Literal` ensures the LLM can only return exact values:")
    
    st.code('''water: Literal["Low", "Medium", "High"]

# Valid: result.water = "Low"
# Valid: result.water = "Medium"
# Invalid: result.water = "Very Low"  # Pydantic will reject!
# Invalid: result.water = "low"       # Wrong case, rejected!
''', language="python")
    
    st.success("""
    **Why This Matters:**
    - Prevents typos and variations
    - Ensures consistent data format
    - Makes downstream processing reliable
    - No need to handle edge cases
    """, icon=":material/verified:")

with concept_tab2:
    st.markdown("### :material/description: Field Descriptions")
    st.write("Descriptions help the LLM understand what each field should contain:")
    
    st.code('''name: str = Field(description="Common name of the plant")
water: Literal["Low", "Medium", "High"] = Field(description="Water requirement level")
care_tips: str = Field(description="Brief care instructions in 1-2 sentences")
''', language="python")
    
    st.info("""
    **Best Practices:**
    - Be specific about what you want
    - Include format hints (e.g., "1-2 sentences")
    - Mention any constraints or requirements
    - The LLM reads these descriptions!
    """, icon=":material/lightbulb:")

with concept_tab3:
    st.markdown("### :material/settings: Format Instructions")
    st.write("The parser automatically generates instructions for the LLM:")
    
    st.code('''instructions = parser.get_format_instructions()
# Produces something like:
# "Return a JSON object with the following schema:
#  {'name': str, 'water': 'Low'|'Medium'|'High', ...}"
''', language="python")
    
    st.info("""
    **How It Works:**
    1. Parser reads your Pydantic schema
    2. Generates JSON schema instructions
    3. Instructions injected into prompt via `{format_instructions}`
    4. LLM follows the schema to format its response
    """, icon=":material/info:")

st.markdown("---")

# Try It Out Section
st.subheader(":material/science: Try It Out")

st.markdown("### 🌿 Plant Recommender App")

col1, col2 = st.columns(2)
with col1:
    location = st.text_input("Location:", "Apartment in Seattle")
    experience = st.selectbox("Experience:", ["Beginner", "Intermediate", "Expert"])
with col2:
    space = st.text_input("Space Description:", "Small desk near a window")

if st.button("Get Recommendation", type="primary"):
    if chain:
        with st.spinner("Analyzing plant compatibility..."):
            try:
                result = chain.invoke({
                    "location": location,
                    "experience": experience,
                    "space": space,
                    "format_instructions": parser.get_format_instructions()
                })

                st.subheader(f":material/eco: {result.name}")
                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Water", result.water)
                m_col2.metric("Light", result.light)
                m_col3.metric("Difficulty", result.difficulty)
                st.info(f"**Care Tips:** {result.care_tips}")

                with st.expander(":material/code: View Pydantic Object (JSON)"):
                    st.json(result.model_dump())
            except Exception as e:
                st.error(f"Error generating recommendation: {e}")
    else:
        st.error("Snowflake session is not active. Please check your credentials in `.streamlit/secrets.toml`.")

st.info("""
**Steps to test the app:**

1. **Enter your location** - e.g., "Apartment in Seattle", "Office in Austin"
2. **Select experience level** - Beginner, Intermediate, or Expert
3. **Describe your space** - e.g., "Small desk", "Sunny windowsill", "Dark corner"
4. **Click "Get Recommendation"** - See personalized plant suggestion
5. **Explore the results:**
   - View metrics for Water, Light, and Difficulty
   - Read care tips
   - Expand JSON to see structured data

Try different combinations and notice how the structured output makes everything clean and predictable!
""", icon=":material/lightbulb:")

st.markdown("---")

# Real-World Use Cases
st.subheader(":material/work: Real-World Use Cases")

usecase_col1, usecase_col2 = st.columns(2)

with usecase_col1:
    st.markdown("### :material/apartment: Perfect For")
    st.success("""
    **1. Form Generation**
    Extract structured data from documents
    
    **2. Data Classification**
    Categorize items with consistent labels
    
    **3. Multi-field Extraction**
    Pull multiple fields from unstructured text
    
    **4. API Responses**
    Generate consistent API response formats
    
    **5. Database Inserts**
    Create records with validated fields
    """)

with usecase_col2:
    st.markdown("### :material/code: Example Schemas")
    
    with st.expander("📧 Email Classification", expanded=False):
        st.code('''class EmailClassification(BaseModel):
    category: Literal["Sales", "Support", "Billing"]
    priority: Literal["Low", "Medium", "High"]
    requires_response: bool
    summary: str
''', language="python")
    
    with st.expander("🏠 Real Estate Listing", expanded=False):
        st.code('''class PropertyListing(BaseModel):
    address: str
    price: int
    bedrooms: int
    bathrooms: float
    property_type: Literal["House", "Condo", "Apartment"]
''', language="python")
    
    with st.expander("📦 Product Review", expanded=False):
        st.code('''class ProductReview(BaseModel):
    rating: Literal[1, 2, 3, 4, 5]
    sentiment: Literal["Positive", "Neutral", "Negative"]
    key_points: list[str]
    would_recommend: bool
''', language="python")

st.markdown("---")

# Advanced Tips
st.subheader(":material/tips_and_updates: Advanced Tips")

tip_col1, tip_col2 = st.columns(2)

with tip_col1:
    st.markdown("### :material/psychology: Pro Tips")
    st.info("""
    **1. Optional Fields**
    ```python
    from typing import Optional
    
    middle_name: Optional[str] = None
    ```
    
    **2. Lists of Objects**
    ```python
    recommendations: list[PlantRecommendation]
    ```
    
    **3. Nested Objects**
    ```python
    class CareSchedule(BaseModel):
        water_days: list[str]
        fertilize_frequency: str
    
    class Plant(BaseModel):
        name: str
        care: CareSchedule
    ```
    
    **4. Default Values**
    ```python
    color: str = Field(default="Green")
    ```
    """)

with tip_col2:
    st.markdown("### :material/error: Error Handling")
    st.warning("""
    **Handle Validation Errors:**
    
    ```python
    from pydantic import ValidationError
    
    try:
        result = chain.invoke({...})
    except ValidationError as e:
        st.error("LLM response didn't match schema!")
        st.json(e.errors())
    ```
    
    **Common Issues:**
    - LLM returns wrong field names
    - Values outside Literal constraints
    - Missing required fields
    - Wrong data types
    
    **Solutions:**
    - Add clearer Field descriptions
    - Use few-shot examples in prompt
    - Retry with modified prompt
    - Use temperature=0 for consistency
    """)

st.markdown("---")

# Resources
st.subheader(":material/link: Resources & Next Steps")

resource_col1, resource_col2 = st.columns(2)

with resource_col1:
    st.markdown("### :material/book: Documentation")
    st.page_link("https://docs.pydantic.dev/latest/", label="Pydantic Documentation", icon=":material/book:")
    st.page_link("https://python.langchain.com/docs/how_to/output_parser_structured/", label="LangChain Output Parsers", icon=":material/code:")
    st.page_link("https://python.langchain.com/docs/integrations/chat/snowflake/", label="LangChain Snowflake Integration", icon=":material/cloud:")
    st.page_link("https://docs.snowflake.com/en/user-guide/snowflake-cortex/overview", label="Snowflake Cortex AI", icon=":material/ac_unit:")

with resource_col2:
    st.markdown("### :material/celebration: Congratulations!")
    st.success("""
    **🎉 You've completed 30 Days of AI with Streamlit!**
    
    **What You've Learned:**
    • Basic LLM calls and streaming
    • Building chatbots with session state
    • RAG applications with Cortex Search
    • Multimodal AI and image generation
    • LangChain for cleaner code
    • Structured outputs with Pydantic
    
    **Keep Building:**
    • Combine techniques from multiple days
    • Build production applications
    • Share your creations!
    """, icon=":material/emoji_events:")

st.divider()
st.caption("Day 30: Structured Output with Pydantic | 30 Days of AI with Streamlit")
