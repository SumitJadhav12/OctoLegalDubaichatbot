import streamlit as st
import requests
import time

st.set_page_config(page_title="OctoLegal UAE", page_icon="🛡️", layout="wide")

st.title("🛡️ UAE Labour Law Citation-Grounded Chatbot")
st.subheader("Focused on Federal Law No. 8 of 1980")

st.warning("⚠️ This system provides **legal information only**. It is **not professional legal advice**. Consult a qualified lawyer.")

# Sidebar
with st.sidebar:
    st.header("About")
    st.info("**Domain:** Employment Regulations\n**Corpus:** UAE Labour Law (1980)")
    st.caption("Hybrid Retrieval: BM25 + Vector Search")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about UAE Labour Law..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Retrieving from UAE Labour Law..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/chat", 
                    json={"question": prompt},
                    timeout=12
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(data.get("answer", "No response generated."))
                    
                    if data.get("citations"):
                        st.subheader("📌 Citations")
                        for i, cit in enumerate(data["citations"]):
                            with st.expander(f"Source {i+1} - {cit.get('section')}"):
                                st.write(f"**Document:** {cit.get('document')}")
                                st.write(f"**Page:** {cit.get('page')}")
                else:
                    st.error(f"Server Error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ **Backend is not running!**\n\nOpen a new terminal and run:\n`uvicorn main:app --reload --port 8000`")
            except requests.exceptions.Timeout:
                st.error("⏱️ **Request timed out.**\n\nThe backend is slow. Try these:\n1. Restart backend\n2. Ask simpler questions")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    # Safe append
    try:
        assistant_msg = data.get("answer", "Sorry, I encountered an error.") if 'data' in locals() else "Sorry, I encountered an error."
    except:
        assistant_msg = "Sorry, I encountered an error."
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})