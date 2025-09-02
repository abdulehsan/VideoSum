import streamlit as st
import groq
from utils import download_youtube_audio, transcribe_audio, summarize_text_with_llm

# ✅ Init Groq client
client = groq.Client(api_key=st.secrets["GROQ_KEY_1"])

# ✅ Session state setup
if "transcript" not in st.session_state:
    st.session_state["transcript"] = None
if "summary" not in st.session_state:
    st.session_state["summary"] = None
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.title("🎬 Video Summarizer with LLM")

tab2, tab3 = st.tabs(["YouTube Link", "Chat"])

# --- Tab 2: YouTube Video ---
with tab2:
    youtube_url = st.text_input("Enter YouTube link")
    if youtube_url and st.button("Summarize YouTube Video"):
        with st.spinner("Processing..."):
            audio_path = download_youtube_audio(youtube_url)
            transcript = transcribe_audio(audio_path, client)
            summary = summarize_text_with_llm(transcript, client)
            st.session_state["transcript"] = transcript
            st.session_state["summary"] = summary
            st.session_state["chat_history"] = []  # reset chat for new video

            # Add summary as first assistant message
            st.session_state["chat_history"].append({
                "role": "assistant",
                "content": "📌 **Summary:**\n\n" + summary
            })

            st.success("Done ✅")

# --- Tab 3: Chat ---
with tab3:
    if st.session_state["summary"]:
        st.subheader("💬 Chat about the Video")

        # Show existing chat history
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.chat_message("user").write(msg["content"])
            else:
                st.chat_message("assistant").write(msg["content"])

        # User input box
        query = st.chat_input("Enter your question...")
        if query:
            # Save user input
            st.session_state["chat_history"].append({"role": "user", "content": query})

            # ✅ Instead of backend request, answer directly with LLM
            answer = summarize_text_with_llm(
                f"You have given this Summary previously: {st.session_state['summary']}\nNow user gonna chat with you , it can be about the video content or anyother questions. Act like a general assistant that answers question if you have knowledge about it.\nUser question: {query}",
                client
            )

            # Save answer
            st.session_state["chat_history"].append({"role": "assistant", "content": answer})

            # Refresh UI
            st.rerun()
    else:
        st.warning("First summarize a video (YouTube tab) to start chatting.")
