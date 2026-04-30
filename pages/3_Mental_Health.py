import streamlit as st
from datetime import datetime
from utils.db import get_connection
from utils.language import t, current_lang

st.title("🧠 " + t("mental_title"))
st.warning(t("warning"))

lang = current_lang()

mood = st.slider("Mood" if lang == "English" else ("மனநிலை" if lang == "Tamil" else "मूड"), 1, 10, 5)
stress = st.slider("Stress" if lang == "English" else ("மன அழுத்தம்" if lang == "Tamil" else "तनाव"), 1, 10, 5)
sleep = st.slider(t("sleep"), 1, 10, 5)
energy = st.slider("Energy" if lang == "English" else ("ஆற்றல்" if lang == "Tamil" else "ऊर्जा"), 1, 10, 5)
appetite = st.slider("Appetite" if lang == "English" else ("பசி" if lang == "Tamil" else "भूख"), 1, 10, 5)
social = st.slider("Social Interaction" if lang == "English" else ("சமூக தொடர்பு" if lang == "Tamil" else "सामाजिक संपर्क"), 1, 10, 5)

journal = st.text_area("How do you feel?" if lang == "English" else ("நீங்கள் எப்படி உணர்கிறீர்கள்?" if lang == "Tamil" else "आप कैसा महसूस कर रहे हैं?"))

if st.button(t("check")):
    score = mood + sleep + energy + appetite + social - stress

    if score >= 35:
        level = "Good"
        level_display = "Good" if lang == "English" else ("நல்லது" if lang == "Tamil" else "अच्छा")
    elif score >= 22:
        level = "Moderate"
        level_display = t("moderate")
    else:
        level = "Needs Attention"
        level_display = "Needs Attention" if lang == "English" else ("கவனம் தேவை" if lang == "Tamil" else "ध्यान देने की जरूरत")

    if lang == "Tamil":
        if level == "Good":
            advice = "உங்கள் மனநிலை நன்றாக உள்ளது. இதேபோல் தூக்கம், உணவு, உடற்பயிற்சியை தொடருங்கள்."
        elif level == "Moderate":
            advice = "சிறிது ஓய்வு எடுக்கவும். நம்பகமான ஒருவருடன் பேசவும்."
        else:
            advice = "உங்கள் மனநலத்திற்கு கவனம் தேவை. நம்பகமானவருடன் பேசவும் அல்லது மருத்துவரை அணுகவும்."

    elif lang == "Hindi":
        if level == "Good":
            advice = "आपका मानसिक स्वास्थ्य अच्छा है। अच्छी नींद, भोजन और व्यायाम जारी रखें।"
        elif level == "Moderate":
            advice = "थोड़ा आराम करें और किसी भरोसेमंद व्यक्ति से बात करें।"
        else:
            advice = "आपके मानसिक स्वास्थ्य पर ध्यान देने की जरूरत है। किसी भरोसेमंद व्यक्ति या डॉक्टर से बात करें।"

    else:
        if level == "Good":
            advice = "Your mental health looks good. Continue proper sleep, food, and exercise."
        elif level == "Moderate":
            advice = "Take some rest and talk to someone you trust."
        else:
            advice = "Your mental health needs attention. Talk to someone you trust or consult a professional."

    st.success(f"Score: {score}")
    st.warning(f"Level: {level_display}")
    st.info(advice)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mental_logs
        (date, mood, stress, sleep, energy, appetite, social, journal, score, level, ai_response)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        mood, stress, sleep, energy, appetite, social, journal, score, level, advice
    ))
    conn.commit()
    conn.close()