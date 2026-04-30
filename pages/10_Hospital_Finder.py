import streamlit as st
from utils.language import t

st.title("🏥 " + t("hospital_title"))

city = st.text_input(t("city"), "Chennai")

care_display = st.selectbox(
    t("care_type"),
    ["General", "Emergency", "Cardiology", "Orthopedic", "Neurology", "Clinic"]
)

if st.button(t("find")):
    query = f"{care_display} hospital clinic near {city}"
    maps_link = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    st.success(t("nearby_hospital"))
    st.markdown(f"[📍 {t('open_maps')}]({maps_link})")
    st.info(t("hospital_info"))