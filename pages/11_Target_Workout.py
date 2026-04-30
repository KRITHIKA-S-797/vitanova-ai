import streamlit as st
import streamlit.components.v1 as components
from utils.language import t

st.title("🏋️ " + t("workout_title"))

body_options = {
    t("arms"): "Arms",
    t("legs"): "Legs",
    t("belly"): "Belly",
    t("chest"): "Chest",
    t("back"): "Back",
    t("full_body"): "Full Body",
    t("eyes"): "Eyes",
    t("neck"): "Neck",
}

selected_display = st.selectbox(t("body_part"), list(body_options.keys()))
body_part = body_options[selected_display]

exercise_data = {
    "Arms": [
        ("Push Ups", "https://www.youtube.com/embed/IODxDxX7oi4"),
        ("Tricep Dips", "https://www.youtube.com/embed/0326dy_-CzM"),
    ],
    "Legs": [
        ("Squats", "https://www.youtube.com/embed/aclHkVaku9U"),
        ("Lunges", "https://www.youtube.com/embed/QOVaHwm-Q6U"),
    ],
    "Belly": [
        ("Crunches", "https://www.youtube.com/embed/Xyd_fa5zoEU"),
        ("Plank", "https://www.youtube.com/embed/pSHjTRCQxIw"),
    ],
    "Chest": [
        ("Push Ups", "https://www.youtube.com/embed/IODxDxX7oi4"),
        ("Chest Press", "https://www.youtube.com/embed/gRVjAtPip0Y"),
    ],
    "Back": [
        ("Superman Exercise", "https://www.youtube.com/embed/z6PJMT2y8GQ"),
        ("Bird Dog", "https://www.youtube.com/embed/wiFNA3sqjCA"),
    ],
    "Full Body": [
        ("Jumping Jacks", "https://www.youtube.com/embed/c4DAnQ6DtF8"),
        ("Burpees", "https://www.youtube.com/embed/TU8QYVW0gDU"),
    ],
    "Eyes": [
        ("Eye Relaxation", "https://www.youtube.com/embed/GoOLQkt4vkY"),
        ("Eye Exercise", "https://www.youtube.com/embed/2nYjGy_ZUG8"),
    ],
    "Neck": [
        ("Neck Stretch", "https://www.youtube.com/embed/5-3rRz6V9sA"),
        ("Chin Tuck", "https://www.youtube.com/embed/2xSlX7n-IHw"),
    ],
}

if st.button(t("show_exercises")):
    if body_part in ["Eyes", "Neck"]:
        st.warning("These are wellness exercises, not fat-loss exercises.")

    for name, video in exercise_data[body_part]:
        st.subheader(name)
        components.iframe(video, height=315)
        st.markdown("---")