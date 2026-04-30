import streamlit as st
from datetime import datetime
from utils.db import get_connection
from utils.ollama_client import ask_ollama
from utils.language import t, current_lang

st.title("🩺 " + t("disease_title"))
st.warning(t("warning"))

age = st.number_input(t("age"), 1, 100, 25)
height = st.number_input(t("height") + " (cm)", 50.0, 250.0, 160.0)
weight = st.number_input(t("weight") + " (kg)", 10.0, 300.0, 60.0)

exercise_display = st.selectbox(t("exercise"), [t("low"), t("moderate"), t("high")])
exercise_map = {t("low"): "Low", t("moderate"): "Moderate", t("high"): "High"}
exercise = exercise_map[exercise_display]

sleep = st.number_input(t("sleep"), 0.0, 15.0, 7.0)

yes_no = [t("no"), t("yes")]
yes_no_map = {t("no"): "No", t("yes"): "Yes"}

smoking = yes_no_map[st.selectbox(t("smoking"), yes_no)]
alcohol = yes_no_map[st.selectbox(t("alcohol"), yes_no)]
sugar = yes_no_map[st.selectbox(t("sugar"), yes_no)]
family_history = yes_no_map[st.selectbox(t("family"), yes_no)]
bp = yes_no_map[st.selectbox(t("bp"), yes_no)]

def factor_display(factor):
    lang = current_lang()

    tamil = {
        "Higher age": "அதிக வயது",
        "High BMI": "அதிக உடல் நிறை குறியீடு",
        "Low exercise": "குறைந்த உடற்பயிற்சி",
        "Poor sleep": "குறைந்த தூக்கம்",
        "Smoking": "புகைபிடித்தல்",
        "Alcohol use": "மது அருந்துதல்",
        "High sugar intake": "அதிக சர்க்கரை உட்கொள்ளல்",
        "Family history": "குடும்ப வரலாறு",
        "High blood pressure": "உயர் இரத்த அழுத்தம்",
    }

    hindi = {
        "Higher age": "अधिक उम्र",
        "High BMI": "अधिक BMI",
        "Low exercise": "कम व्यायाम",
        "Poor sleep": "कम नींद",
        "Smoking": "धूम्रपान",
        "Alcohol use": "शराब सेवन",
        "High sugar intake": "अधिक चीनी सेवन",
        "Family history": "पारिवारिक इतिहास",
        "High blood pressure": "उच्च रक्तचाप",
    }

    if lang == "Tamil":
        return tamil.get(factor, factor)
    if lang == "Hindi":
        return hindi.get(factor, factor)
    return factor

if st.button(t("check_risk")):
    bmi = weight / ((height / 100) ** 2)
    risk_score = 0
    factors = []

    if age > 45:
        risk_score += 2
        factors.append("Higher age")
    if bmi >= 30:
        risk_score += 3
        factors.append("High BMI")
    if exercise == "Low":
        risk_score += 2
        factors.append("Low exercise")
    if sleep < 6:
        risk_score += 2
        factors.append("Poor sleep")
    if smoking == "Yes":
        risk_score += 2
        factors.append("Smoking")
    if alcohol == "Yes":
        risk_score += 1
        factors.append("Alcohol use")
    if sugar == "Yes":
        risk_score += 2
        factors.append("High sugar intake")
    if family_history == "Yes":
        risk_score += 2
        factors.append("Family history")
    if bp == "Yes":
        risk_score += 2
        factors.append("High blood pressure")

    if risk_score >= 10:
        risk_level = "High"
        risk_level_display = t("high")
    elif risk_score >= 5:
        risk_level = "Medium"
        risk_level_display = t("moderate")
    else:
        risk_level = "Low"
        risk_level_display = t("low")

    display_factors = [factor_display(f) for f in factors]

    st.write(f"**{t('bmi')}:** {bmi:.2f}")
    st.write(f"**{t('risk_score')}:** {risk_score}")
    st.write(f"**{t('risk_level')}:** {risk_level_display}")
    st.write(f"**{t('risk_factors')}:** {', '.join(display_factors) if display_factors else t('no')}")

    lang = current_lang()

    if lang == "Tamil":
        advice = "ஆரோக்கியமான உணவு எடுத்துக்கொள்ளவும். தினமும் சிறிது உடற்பயிற்சி செய்யவும். பிரச்சனை அதிகமாக இருந்தால் மருத்துவரை அணுகவும்."
    elif lang == "Hindi":
        advice = "स्वस्थ भोजन करें और रोज़ थोड़ा व्यायाम करें। समस्या अधिक हो तो डॉक्टर से सलाह लें।"
    else:
        advice = ask_ollama(f"""
Risk level: {risk_level}
BMI: {bmi:.2f}
Factors: {', '.join(factors)}
Give 2 short health tips in English.
""")
        if "⚠️" in advice:
            advice = "Eat healthy food and exercise regularly. Consult a doctor if the problem is serious."

    st.info(advice)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO disease_checks
        (date, age, height, weight, bmi, exercise, sleep, smoking, alcohol, sugar,
        family_history, bp, risk_score, risk_level, factors, advice)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        age, height, weight, bmi, exercise, sleep, smoking, alcohol, sugar,
        family_history, bp, risk_score, risk_level, ", ".join(factors), advice
    ))
    conn.commit()
    conn.close()