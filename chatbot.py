import streamlit as st
import requests
import json
import os

# Streamlit Page Configuration
st.set_page_config(page_title="AI Sustainable Living Coach", layout="wide")

# App Header
st.title("🤖 AI Sustainable Living Coach 🥗")
st.markdown("**Created By-**   \n**Name:** Mortoza Mohammad Morshed  \n**Registration Number:** 12302326")

# Constants
CHAT_FILE = "chat_history.json"

# Load chat history from JSON
def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            content = f.read().strip()  # Read and remove whitespace
            if content:  # Check if there’s actual content
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {}  # Invalid JSON, return empty dict
            return {}  # Empty file, return empty dict
    return {}  # File doesn’t exist, return empty dict

# Save chat history to JSON
def save_chats():
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.saved_chats, f)

# Initialize chat history and saved conversations
if "messages" not in st.session_state:
    st.session_state.messages = []  # Active chat session
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = load_chats()  # Load from JSON
if "conversation_title" not in st.session_state:
    st.session_state.conversation_title = None  # No title until user inputs

# Sidebar for saved conversations
with st.sidebar:
    st.header("📂 Chat History")
    for title in list(st.session_state.saved_chats.keys()):  # Use list to avoid runtime error
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(title, key=f"load_{title}"):  # Load chat
                st.session_state.messages = st.session_state.saved_chats[title]
                st.session_state.conversation_title = title
        with col2:
            if st.button("🗑️", key=f"delete_{title}"):  # Delete chat
                del st.session_state.saved_chats[title]
                save_chats()
                if st.session_state.conversation_title == title:
                    st.session_state.messages = []
                    st.session_state.conversation_title = None
                st.rerun()  # Refresh UI
    if st.button("➕ New Chat", key="new_chat"):
        st.session_state.messages = []
        st.session_state.conversation_title = None

# Display the active conversation title
if st.session_state.conversation_title:
    st.subheader(f"📜 Chat Session")
else:
    st.subheader("📜 Current Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input handling
user_input = st.chat_input("Ask me about nutrition, fitness, wellness, etc...")
if user_input:
    # Set conversation title based on first message if not set
    if st.session_state.conversation_title is None:
        st.session_state.conversation_title = user_input[:20] + "..."
        st.session_state.saved_chats[st.session_state.conversation_title] = []

    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):  
        st.write(user_input)

    # Show "Thinking..." while processing
    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()  # Create a placeholder
        thinking_placeholder.write("Thinking...")  # Display "Thinking..."

    # Send request to Flask API
    try:
        response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input})
        bot_response = response.json().get("response", "Sorry, I couldn't understand that.")
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    # Append AI response, update placeholder, and save
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    thinking_placeholder.write(bot_response)  # Replace "Thinking..." with response
    st.session_state.saved_chats[st.session_state.conversation_title] = st.session_state.messages.copy()
    save_chats()  # Save to JSON
    st.rerun()  # Force UI refresh to update sidebar
