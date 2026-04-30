import streamlit as st
import requests
from utils.language import t

st.title("🚨 " + t("sos_title"))
st.warning(t("warning"))

name = st.text_input(t("name"))
guardian_email = st.text_input(t("guardian_email"))
location = st.text_input(t("location"))

if st.button("🚨 SOS"):
    if not name or not guardian_email or not location:
        st.warning("Please fill all fields")
    else:
        map_link = f"https://www.google.com/maps/search/{location.replace(' ', '+')}"

        url = "https://api.emailjs.com/api/v1.0/email/send"

        payload = {
            "service_id": "service_tcavjzh",
            "template_id": "template_3bqc7ye",
            "user_id": "4AxdxaNxiqq1Jqc48",
            "template_params": {
                "name": name,
                "location": map_link,
                "message": "I need help immediately!",
                "to_email": guardian_email
            }
        }

        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                st.success("Emergency alert sent!")
            else:
                st.error(f"Failed: {response.text}")

        except Exception as e:
            st.error(e)

        st.markdown(f"[📍 View Location on Map]({map_link})")