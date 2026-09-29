# 🤖 AI Mood Chatbot

An interactive AI chatbot built with **Python, Streamlit, LangChain, and Groq**. Choose an AI personality and enjoy a conversation with a chatbot that responds according to its selected mood.

## ✨ Features

* 😡 **Angry Mode** — Aggressive and impatient responses.
* 😂 **Funny Mode** — Humorous responses and jokes.
* 😢 **Sad Mode** — Emotional and gloomy responses.
* 💬 Interactive chat interface with message history.
* 🎨 Custom UI with gradients, colors, and emoji avatars.
* 🔄 Restart conversations or switch between AI personalities.
* ⚡ Powered by Groq and LangChain.

## 🛠️ Technologies Used

* Python
* Streamlit
* LangChain
* Groq API
* python-dotenv

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-mood-chatbot.git
cd ai-mood-chatbot
```

### 2. Install dependencies

```bash
pip install streamlit python-dotenv langchain langchain-core langchain-groq
```

### 3. Configure your API key

Create a `.env` file in the project directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from [Groq Console](https://console.groq.com/).

**Important:** Never upload your `.env` file or expose your API key publicly.

### 4. Run the application

```bash
streamlit run app.py
```

Replace `app.py` with your Python filename if necessary.

## 🎮 How to Use

1. Launch the application.
2. Choose Angry, Funny, or Sad mode.
3. Start chatting with your selected AI personality.
4. Type `exit` to end the conversation.
5. Restart the chat or switch modes using the sidebar controls.

## 🤖 Model

* **Model:** `openai/gpt-oss-120b`
* **Provider:** Groq
* **Temperature:** `0.9`

## 📁 Project Structure

```text
ai-mood-chatbot/
├── app.py
├── README.md
└── .gitignore
```

Create a `.env` file locally for your API key. Keep it out of version control.
resting, consider giving the repository a star!
