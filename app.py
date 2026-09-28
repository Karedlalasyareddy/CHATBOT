

import streamlit as st
import ollama
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
# Page configuration
st.set_page_config(
    page_title="ZenChat AI",
    page_icon="🤖",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
    color: #172033 !important;
}

/* Main text */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #12304a !important;
    margin-bottom: 5px;
}

.subtitle {
    color: #475569 !important;
    font-size: 17px;
    margin-bottom: 25px;
}

/* Normal Streamlit text */
p, span, label, div {
    color: #172033;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #14243e, #1b3655);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] button {
    color: #ffffff !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: #ffffff !important;
    color: #172033 !important;
    border: 1px solid #dbe3ec;
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
    margin-bottom: 12px;
}

/* Text inside chat messages */
[data-testid="stChatMessage"] p {
    color: #172033 !important;
}

/* Chat input */
[data-testid="stChatInput"] {
    border: 2px solid #0d9488;
    border-radius: 16px;
    background-color: #ffffff;
}

/* Chat input text */
[data-testid="stChatInput"] textarea {
    color: #172033 !important;
    background-color: #ffffff !important;
}

/* Camera section */
.camera-box {
    background-color: #ffffff;
    border: 1px solid #dbe3ec;
    border-radius: 16px;
    padding: 15px;
    margin-top: 15px;
}

/* Buttons */
button[kind="primary"] {
    background-color: #0d9488 !important;
    color: white !important;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("# 🤖 ZenChat")
    st.markdown("### Your AI Assistant 🌿")

    st.divider()

    if st.button("＋ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.camera_image = None
        st.rerun()

    st.markdown("### 💡 What I can do")

    st.markdown("""
    - Answer questions
    - Explain programming
    - Help with studies
    - Generate ideas
    - Write Python code
    - 📷 Capture images
    """)

    st.divider()

    st.caption("Powered by Ollama • Llama 3.2")


# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "camera_image" not in st.session_state:
    st.session_state.camera_image = None


# ---------------- MAIN HEADING ----------------
st.markdown(
    '<div class="main-title">👋 Hello! I am ZenChat</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your friendly AI assistant. Ask me anything!'
    '</div>',
    unsafe_allow_html=True
)


# ---------------- CAMERA OPTION ----------------
st.markdown("### 📷 Capture Data")

camera_image = st.camera_input(
    "Take a picture using your camera"
)

if camera_image is not None:

    st.session_state.camera_image = camera_image

    st.success("📸 Image captured successfully!")

    st.image(
        camera_image,
        caption="Captured Image",
        use_container_width=True
    )


# ---------------- DISPLAY CHAT HISTORY ----------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------- CHAT INPUT ----------------
prompt = st.chat_input("Type your message here...")


if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)


    # ---------------- AI RESPONSE ----------------
    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        try:

            with st.spinner("Thinking..."):

                response = ollama.chat(
                    model="llama3.2",
                    messages=[
                        {
                            "role": "system",
                            "content":
                            "You are ZenChat, a friendly and helpful "
                            "AI assistant. Give clear and simple answers."
                        },
                        *st.session_state.messages
                    ]
                )

            answer = response["message"]["content"]

            response_placeholder.markdown(answer)

            # Save AI response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            response_placeholder.error(
                "Could not connect to Ollama. "
                "Make sure Ollama is running and "
                "the llama3.2 model is installed."
            )

            st.caption(str(e))

