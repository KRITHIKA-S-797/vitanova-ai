import streamlit as st
from utils.db import create_tables
from utils.habit_logic import get_total_points
from utils.language import t

st.set_page_config(page_title="VitaNova AI", layout="wide")

create_tables()

if "lang" not in st.session_state:
    st.session_state.lang = "English"

col1, col2 = st.columns([4, 1])

with col1:
    st.session_state.lang = st.selectbox(
        "🌐 Language / மொழி / भाषा",
        ["English", "Tamil", "Hindi"],
        index=["English", "Tamil", "Hindi"].index(st.session_state.lang)
    )

with col2:
    st.markdown(f"### 🏆 {get_total_points()} pts")

st.title(t("app_title"))
st.subheader(t("subtitle"))
st.warning(t("warning"))

st.markdown(f"### {t('modules')}")

st.markdown(f"""
- {t("disease_title")}
- {t("mental_title")}
- {t("diet_title")}
- {t("medicine_title")}
- {t("sos_title")}
- {t("hospital_title")}
- {t("habit_title")}
- {t("dashboard_title")}
- {t("workout_title")}
- {t("chatbot")}
""")