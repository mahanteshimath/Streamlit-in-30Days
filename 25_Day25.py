import streamlit as st
import json
from snowflake.snowpark.functions import ai_complete
import io
import time
import hashlib

st.set_page_config(page_title="Day 25 - Voice Interface", page_icon="2️⃣5️⃣")

# Connect to Snowflake
try:
    # Works in Streamlit in Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
except:
    # Works locally and on Streamlit Community Cloud
    from snowflake.snowpark import Session
    session = Session.builder.configs(st.secrets["connections"]["snowflake"]).create()

def call_llm(prompt_text: str) -> str:
    """Call Snowflake Cortex LLM."""
    df = session.range(1).select(
        ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
    )
    response_raw = df.collect()[0][0]
    response_json = json.loads(response_raw)
    if isinstance(response_json, dict):
        return response_json.get("choices", [{}])[0].get("messages", "")
    return str(response_json)

st.title(":material/record_voice_over: Day 25: Voice Interface")
st.write("Record voice messages and get AI-powered conversational responses using Snowflake's `AI_TRANSCRIBE` function.")

st.markdown("---")

# Quick Start Section
st.header("🚀 Quick Start - Default Connection")
with st.expander("View Code Snippet", expanded=False):
    st.code('''
    import streamlit as st
    import json
    from snowflake.snowpark.functions import ai_complete
    import io
    import time
    import hashlib
    
    # Connect to Snowflake
    from snowflake.snowpark.context import get_active_session
    session = get_active_session()
    
    def call_llm(prompt_text: str) -> str:
        """Call Snowflake Cortex LLM."""
        df = session.range(1).select(
            ai_complete(model="claude-3-5-sonnet", prompt=prompt_text).alias("response")
        )
        response_raw = df.collect()[0][0]
        response_json = json.loads(response_raw)
        if isinstance(response_json, dict):
            return response_json.get("choices", [{}])[0].get("messages", "")
        return str(response_json)
    
    # Initialize voice messages
    if "voice_messages" not in st.session_state:
        st.session_state.voice_messages = [{
            "role": "assistant",
            "content": "Hello! I'm your voice-enabled AI assistant."
        }]
    
    # Sidebar with audio input
    with st.sidebar:
        st.title("Voice-Enabled Assistant")
        st.subheader("Record Your Message")
        audio = st.audio_input("Click to record")
    
    # Display conversation
    for msg in st.session_state.voice_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Process audio when recorded
    if audio is not None:
        audio_bytes = audio.read()
        audio_hash = hashlib.md5(audio_bytes).hexdigest()
        
        if audio_hash != st.session_state.get("processed_audio_id"):
            st.session_state.processed_audio_id = audio_hash
            
            # Upload to stage and transcribe
            timestamp = int(time.time())
            filename = f"audio_{timestamp}.wav"
            
            session.file.put_stream(
                io.BytesIO(audio_bytes),
                f"@RAG_DB.RAG_SCHEMA.VOICE_AUDIO/{filename}",
                overwrite=True,
                auto_compress=False
            )
            
            # Transcribe audio
            result = session.sql(f"""
                SELECT SNOWFLAKE.CORTEX.AI_TRANSCRIBE(
                    TO_FILE('@RAG_DB.RAG_SCHEMA.VOICE_AUDIO', '{filename}')
                ) as transcript
            """).collect()
            
            transcript_data = json.loads(result[0]['TRANSCRIPT'])
            transcript = transcript_data.get("text", "")
            
            # Add user message
            st.session_state.voice_messages.append({
                "role": "user",
                "content": transcript
            })
            
            # Generate response
            conversation_context = "You are a friendly voice assistant.\\n\\n"
            for msg in st.session_state.voice_messages:
                role = "User" if msg["role"] == "user" else "Assistant"
                conversation_context += f"{role}: {msg['content']}\\n"
            
            response = call_llm(conversation_context)
            
            st.session_state.voice_messages.append({
                "role": "assistant",
                "content": response
            })
            
            st.rerun()
    ''', language="python")

st.markdown("---")

# Initialize state
if "voice_messages" not in st.session_state:
    st.session_state.voice_messages = []

# Ensure welcome message is always present
if len(st.session_state.voice_messages) == 0:
    st.session_state.voice_messages = [
        {
            "role": "assistant",
            "content": "Hello! :material/waving_hand: I'm your voice-enabled AI assistant. Click the microphone button in the sidebar to record a message, and I'll respond to you!"
        }
    ]

if "voice_database" not in st.session_state:
    st.session_state.voice_database = "RAG_DB"
    st.session_state.voice_schema = "RAG_SCHEMA"

