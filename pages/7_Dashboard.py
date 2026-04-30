import streamlit as st
import pandas as pd
from utils.db import get_connection
from utils.habit_logic import get_total_points
from utils.language import t

st.title("📊 " + t("dashboard_title"))

conn = get_connection()

st.subheader("🏆 Total Points")
st.success(get_total_points())

st.subheader("📅 Habit Progress")
try:
    habit_df = pd.read_sql("SELECT * FROM habit_logs", conn)
    if not habit_df.empty:
        habit_df["date"] = pd.to_datetime(habit_df["date"])
        daily_points = habit_df.groupby(habit_df["date"].dt.date)["points"].sum()
        st.line_chart(daily_points)
        st.dataframe(habit_df.tail(5))
    else:
        st.info("No habit data yet")
except Exception as e:
    st.info(f"No habit data: {e}")

st.subheader("🧠 Mental Health Logs")
try:
    mental_df = pd.read_sql("SELECT * FROM mental_logs", conn)
    if not mental_df.empty:
        st.dataframe(mental_df.tail(5))
    else:
        st.info("No mental data")
except:
    st.info("No mental data")

st.subheader("🩺 Disease Risk History")
try:
    disease_df = pd.read_sql("SELECT * FROM disease_checks", conn)
    if not disease_df.empty:
        st.dataframe(disease_df.tail(5))
    else:
        st.info("No disease data")
except:
    st.info("No disease data")

st.subheader("💊 Medicine Logs")
try:
    med_df = pd.read_sql("SELECT * FROM medicines", conn)
    if not med_df.empty:
        st.dataframe(med_df.tail(5))
    else:
        st.info("No medicine data")
except:
    st.info("No medicine data")

conn.close()