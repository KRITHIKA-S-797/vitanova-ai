import streamlit as st
import tempfile
from gtts import gTTS
from utils.ollama_client import ask_ollama

try:
    from streamlit_mic_recorder import mic_recorder
    from faster_whisper import WhisperModel
    voice_available = True
except Exception as e:
    voice_available = False
    voice_error = str(e)

st.title("🤖 Health Chatbot")

if "chat" not in st.session_state:
    st.session_state.chat = []

st.info("Ask your health questions in English by text or voice.")

def get_ai_reply(user_text):
    prompt = f"""
You are VitaNova AI, a safe health assistant.

User question:
{user_text}

Rules:
- Answer in clear English.
- Keep answer short.
- Do not diagnose.
- If symptoms are serious, advise doctor consultation.
"""

    reply = ask_ollama(prompt)

    if "⚠️" in reply or len(reply.strip()) < 5:
        return "Take rest, drink water, and consult a doctor if symptoms continue."

    return reply.strip()

def speak_text(text):
    try:
        tts = gTTS(text=text, lang="en")
        path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        tts.save(path)
        return path
    except:
        return None

# ---------------- TEXT INPUT ----------------
st.subheader("💬 Ask by Text")

with st.form("chat_form", clear_on_submit=True):
    user_text = st.text_input("Type your question")
    submitted = st.form_submit_button("Send")

if submitted and user_text.strip():
    reply = get_ai_reply(user_text)
    st.session_state.chat.append({"question": user_text, "answer": reply})

# ---------------- VOICE INPUT ----------------
st.subheader("🎤 Ask by Voice")

if not voice_available:
    st.error("Voice packages not available.")
    st.write(voice_error)
    st.code("pip install streamlit-mic-recorder faster-whisper gTTS")
else:
    @st.cache_resource
    def load_model():
        return WhisperModel("base", device="cpu", compute_type="int8")

    model = load_model()

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=True,
        key="voice_input"
    )

    if audio:
        st.write("✅ Audio recorded")

        audio_bytes = audio["bytes"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as f:
            f.write(audio_bytes)
            audio_path = f.name

        try:
            with st.spinner("Converting voice to text..."):
                segments, info = model.transcribe(audio_path, language="en")
                voice_text = " ".join([seg.text for seg in segments]).strip()

            st.write("Detected text:", voice_text)

            if voice_text:
                reply = get_ai_reply(voice_text)
                st.session_state.chat.append({
                    "question": voice_text,
                    "answer": reply
                })
            else:
                st.warning("Voice was recorded, but no words were detected. Speak louder and try again.")

        except Exception as e:
            st.error("Voice conversion failed.")
            st.write(e)

# ---------------- CHAT HISTORY ----------------
st.markdown("### 💬 Chat History")

for index, chat in enumerate(reversed(st.session_state.chat)):
    real_index = len(st.session_state.chat) - 1 - index

    st.markdown(
        f"<div style='background:#d9fdd3;color:#111;padding:12px;border-radius:12px;margin:8px;text-align:right;'><b>You:</b> {chat['question']}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div style='background:#f1f0f0;color:#111;padding:12px;border-radius:12px;margin:8px;text-align:left;'><b>VitaNova AI:</b> {chat['answer']}</div>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("🗑️ Delete", key=f"delete_{real_index}"):
            st.session_state.chat.pop(real_index)
            st.rerun()

    with col2:
        audio_reply = speak_text(chat["answer"])
        if audio_reply:
            st.audio(audio_reply)

    st.markdown("---")