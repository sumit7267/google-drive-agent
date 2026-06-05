import streamlit as st
import requests

st.set_page_config(page_title="Drive AI Agent", page_icon="$$", layout="centered")

st.title("Google Drive Assistant")
st.markdown("Search, filter, and discover files using natural language.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help with your Drive?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    try:
        with st.spinner("Agent is searching..."):
            response = requests.post(
                "https://google-drive-ai.onrender.com/chat", 
                json={"message": prompt},
                timeout=30 
            )
            if response.status_code == 200:
                data = response.json()
                if "error" in data:
                    answer = f"Backend Error: {data['error']}"
                else:
                    answer = data.get("response", "No response received.")
            else:
                answer = f"Error: Backend returned status code {response.status_code}"

    except Exception as e:
        answer = f"Connection Error: Make sure your FastAPI server is running! ({str(e)})"

    with st.chat_message("assistant"):
        st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})
