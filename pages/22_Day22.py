import streamlit as st

st.set_page_config(page_title="Day 22 - Multimodal AI", page_icon="2️⃣2️⃣")

st.title("Day 22: Multimodal AI Integration")
st.markdown("**Section 4: Advanced Features**")
st.markdown("---")

st.header("🎯 Learning Objectives")
st.markdown("""
- Work with images in LLM apps
- Audio processing
- Vision models (GPT-4 Vision)
- Multimodal prompts
""")

st.header("📖 Content")

st.subheader("Image Input")
st.code("""
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image:
    # Display image
    st.image(uploaded_image, caption="Uploaded Image")
    
    # Convert to base64 for API
    import base64
    image_bytes = uploaded_image.read()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
""", language="python")

st.subheader("GPT-4 Vision")
st.code("""
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=300
)

st.write(response.choices[0].message.content)
""", language="python")

st.subheader("Audio Processing")
st.code("""
audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])

if audio_file:
    st.audio(audio_file)
    
    # Transcribe with Whisper
    from openai import OpenAI
    client = OpenAI()
    
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    
    st.write("Transcript:", transcript.text)
""", language="python")

st.subheader("Text-to-Speech")
st.code("""
text = st.text_area("Enter text to convert to speech")

if st.button("Generate Speech"):
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    
    # Save and play
    response.stream_to_file("output.mp3")
    st.audio("output.mp3")
""", language="python")

st.subheader("Image Generation (DALL-E)")
st.code("""
prompt = st.text_input("Describe an image")

if st.button("Generate Image"):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    
    image_url = response.data[0].url
    st.image(image_url)
""", language="python")

st.markdown("---")
st.info("✅ Explore multimodal AI!")

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
