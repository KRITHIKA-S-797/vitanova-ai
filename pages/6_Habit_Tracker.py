import streamlit as st
from datetime import datetime
from utils.db import get_connection
from utils.habit_logic import add_points, get_total_points
from utils.language import t, current_lang

st.title("✅ " + t("habit_title"))

lang = current_lang()

default_habits = {
    "Drink Water": {
        "English": "Drink Water",
        "Tamil": "நீர் குடித்தல்",
        "Hindi": "पानी पीना"
    },
    "Exercise": {
        "English": "Exercise",
        "Tamil": "உடற்பயிற்சி",
        "Hindi": "व्यायाम"
    },
    "Sleep Early": {
        "English": "Sleep Early",
        "Tamil": "விரைவாக தூங்குதல்",
        "Hindi": "जल्दी सोना"
    },
    "Eat Fruits": {
        "English": "Eat Fruits",
        "Tamil": "பழங்கள் சாப்பிடுதல்",
        "Hindi": "फल खाना"
    },
    "Avoid Junk Food": {
        "English": "Avoid Junk Food",
        "Tamil": "ஜங்க் உணவு தவிர்த்தல்",
        "Hindi": "जंक फूड से बचना"
    }
}

display_to_real = {}
display_habits = []

for real_name, labels in default_habits.items():
    display_name = labels.get(lang, real_name)
    display_to_real[display_name] = real_name
    display_habits.append(display_name)

st.subheader(t("select_habits"))

selected_display = st.multiselect(
    t("select_habits"),
    display_habits
)

st.markdown("---")

st.subheader(t("add_habit"))

new_habit = st.text_input(t("add_habit"))

col1, col2 = st.columns(2)

with col1:
    if st.button(t("add")):
        if new_habit.strip():
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO custom_habits (habit_name)
                VALUES (?)
            """, (new_habit.strip(),))

            conn.commit()
            conn.close()

            st.success(t("habit_saved"))
            st.rerun()
        else:
            st.warning(t("add_habit"))

with col2:
    if st.button("🗑️ Clear Custom Habits"):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM custom_habits")

        conn.commit()
        conn.close()

        st.success("Custom habits cleared")
        st.rerun()

st.markdown("---")

conn = get_connection()
cursor = conn.cursor()
cursor.execute("SELECT habit_name FROM custom_habits")
custom_habits = [row[0] for row in cursor.fetchall()]
conn.close()

if custom_habits:
    st.subheader("Custom Habits")
    st.info(
        "Custom habits are shown exactly as you typed them. "
        "For Tamil/Hindi, type your custom habit in that language."
    )

    selected_custom = st.multiselect(
        "Select Custom Habits",
        custom_habits
    )
else:
    selected_custom = []

if st.button(t("save")):
    conn = get_connection()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")
    total = 0

    # Save default habits
    for item in selected_display:
        real_habit = display_to_real.get(item, item)
        points = 10
        total += points

        cursor.execute("""
            INSERT INTO habit_logs (date, habit_name, completed, points, streak)
            VALUES (?, ?, ?, ?, ?)
        """, (
            today,
            real_habit,
            1,
            points,
            1
        ))

    # Save custom habits
    for habit in selected_custom:
        points = 10
        total += points

        cursor.execute("""
            INSERT INTO habit_logs (date, habit_name, completed, points, streak)
            VALUES (?, ?, ?, ?, ?)
        """, (
            today,
            habit,
            1,
            points,
            1
        ))

    conn.commit()
    conn.close()

    add_points(total)

    st.success(f"{t('save')} ✅ +{total} pts")
    st.info(f"🏆 Total Points: {get_total_points()}")