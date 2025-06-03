import streamlit as st
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
import json

# Load your API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# Setup the Groq model (LLaMA 3)
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

# Streamlit UI
st.title("🎭 AI Celebrity Impersonator Setup")

celebs = load_celebs()

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
st.subheader("🗂️ Manage Celebrities")
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