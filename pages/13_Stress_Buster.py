import streamlit as st
from utils.ollama_client import ask_ollama

st.title("🫂 Stress Buster")
st.warning("This page gives emotional support only. If you feel unsafe, contact emergency help immediately.")

feeling = st.text_area(
    "Share your stress or problem here",
    placeholder="Example: I feel stressed about exams..."
)

def danger_detect(text):
    text = text.lower()
    danger_words = [
        "suicide", "kill myself", "die", "self harm",
        "hurt myself", "end my life", "overdose"
    ]
    return any(word in text for word in danger_words)

if st.button("Talk to VitaNova"):
    if not feeling.strip():
        st.warning("Please share how you feel.")
    else:
        if danger_detect(feeling):
            st.error("🚨 You may need urgent support.")
            st.markdown("""
Please do not stay alone.

- Call emergency help immediately
- Talk to a trusted family member or friend
- Contact a mental health professional

India Emergency Number: 112
""")
        else:
            prompt = f"""
You are VitaNova AI, a kind and supportive stress relief assistant.

User feeling:
{feeling}

Reply in simple English.

Rules:
- Be warm and comforting
- Do not judge
- Give 3 small practical steps
- Do not give medical diagnosis
- Keep it short and caring
"""

            with st.spinner("VitaNova is listening..."):
                reply = ask_ollama(prompt)

            if "⚠️" in reply or len(reply.strip()) < 5:
                reply = """
I understand that you are feeling stressed. Take a deep breath and give yourself a short break.
Try drinking water, relaxing for a few minutes, and talking to someone you trust.
You are not alone.
"""

            st.success("VitaNova AI Response")
            st.write(reply)