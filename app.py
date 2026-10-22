import streamlit as st
import os
from groq import Groq


api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("API Key nahi mili! Please settings check karein.")
else:
    client = Groq(api_key=api_key)
    st.set_page_config(page_title="AI Study Buddy", page_icon="🤖")
    st.title("🤖 AI Study Buddy")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask me anything...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Soch raha hoon..."):
            try:
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "system", "content": "You are a friendly AI Study Buddy. Talk like a human and use emojis 😊."}] + st.session_state.messages
                )
                answer = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
                with st.chat_message("assistant"):
                    st.markdown(answer)
            except Exception as e:
                st.error(f"Error aya hai: {e}")
