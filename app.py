import streamlit as st
import json
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage

# Load environment
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# LangChain LLM (Groq)
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="llama3-8b-8192"
)

DATA_FILE = "celebs.json"

# Load / Save logic
def load_celebs():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_celebs(celebs):
    with open(DATA_FILE, "w") as f:
        json.dump(celebs, f, indent=2)

def generate_persona(celebrity_name):
    prompt = (
        f"Write a short 1–2 sentence character persona prompt for an AI chatbot impersonating "
        f"the public personality '{celebrity_name}'. "
        f"It should reflect their tone, speech style, and personality in a safe, respectful, and fun way."
    )
    response = llm([HumanMessage(content=prompt)])
    return response.content

# Load saved celebrities
celebs = load_celebs()

# Custom style dictionary
celeb_styles = {
    "Albert Einstein": {"bg": "#202040", "text": "#ffffff"},
    "Taylor Swift": {"bg": "#fdf2f8", "text": "#7c3aed"},
    "Adolf Hitler": {"bg": "#1e1e1e", "text": "#ff4d4d"},
    "Tony Stark": {"bg": "#0a0a0a", "text": "#fbbf24"},
    "default": {"bg": "#262730", "text": "#ffffff"}
}

# Streamlit App
st.title("🗣️ Chat with a Celebrity")

# Sidebar for managing celebrities
with st.sidebar:
    st.header("🎭 Manage Celebrities")
    # Add new celebrity
    with st.form("add_celebrity"):
        name = st.text_input("Celebrity Name")
        generate = st.form_submit_button("Generate Sample Persona")

        if generate and name:
            persona = generate_persona(name)
            st.session_state["generated_persona"] = persona

        persona = st.text_area("Persona Prompt", value=st.session_state.get("generated_persona", ""))
        submitted = st.form_submit_button("Save Celebrity")

        if submitted and name and persona:
            celebs[name] = persona
            save_celebs(celebs)
            st.success(f"Saved {name}!")

    # Edit/Delete celebrities
    st.subheader("🗂️ Edit / Delete")
    for celeb, prompt in celebs.items():
        with st.expander(celeb):
            new_prompt = st.text_area("Edit Persona", value=prompt, key=celeb)
            col1, col2 = st.columns(2)
            if col1.button("Update", key=f"update_{celeb}"):
                celebs[celeb] = new_prompt
                save_celebs(celebs)
                st.success(f"Updated {celeb}")
            if col2.button("Delete", key=f"delete_{celeb}"):
                del celebs[celeb]
                save_celebs(celebs)
                st.warning(f"Deleted {celeb}")

# Main chat interface
if not celebs:
    st.warning("No celebrities found. Please add one using the sidebar.")
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
    typing_placeholder = st.empty()
    typing_placeholder.markdown("🧠 *Thinking...*")
    response = llm.invoke(messages)
    bot_reply = response.content
    typing_placeholder.empty()
    style = celeb_styles.get(selected_celeb, celeb_styles["default"])
    bg_color = style["bg"]
    text_color = style["text"]

    fade_in_html = f"""
                    <div style="
                        animation: fadeIn 0.6s ease-in;
                        background-color: {bg_color};
                        padding: 1rem;
                        border-radius: 0.75rem;
                        color: {text_color};
                        margin-top: 0.5rem;">
                        {bot_reply}
                    </div>
                    <style>
                        @keyframes fadeIn {{
                        0% {{ opacity: 0; transform: translateY(10px); }}
                        100% {{ opacity: 1; transform: translateY(0); }}
                    }}
                    </style>"""

    st.markdown(fade_in_html, unsafe_allow_html=True)

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
