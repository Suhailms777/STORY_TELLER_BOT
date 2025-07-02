import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load API Key from .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-2.0-flash")

# Streamlit Page Config
st.set_page_config(
    page_title="📖 Story-Telling Chatbot",
    page_icon="🐉",
    layout="centered"
)

# Helper Function
def map_role(role):
    return "assistant" if role == "model" else role

# Start or restore session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    # Display default welcome message
    with st.chat_message("assistant"):
        st.markdown("👋 Hello! I'm your *Story-Telling Chatbot* 🧙‍♂.\n\nGive me a genre or a story prompt, and I'll spin a tale for you!")

# Title
st.title("📚 Story-Telling Chatbot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(map_role(message.role)):
        st.markdown(message.parts[0].text)

# Input box
user_input = st.chat_input("Enter a story prompt, idea, or genre...")

# If user types something
if user_input:
    st.chat_message("user").markdown(user_input)
    
    # Add system prompt for story generation
    story_prompt = f"You are a story writer AI. Generate a creative and engaging story based on this prompt: {user_input}"
    response = st.session_state.chat_session.send_message(story_prompt)

    # Show AI's story
    with st.chat_message("assistant"):
        st.markdown(response.text)