import streamlit as st
from datetime import datetime
from utils.db import get_connection
from utils.medicine_logic import analyze_medicine, check_interactions
from utils.language import t

st.title("💊 " + t("medicine_title"))
st.warning(t("warning"))

medicines = st.text_area(t("medicine_name"), placeholder="paracetamol, ibuprofen")
dosage = st.text_input(t("dosage"), "1 tablet")

morning = st.checkbox(t("morning"))
afternoon = st.checkbox(t("afternoon"))
night = st.checkbox(t("night"))

if st.button(t("check")):
    med_list = [m.strip() for m in medicines.split(",") if m.strip()]

    if not med_list:
        st.warning(t("medicine_name"))
    else:
        results = []

        for med in med_list:
            level, msg = analyze_medicine(med, dosage)
            results.append(msg)

            if level == "CRITICAL":
                st.error("🚨 " + msg)
            elif level == "HIGH":
                st.error("⚠️ " + msg)
            elif level == "UNKNOWN":
                st.warning("⚠️ " + msg)
            else:
                st.success(msg)

        warnings = check_interactions(med_list)

        st.subheader(t("interaction"))

        if warnings:
            for w in warnings:
                st.error(w)
        else:
            st.info(t("no_interaction"))

        conn = get_connection()
        cursor = conn.cursor()

        for med in med_list:
            cursor.execute("""
                INSERT INTO medicines (date, medicine_name, dosage, morning, afternoon, night, warning_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                med,
                dosage,
                int(morning),
                int(afternoon),
                int(night),
                " | ".join(results)
            ))

        conn.commit()
        conn.close()