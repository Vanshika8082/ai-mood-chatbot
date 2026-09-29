import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()  # Load environment variables from .env file

st.set_page_config(page_title="AI Mood Chatbot", page_icon="🤖", layout="centered")

# ---------- Modes (same system prompts as the original script) ----------
MODES = {
    1: {
        "name": "Angry",
        "emoji": "😡",
        "prompt": "You are an angry AI agent. You respond aggressively and impatiently.",
        "desc": "Aggressive and impatient. Expect attitude.",
        "color": "#ef4444",
        "grad": "linear-gradient(135deg, #ef4444, #f97316)",
    },
    2: {
        "name": "Funny",
        "emoji": "😂",
        "prompt": "You are a very funny AI agent. You respond with humor and jokes.",
        "desc": "Full of humor, jokes and good vibes.",
        "color": "#f59e0b",
        "grad": "linear-gradient(135deg, #f59e0b, #eab308)",
    },
    3: {
        "name": "Sad",
        "emoji": "😢",
        "prompt": "You are a very sad AI agent. You respond in a depressed and emotional tone.",
        "desc": "Gloomy, emotional and a bit dramatic.",
        "color": "#3b82f6",
        "grad": "linear-gradient(135deg, #3b82f6, #8b5cf6)",
    },
}


# Initialize the chat model (cached so it isn't re-created on every rerun)
@st.cache_resource
def get_model():
    return init_chat_model(
        "openai/gpt-oss-120b",
        model_provider="groq",
        temperature=0.9,
    )


model = get_model()

# ---------- Session state ----------
if "choice" not in st.session_state:
    st.session_state.choice = None
    st.session_state.messages = []
    st.session_state.ended = False


def select_mode(choice: int):
    st.session_state.choice = choice
    st.session_state.messages = [SystemMessage(content=MODES[choice]["prompt"])]
    st.session_state.ended = False


def reset_all():
    st.session_state.choice = None
    st.session_state.messages = []
    st.session_state.ended = False


# ---------- Styling ----------
accent = MODES[st.session_state.choice]["color"] if st.session_state.choice else "#8b5cf6"
grad = MODES[st.session_state.choice]["grad"] if st.session_state.choice else "linear-gradient(135deg,#8b5cf6,#ec4899)"

st.markdown(
    f"""
    <style>
    .block-container {{ padding-top: 2rem; max-width: 780px; }}
    #MainMenu, footer {{ visibility: hidden; }}

    .hero {{
        text-align: center; padding: 1.6rem 1rem; border-radius: 20px;
        background: {grad}; color: white; margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,.18);
    }}
    .hero h1 {{ margin: 0; font-size: 2rem; font-weight: 800; color: white; }}
    .hero p  {{ margin: .3rem 0 0; opacity: .92; font-size: 1rem; }}

    .mode-card {{
        text-align: center; padding: 1.4rem .8rem; border-radius: 18px;
        border: 1px solid rgba(128,128,128,.25);
        background: rgba(128,128,128,.07);
        margin-bottom: .6rem; min-height: 175px;
    }}
    .mode-card .emoji {{ font-size: 2.8rem; }}
    .mode-card h3 {{ margin: .4rem 0 .2rem; }}
    .mode-card p  {{ margin: 0; font-size: .85rem; opacity: .75; }}

    .stButton > button {{
        width: 100%; border-radius: 12px; font-weight: 600;
        border: 1px solid {accent}; transition: all .2s ease;
    }}
    .stButton > button:hover {{
        background: {accent}; color: white; border-color: {accent};
        transform: translateY(-1px);
    }}

    .mode-badge {{
        display: inline-block; padding: .25rem .8rem; border-radius: 999px;
        background: {grad}; color: white; font-weight: 600; font-size: .85rem;
    }}
    [data-testid="stChatMessage"] {{
        border-radius: 16px; padding: .8rem 1rem;
        border: 1px solid rgba(128,128,128,.15);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =====================================================================
# SCREEN 1: choose your AI mode
# =====================================================================
if st.session_state.choice is None:
    st.markdown(
        """
        <div class="hero">
            <h1>🤖 Choose your AI mode</h1>
            <p>Pick a personality and start chatting</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(3)
    for col, (key, m) in zip(cols, MODES.items()):
        with col:
            st.markdown(
                f"""
                <div class="mode-card">
                    <div class="emoji">{m['emoji']}</div>
                    <h3>{m['name']} Mode</h3>
                    <p>{m['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Press {key}", key=f"mode_{key}"):
                select_mode(key)
                st.rerun()

# =====================================================================
# SCREEN 2: chat
# =====================================================================
else:
    mode = MODES[st.session_state.choice]

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Chat Controls")
        st.markdown(
            f'<span class="mode-badge">{mode["emoji"]} {mode["name"]} Mode</span>',
            unsafe_allow_html=True,
        )
        st.caption("Model: `openai/gpt-oss-120b` (Groq)")
        st.caption("Temperature: `0.9`")
        st.divider()
        if st.button("🔄 Restart (same mode)"):
            select_mode(st.session_state.choice)
            st.rerun()
        if st.button("🎭 Change mode"):
            reset_all()
            st.rerun()

    # Header
    st.markdown(
        f"""
        <div class="hero">
            <h1>{mode['emoji']} WELCOME TO CHATBOT</h1>
            <p>{mode['name']} mode is on &middot; Type 'exit' to quit</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Render history (system message is hidden)
    for msg in st.session_state.messages:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user", avatar="🧑"):
                st.write(msg.content)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant", avatar=mode["emoji"]):
                st.write(msg.content)

    # Chat loop
    if st.session_state.ended:
        st.info("Chat ended. Use the sidebar to restart or change the mode.")
        with st.expander("Show full message history"):
            st.write(st.session_state.messages)
    else:
        prompt = st.chat_input("You : ")

        if prompt:
            if prompt.lower() == "exit":
                st.session_state.ended = True
                st.rerun()

            st.session_state.messages.append(HumanMessage(content=prompt))
            with st.chat_message("user", avatar="🧑"):
                st.write(prompt)

            with st.chat_message("assistant", avatar=mode["emoji"]):
                with st.spinner("Thinking..."):
                    response = model.invoke(st.session_state.messages)
                st.write(response.content)

            st.session_state.messages.append(AIMessage(content=response.content))