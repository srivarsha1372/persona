# 🧠 AI Celebrity Impersonator Chat

Welcome to **AI Celebrity Chat**, an interactive and fun Streamlit app where you can chat with AI-powered personas of your favorite celebrities! Powered by the blazing-fast **Groq LLaMA3-8B model**, this app lets you create, manage, and talk to impersonated personalities in a safe, respectful, and entertaining environment.

---

## 🚀 Features

- 💬 **Chat with AI-powered Celebrities**  
  Select any celebrity and talk to their AI-generated persona. Each celebrity has a unique tone and personality.

- ✍️ **Add Your Own Celebrities**  
  Create new personas with auto-generated prompts using the LLM.

- 🧠 **Per-Celebrity Memory**  
  Chat history is preserved per celebrity session.

- 🎨 **Custom Chat Styles**  
  Chat bubbles are styled based on each celebrity’s theme with a smooth fade-in animation.

- 🔄 **Reset Chat**  
  Clear chat history for a clean restart.

- ⚙️ **Manage Celebrity Prompts**  
  Edit or delete saved personas easily from within the same app.

- ⏳ **Typing Indicator**  
  Simulated thinking animation while the AI generates a response.

---

---

## 📁 Project Structure

```
.
├── .env                      # Environment file with GROQ_API_KEY
├── .gitignore
├── .streamlit/
│   └── config.toml           # Streamlit deployment settings
├── app.py                    # Main application (chat + manage)
├── celebs.json               # JSON file storing all celebrity prompts
├── requirements.txt          # Python dependencies
└── README.md                 # You’re reading it
```

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – frontend + UI
- [LangChain](https://www.langchain.com/) – prompt management
- [Groq API](https://console.groq.com/) – for ultra-fast LLM responses
- [LLaMA3-8B-8192](https://groq.com/) – the AI model behind the personas

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/aipersona.git
cd aipersona
```

### 2. Create Environment Variables

Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## 🌐 Deployment on Streamlit Cloud

1. Push this project to a GitHub repository
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Link your GitHub repo
4. In the Streamlit Cloud settings, go to `Secrets` and add:

```env
GROQ_API_KEY=your_groq_api_key
```

5. Deploy and enjoy!

---

## 📦 requirements.txt

```txt
streamlit
python-dotenv
langchain
langchain-groq
```

Generate it with:

```bash
pip freeze > requirements.txt
```

---

## 📌 Example Celebrities

| Name            | Style             |
|-----------------|-------------------|
| Albert Einstein | Thoughtful, wise  |
| Tony Stark      | Witty, sarcastic  |
| Taylor Swift    | Friendly, warm    |

Feel free to add your own fictional or real-world personalities!

---

## 🧯 Content Safety

This application is meant for **entertainment and educational purposes only**. All generated personas are designed to avoid harm, impersonation, or misinformation. Please ensure all added prompts are appropriate and respectful.

---

## 📜 License

MIT License

---

## 🙌 Acknowledgments

- [Groq](https://groq.com) for blazing fast inference
- [LangChain](https://www.langchain.com/) for prompt orchestration
- [Streamlit](https://streamlit.io/) for an amazing app framework

---

## 💡 Future Ideas

- Voice chat integration
- Avatar images per celebrity
- Exportable chat transcripts
- Shared chatrooms with friends

---

Made with ❤️ using LLaMA + LangChain + Streamlit
