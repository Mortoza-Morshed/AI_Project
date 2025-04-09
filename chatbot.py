import streamlit as st
import requests
import json
import os

st.set_page_config(page_title="AI Sustainable Living Coach", layout="wide")

st.title("🤖 AI Sustainable Living Coach 🥗")
st.markdown("**Created By-**   \n**Name:** Mortoza Mohammad Morshed  \n**Registration Number:** 12302326")

CHAT_FILE = "chat_history.json"

def load_chats():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            content = f.read().strip()  
            if content:  
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return {}  
            return {}  
    return {}  

def save_chats():
    with open(CHAT_FILE, "w") as f:
        json.dump(st.session_state.saved_chats, f)

if "messages" not in st.session_state:
    st.session_state.messages = []  
if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = load_chats()  
if "conversation_title" not in st.session_state:
    st.session_state.conversation_title = None  

with st.sidebar:
    st.header("📂 Chat History")
    for title in list(st.session_state.saved_chats.keys()):  
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(title, key=f"load_{title}"):  
                st.session_state.messages = st.session_state.saved_chats[title]
                st.session_state.conversation_title = title
        with col2:
            if st.button("🗑️", key=f"delete_{title}"):  
                del st.session_state.saved_chats[title]
                save_chats()
                if st.session_state.conversation_title == title:
                    st.session_state.messages = []
                    st.session_state.conversation_title = None
                st.rerun()  
    if st.button("➕ New Chat", key="new_chat"):
        st.session_state.messages = []
        st.session_state.conversation_title = None

if st.session_state.conversation_title:
    st.subheader(f"📜 Chat Session")
else:
    st.subheader("📜 Current Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me about nutrition, fitness, wellness, etc...")
if user_input:
    if st.session_state.conversation_title is None:
        st.session_state.conversation_title = user_input[:20] + "..."
        st.session_state.saved_chats[st.session_state.conversation_title] = []

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):  
        st.write(user_input)

    with st.chat_message("assistant"):
        thinking_placeholder = st.empty()  
        thinking_placeholder.write("Thinking...")  

    try:
        response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input})
        bot_response = response.json().get("response", "Sorry, I couldn't understand that.")
    except Exception as e:
        bot_response = f"Error: {str(e)}"

    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    thinking_placeholder.write(bot_response)  
    st.session_state.saved_chats[st.session_state.conversation_title] = st.session_state.messages.copy()
    save_chats()  
    st.rerun()  
