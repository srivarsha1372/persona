import streamlit as st
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage


# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Load saved celebrities
def load_celebs():
    if not os.path.exists("celebs.json"):
        return {}
    with open("celebs.json", "r") as f:
        return json.load(f)

celebs = load_celebs()

# LangChain LLM (Groq)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="llama3-8b-8192"
)

# Streamlit App
st.title("🗣️ Chat with a Celebrity")

if not celebs:
    st.warning("No celebrities found. Please add one in `main.py` first.")
    st.stop()

selected_celeb = st.selectbox("Choose a Celebrity", list(celebs.keys()))
if st.button("🧹 Reset Chat"):
    if "chat_memory" in st.session_state and selected_celeb in st.session_state.chat_memory:
        st.session_state.chat_memory[selected_celeb] = []
    st.rerun()

persona_prompt = celebs[selected_celeb]

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}

if selected_celeb not in st.session_state.chat_memory:
    st.session_state.chat_memory[selected_celeb] = []

chat_history = st.session_state.chat_memory[selected_celeb]

st.chat_message("system").markdown(f"**You are now chatting with {selected_celeb}.**")

for msg in chat_history:
    st.chat_message("user").markdown(msg["user"])
    st.chat_message("assistant").markdown(msg["bot"])

user_input = st.chat_input(f"Talk to {selected_celeb}...")

if user_input:
    st.chat_message("user").markdown(user_input)

    messages = [
        SystemMessage(content=persona_prompt),
        *[message for msg in chat_history for message in [
            HumanMessage(content=msg["user"]),
            AIMessage(content=msg["bot"])
        ]],
        HumanMessage(content=user_input)
    ]

    response = llm(messages)
    bot_reply = response.content

    st.chat_message("assistant").markdown(bot_reply)

    chat_history.append({
        "user": user_input,
        "bot": bot_reply
    })

# Auto-scroll to bottom using JS
scroll_script = """
    <script>
        const chatArea = window.parent.document.querySelector('section.main');
        if (chatArea) {
            chatArea.scrollTo({ top: chatArea.scrollHeight, behavior: 'smooth' });
        }
    </script>
"""
st.components.v1.html(scroll_script, height=0)
