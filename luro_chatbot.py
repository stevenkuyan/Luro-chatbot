import streamlit as st
import openai
import os
import time

st.set_page_config(page_title="Luro Health Chat", page_icon="💬", layout="centered")

st.markdown("""
    <style>
    /* Full header banner */
    .header-banner {
        background-color: #003366; /* dark blue */
        padding: 2rem;
        text-align: center;
    }

    .header-banner h1 {
        color: white;
        font-size: 32px;
        margin-bottom: 0.5rem;
    }

    .header-banner p {
        color: white;
        font-size: 16px;
        margin-top: 0;
    }

    /* Input styling */
    .stChatInput {
        background-color: #f2f2f2 !important;
        border-radius: 8px !important;
    }

    /* Chat bubbles */
    .stChatMessage {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }

    /* Logo image */
    .logo {
        display: block;
        margin: 0 auto 1rem auto;
        width: 120px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-banner">
    <img src="https://cdn.prod.website-files.com/6838cbb99bbf0d11446556ed/68395d3a248ddb50f55b9a35_luro.svg" class="logo">
    <h1>💬 Luro Health Weight Management Agent - Production</h1>
    <p>Ask me anything related to weight management for patients in the Healthy Weight Program.</p>
</div>
""", unsafe_allow_html=True)
 
# Set your OpenAI key using Streamlit secrets
import os
openai.api_key = os.environ["OPENAI_API_KEY"]
assistant_id = os.environ["ASSISTANT_ID"]

# Setup session state
if "thread_id" not in st.session_state:
    thread = openai.beta.threads.create()
    st.session_state.thread_id = thread.id

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New user input
if prompt := st.chat_input("Type your message here..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    openai.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt,
    )

    run = openai.beta.threads.runs.create(
        thread_id=st.session_state.thread_id,
        assistant_id=ASSISTANT_ID,
    )

    # Wait for assistant
    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread_id, run_id=run.id
        )
        if run_status.status == "completed":
            break
        time.sleep(1)

    # Get the assistant reply
    messages = openai.beta.threads.messages.list(thread_id=st.session_state.thread_id)
    reply = messages.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
