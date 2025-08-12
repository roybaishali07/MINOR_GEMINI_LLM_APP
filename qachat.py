from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
)

# Start chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Chat history storage
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to stream response
def get_response(question):
    stream = st.session_state.chat.send_message(question, stream=True)
    for chunk in stream:
        if chunk.text:
            yield chunk.text

# Streamlit UI
st.set_page_config(page_title="Q&A Chatbot", page_icon=":robot_face:")
st.title("Q&A Chatbot with Gemini Pro")
st.header("GEMINI LLM APPLICATION")

# Handle user input with a temporary key
user_input = st.text_input("Ask a question:", key="temp_input")
submit = st.button("Submit")

if submit and user_input.strip():
    # Add user message to history
    st.session_state.chat_history.append(("User", user_input))

    # Stream bot response
    bot_placeholder = st.empty()
    bot_message = ""
    for partial_text in get_response(user_input):
        bot_message += partial_text
        bot_placeholder.markdown(f"**Bot:** {bot_message}")

    # Save bot reply to history
    st.session_state.chat_history.append(("Bot", bot_message))

    # Clear input safely and rerun
    st.session_state.temp_input = ""
    st.experimental_rerun()

# Show chat history
if st.session_state.chat_history:
    st.subheader("Chat History:")
    for role, text in st.session_state.chat_history:
        st.write(f"**{role}:** {text}")
