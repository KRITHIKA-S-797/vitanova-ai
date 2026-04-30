import streamlit as st
from utils.ollama_client import ask_ollama
from utils.language import t, current_lang

st.title("🥗 " + t("diet_title"))
st.warning(t("warning"))

age = st.number_input(t("age"), 10, 100, 20)

goal = st.selectbox(t("goal"), ["Weight Loss", "Weight Gain", "Maintain Weight"])
diet_type = st.selectbox(t("diet_type"), ["Vegetarian", "Non-Vegetarian", "Vegan"])
activity = st.selectbox(t("activity"), ["Low", "Moderate", "High"])
region = st.selectbox(t("region"), ["South Indian", "North Indian"])

health = st.text_input(
    t("health_condition"),
    placeholder="Diabetes, BP, Thyroid, etc."
)

def is_complete(text):
    required = ["Breakfast", "Lunch", "Dinner", "Snacks"]
    return all(r.lower() in text.lower() for r in required)

def fallback_plan(lang):
    if lang == "Tamil":
        return """
### 🥣 காலை உணவு
- இட்லி
- தோசை
- ஓட்ஸ்
- பழங்கள்
- முளைகட்டிய பயறு

### 🍛 மதிய உணவு
- அரிசி + பருப்பு
- சப்பாத்தி + காய்கறி
- தயிர்
- சாலட்
- கறி

### 🍽 இரவு உணவு
- சூப்
- சப்பாத்தி
- காய்கறி
- பருப்பு
- சாலட்

### 🍿 சிற்றுண்டி
- பழங்கள்
- நட்ஸ்
- வறுத்த கொண்டைக்கடலை
- பால்
- மோர்
"""
    if lang == "Hindi":
        return """
### 🥣 नाश्ता
- इडली
- डोसा
- ओट्स
- फल
- स्प्राउट्स

### 🍛 दोपहर का खाना
- चावल + दाल
- रोटी + सब्जी
- दही
- सलाद
- करी

### 🍽 रात का खाना
- सूप
- रोटी
- सब्जी
- दाल
- सलाद

### 🍿 स्नैक्स
- फल
- नट्स
- भुना चना
- दूध
- छाछ
"""
    return """
### 🥣 Breakfast
- Idli
- Dosa
- Oats
- Fruits
- Sprouts

### 🍛 Lunch
- Rice + dal
- Chapati + vegetables
- Curd
- Salad
- Curry

### 🍽 Dinner
- Soup
- Chapati
- Vegetables
- Dal
- Salad

### 🍿 Snacks
- Fruits
- Nuts
- Roasted chana
- Milk
- Buttermilk
"""

if st.button(t("generate")):
    lang = current_lang()

    prompt = f"""
Create a FULL 1-day Indian diet plan.

User Profile:
Age: {age}
Goal: {goal}
Diet Type: {diet_type}
Activity Level: {activity}
Region: {region}
Health Condition: {health}

Reply language: {lang}

STRICT RULES:
- Must include Breakfast, Lunch, Dinner, Snacks
- Each section must contain 5 to 10 different foods
- Foods must match region
- Diet must match goal
- If health condition exists, adjust foods accordingly
- Only food list
"""

    with st.spinner("Generating personalized diet..."):
        result = ask_ollama(prompt)

    if "⚠️" in result or not result.strip():
        st.warning("Using fallback plan")
        st.markdown(fallback_plan(lang))
    else:
        st.success("Diet Plan")
        st.markdown(result)