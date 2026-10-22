import streamlit as st
import os
import time
from groq import Groq


st.set_page_config(page_title="AI Study Buddy", page_icon="🤖", layout="centered")


st.markdown("""
<style>
    .stChatMessage {
        animation: fadeIn 0.5s ease-in;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.title("⚙️ Settings")
    
    
    theme = st.toggle("🌙 Dark Mode", value=True)
    if not theme:
        st.markdown("<style>.stApp { background-color: #f0f2f6; color: #1f1f1f; }</style>", unsafe_allow_html=True)
    
    st.divider()
    
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()
        
    st.divider()
    st.caption("Made with ❤️ for Hacktoberfest")


st.title("🤖 Hi Buddy")
st.caption("Aapka personal AI assistant (Powered by Groq)")

api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("API Key nahi mili! Please Streamlit secrets check karein.")
    st.stop()

client = Groq(api_key=api_key)


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🧑‍🎓" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])


prompt = st.chat_input("Ask me anything...")

if prompt:
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    
    with st.chat_message("assistant", avatar="🤖"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": "You are a friendly AI Study Buddy. Keep answers short, use bullet points, and add emojis."}
                ] + st.session_state.messages,
                stream=True 
            )

            
            def stream_data():
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        yield chunk.choices[0].delta.content
                        time.sleep(0.03) # Speed of typing

            
            full_response = st.write_stream(stream_data)
            
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Error: {e}")


if len(st.session_state.messages) > 0:
    chat_text = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
    st.download_button(
        label="📥 Download Chat History",
        data=chat_text,
        file_name="study_buddy_chat.txt",
        mime="text/plain"
    )
