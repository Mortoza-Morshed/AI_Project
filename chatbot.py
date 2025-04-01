import streamlit as st
import requests

# Streamlit Page Configuration
st.set_page_config(page_title="AI Sustainable Living Coach", layout="wide")

# App Header
st.title("🤖 AI Sustainable Living Coach 🥗")
st.markdown("**Created By-**   \n**Name:** Mortoza Mohammad Morshed  \n**Registration Number:** 12302326")

# Initialize chat history and saved conversations
if "messages" not in st.session_state:
    st.session_state.messages = []  # Active chat session

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = {}  # Dictionary to store past conversations

if "conversation_title" not in st.session_state:
    st.session_state.conversation_title = None  # No title until user inputs

# Sidebar for saved conversations
with st.sidebar:
    st.header("📂 Chat History")

    # Show saved chats in sidebar
    for title in st.session_state.saved_chats.keys():
        if st.button(title, key=title):  # Clicking loads a saved conversation
            st.session_state.messages = st.session_state.saved_chats[title]
            st.session_state.conversation_title = title

    # Button to start a new chat
    if st.button("➕ New Chat", key="new_chat"):
        st.session_state.messages = []  # Clear messages
        st.session_state.conversation_title = None  # Reset title

# Display the active conversation title
if st.session_state.conversation_title:
    st.subheader(f"📜 {st.session_state.conversation_title}")
else:
    st.subheader("📜 Current Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])  # ✅ Displays messages correctly

# User input handling
user_input = st.chat_input("Ask me about nutrition, fitness, wellness, etc...")

if user_input:
    # Set conversation title based on first message if not set
    if st.session_state.conversation_title is None:
        st.session_state.conversation_title = user_input[:30] + "..."  # Trimmed first few words

        # Automatically save new conversation title
        st.session_state.saved_chats[st.session_state.conversation_title] = []

    # Append and display user message **before sending request**
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.saved_chats[st.session_state.conversation_title] = st.session_state.messages.copy()  # Save chat history

    with st.chat_message("user"):  
        st.write(user_input)  # ✅ Ensures the prompt appears immediately

    # Send Request to Flask API
    try:
        response = requests.post(
            "http://127.0.0.1:5000/chat", json={"message": user_input}
        )
        bot_response = response.json().get("response", "Sorry, I couldn't understand that.")
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    st.session_state.saved_chats[st.session_state.conversation_title] = st.session_state.messages.copy()  # Save updated chat

    # Display AI response
    with st.chat_message("assistant"):
        st.write(bot_response)  # ✅ Normal text format