if "processed_audio_id" not in st.session_state:
    st.session_state.processed_audio_id = None

# Get stage path from session state
database = st.session_state.voice_database
schema = st.session_state.voice_schema
full_stage_name = f"{database}.{schema}.VOICE_AUDIO"
stage_name = f"@{full_stage_name}"

# Sidebar
with st.sidebar:
    # Title and description at the top
    st.title(":material/record_voice_over: Voice-Enabled Assistant")
    st.write("Talk to your AI assistant using voice input!")
    
    # Audio Recording section
    st.subheader(":material/mic: Record Your Message")
    st.info(":material/info: **Known Issue**: The recorder may show an error message during recording, but it's harmless - the audio will still be transcribed successfully!", icon="ℹ️")
    audio = st.audio_input("Click to record")
    
    st.header(":material/settings: Settings")
    
    with st.expander("Database Configuration", expanded=False):
        database = st.text_input("Database", value=st.session_state.voice_database, key="db_input")
        schema = st.text_input("Schema", value=st.session_state.voice_schema, key="schema_input")
        
        # Update session state
        st.session_state.voice_database = database
        st.session_state.voice_schema = schema
        
        st.caption(f"Stage: `{database}.{schema}.VOICE_AUDIO`")
        st.caption(":material/edit_note: Stage uses server-side encryption (required for AI_TRANSCRIBE)")
        
        # Manual stage recreation button
        if st.button(":material/autorenew: Recreate Stage", help="Drop and recreate the stage with correct encryption"):
            try:
                full_stage = f"{database}.{schema}.VOICE_AUDIO"
                session.sql(f"DROP STAGE IF EXISTS {full_stage}").collect()
                session.sql(f"""
                CREATE STAGE {full_stage}
                    DIRECTORY = ( ENABLE = true )
                    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' )
                """).collect()
                st.success(f":material/check_circle: Stage recreated successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to recreate stage: {str(e)}")
    
    # Stage Status in expander
    with st.expander("Stage Status", expanded=False):
        # Get database and schema
        database = st.session_state.voice_database
        schema = st.session_state.voice_schema
        full_stage_name = f"{database}.{schema}.VOICE_AUDIO"
        
        # Create stage with proper configuration for AI_TRANSCRIBE (only if it doesn't exist)
        try:
            # Check if stage exists
            stage_info = session.sql(f"SHOW STAGES LIKE 'VOICE_AUDIO' IN SCHEMA {database}.{schema}").collect()
            
            if not stage_info:
                # Stage doesn't exist - create it
                st.info(f":material/construction: Creating audio stage with server-side encryption...")
                session.sql(f"""
                CREATE STAGE {full_stage_name}
                    DIRECTORY = ( ENABLE = true )
                    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' )
                """).collect()
                st.success(f":material/check_box: Audio stage created successfully!")
            else:
                # Stage exists - just confirm it's ready
                st.success(f":material/check_box: Audio stage ready (server-side encrypted)")
            
        except Exception as e:
            st.error(f":material/cancel: Could not verify/create stage")
            st.error(str(e))
            
            with st.expander(":material/build: Manual Fix"):
                st.code(f"""
DROP STAGE IF EXISTS {full_stage_name};
CREATE STAGE {full_stage_name}
    DIRECTORY = ( ENABLE = true )
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );
                """, language="sql")
                st.caption("Use the ':material/autorenew: Recreate Stage' button in Database Configuration if needed")
    
    if st.button(":material/delete: Clear Chat"):
        st.session_state.voice_messages = [
            {
                "role": "assistant",
                "content": "Hello! :material/waving_hand: I'm your voice-enabled AI assistant. Click the microphone button in the sidebar to record a message, and I'll respond to you!"
            }
        ]
        st.rerun()

# Display chat history FIRST (before processing)
st.subheader(":material/voice_chat: Conversation")
for msg in st.session_state.voice_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Create a container for processing status (appears below conversation)
status_container = st.container()

