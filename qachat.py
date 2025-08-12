from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load environment variables from .env
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.2,
        "max_output_tokens": 1024
    }
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
            yield chunk.text  # stream partial text
    return response_text

# Streamlit app setup
st.set_page_config(page_title="Mental Heath Chatbot", page_icon=":robot_face:")
st.title("Talk It Out")
st.header("Mental Health Chatbot")

# Session state for storing chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User input
user_input = st.text_input("Ask a question:", key="input")
submit = st.button("Submit")

# Handle submission
if submit and user_input:
    st.session_state['chat_history'].append(("User", user_input))

    # Display bot response live
    bot_response_placeholder = st.empty()
    bot_response = ""
    for partial_text in get_response(user_input):
        bot_response += partial_text
        bot_response_placeholder.markdown(f"**Bot:** {bot_response}")

    # Append the final response to chat history
    st.session_state['chat_history'].append(("Bot", bot_response))
    
    # Display chat history
    if st.session_state['chat_history']:
        st.subheader("Chat History")
        st.markdown("---")
        for role, text in st.session_state['chat_history']:
            if role == "User":
                st.markdown(f"**{role}:** {text}")
            else:
                st.markdown(f"**{role}:** {text}")
    # Footer
    st.markdown("---")
    
