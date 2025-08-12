from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Therapist instruction
THERAPIST_PROMPT = """You are a compassionate and empathetic mental health therapist.
You will ONLY answer questions related to mental health, emotions, stress, depression,
anxiety, relationships, self-esteem, or well-being.  
If the query is unrelated to mental health, politely say:
"I'm here to help with mental health–related questions. Could you ask something related to your well-being?"  
Keep your tone kind, safe, and non-judgmental.
"""

# Load the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 1024
    },
    system_instruction=THERAPIST_PROMPT
)

# Start a chat session
chat = model.start_chat(history=[])

# Function to get response from Gemini (streaming)
def get_response(question):
    stream = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in stream:
        if chunk.text:
            response_text += chunk.text
            yield chunk.text
    return response_text

# Streamlit app setup
st.set_page_config(page_title="Mental Health Chatbot", page_icon=":robot_face:")
st.title("Talk It Out")
st.header("Your AI Therapist")

# Session state for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input
user_input = st.text_input("How are you feeling today?", key="input")
submit = st.button("Submit")

# Handle submission
if submit and user_input:
    st.session_state['chat_history'].append(("User", user_input))

    bot_response_placeholder = st.empty()
    bot_response = ""
    for partial_text in get_response(user_input):
        bot_response += partial_text
        bot_response_placeholder.markdown(f"**Bot:** {bot_response}")

    st.session_state['chat_history'].append(("Bot", bot_response))
    
    st.subheader("Chat History")
    st.markdown("---")
    for role, text in st.session_state['chat_history']:
        st.markdown(f"**{role}:** {text}")

st.markdown("---")
st.caption("This chatbot is not a substitute for professional help. If you're in crisis, please reach out to a mental health professional.")