# Process audio when recorded
if audio is not None:
    # Read audio bytes and create hash to identify unique recordings
    audio_bytes = audio.read()
    audio_hash = hashlib.md5(audio_bytes).hexdigest()
    
    # Only process if this audio hasn't been processed yet
    if audio_hash != st.session_state.processed_audio_id:
        st.session_state.processed_audio_id = audio_hash
        
        with status_container:
            transcript = None
            with st.spinner(":material/mic: Transcribing audio..."):
                try:
                    # Generate unique filename with timestamp
                    timestamp = int(time.time())
                    filename = f"audio_{timestamp}.wav"
                    
                    # Wrap bytes in BytesIO for put_stream
                    audio_stream = io.BytesIO(audio_bytes)
                    full_stage_path = f"{stage_name}/{filename}"
                    
                    # Upload to Snowflake stage
                    session.file.put_stream(
                        audio_stream,
                        full_stage_path,
                        overwrite=True,
                        auto_compress=False
                    )
                    
                    # Sanitize filename for SQL
                    safe_file_name = filename.replace("'", "''")
                    
                    # Run AI_TRANSCRIBE
                    sql_query = f"""
                    SELECT SNOWFLAKE.CORTEX.AI_TRANSCRIBE(
                        TO_FILE('{stage_name}', '{safe_file_name}')
                    ) as transcript
                    """
                    
                    result_rows = session.sql(sql_query).collect()
                    
                    if result_rows:
                        # Parse JSON response
                        json_string = result_rows[0]['TRANSCRIPT']
                        transcript_data = json.loads(json_string)
                        transcript = transcript_data.get("text", "")
                        audio_duration = transcript_data.get("audio_duration", 0)
                        
                        if transcript:
                            # Add user message
                            st.session_state.voice_messages.append({
                                "role": "user",
                                "content": transcript
                            })
                        else:
                            st.warning(f":material/info: No speech detected in audio (duration: {audio_duration}s)")
                            st.info("""
                            **Possible reasons:**
                            - Audio was too quiet or silent
                            - No clear speech detected
                            - Audio quality too low
                            - Recording might be too short (minimum ~1 second recommended)
                            
                            **Tips:**
                            - Speak clearly and close to the microphone
                            - Ensure you're in a quiet environment
                            - Allow microphone permissions in your browser
                            - Try recording for at least 2-3 seconds
                            """)
                            with st.expander(":material/info: Transcription Response"):
                                st.json(transcript_data)
                    else:
                        st.error("Transcription query returned no results.")
                
                except Exception as e:
                    st.error(f"Error during transcription: {str(e)}")
                    
                    with st.expander(":material/edit_note: Troubleshooting"):
                        st.code(f"""
-- Stage must be created with proper configuration:
CREATE STAGE IF NOT EXISTS {full_stage_name}
    DIRECTORY = ( ENABLE = true )
    ENCRYPTION = ( TYPE = 'SNOWFLAKE_SSE' );

-- Expected transcription SQL:
SELECT SNOWFLAKE.CORTEX.AI_TRANSCRIBE(
    TO_FILE('{stage_name}', 'audio_xxxxx.wav')
) as transcript;
                        """, language="sql")
                        
                        st.markdown("""
                        **Common Issues:**
                        - **Client-Side Encryption Error**: Stage must use server-side encryption (`SNOWFLAKE_SSE`), not client-side
                        - **Directory Table**: Stage must have `DIRECTORY = ( ENABLE = true )`
                        - **Permissions**: Verify you can use `SNOWFLAKE.CORTEX.AI_TRANSCRIBE`
                        - **Availability**: Ensure `AI_TRANSCRIBE` is available in your Snowflake account/region
                        - **Audio Format**: Recorded audio is in WAV format by default
                        
                        **Reference:** [Snowflake AI_TRANSCRIBE Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/ai-audio)
                        """)
            
            # Generate assistant response if transcription was successful
            if transcript:
                with st.spinner(":material/smart_toy: Generating response..."):
                    # Build conversation history for context
                    conversation_context = "You are a friendly voice assistant. Keep responses short and conversational.\n\nConversation history:\n"
                    
                    # Add previous messages (excluding the welcome message if it's the only one)
                    history_messages = st.session_state.voice_messages[:-1] if len(st.session_state.voice_messages) > 1 else []
                    
                    # Skip welcome message in history
                    history_messages = [msg for msg in history_messages if not (msg["role"] == "assistant" and "Click the microphone button" in msg["content"])]
                    
                    for msg in history_messages:
                        role = "User" if msg["role"] == "user" else "Assistant"
                        conversation_context += f"{role}: {msg['content']}\n"
                    
                    # Add current user message
                    conversation_context += f"\nUser: {transcript}\n\nAssistant:"
                    
                    response = call_llm(conversation_context)
                    
                    st.session_state.voice_messages.append({
                        "role": "assistant",
                        "content": response
                    })
                
                # Clean up staged file
                try:
                    session.sql(f"REMOVE {stage_name}/{safe_file_name}").collect()
                except:
                    pass
                
                st.rerun()
else:
    # Reset processed audio ID when no audio is present
    st.session_state.processed_audio_id = None

st.divider()
st.caption("Day 25: Voice Interface | 30 Days of AI")

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
st.markdown(footer, unsafe_allow_html=True)
