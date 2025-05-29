import time
import requests
import streamlit as st

# Constants
N8N_WEBHOOK_URL = (
    "https://shivangsingh26.app.n8n.cloud/webhook-test/slackAgent"
)  

# Page config
st.set_page_config(
    page_title="Slack AI Chatbot",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS styling
st.markdown(
    """
    <style>
        body {
            background-color: #f6f9fc;
        }
        .main {
            background: linear-gradient(to right, #e0eafc, #cfdef3);
            padding: 2rem;
            border-radius: 20px;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stTextInput>div>div>input {
            padding: 0.75rem;
            font-size: 1rem;
            border-radius: 12px;
            border: 1px solid #d4d4d4;
        }
        .stButton>button {
            background: linear-gradient(to right, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 0.6rem 1.2rem;
            font-size: 1rem;
            border-radius: 10px;
            transition: background 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background: linear-gradient(to right, #5a67d8, #6b46c1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and header
st.markdown(
    "<h1 style='text-align: center; color: #3b3b3b;'>🤖 Slack AI Chatbot</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; font-size: 18px;'>Ask me anything and I’ll get you an instant response from Slack!</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input prompt
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    st.session_state.chat_history.append(
        {"role": "user", "content": user_prompt}
    )

    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                response = requests.get(
                    N8N_WEBHOOK_URL,
                    params={"question": user_prompt},
                    timeout=10,
                )

                if response.status_code == 200:
                    bot_reply = response.json().get(
                        "response", "🤖 I couldn't find an answer."
                    )
                else:
                    bot_reply = f"❌ Error: Status code {response.status_code}"

            except Exception as e:
                bot_reply = f"⚠️ Something went wrong: `{str(e)}`"

            # Simulate typing effect
            placeholder = st.empty()
            full_text = ""
            for word in bot_reply.split():
                full_text += word + " "
                placeholder.markdown(full_text)
                time.sleep(0.05)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": bot_reply}
    )