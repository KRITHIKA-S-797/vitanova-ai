import pandas as pd
import re

SAFETY_DATA = {
    "paracetamol": {"max": 2, "risk": "medium"},
    "acetaminophen": {"max": 2, "risk": "medium"},
    "ibuprofen": {"max": 2, "risk": "medium"},
    "aspirin": {"max": 2, "risk": "medium"},
    "cetirizine": {"max": 1, "risk": "low"},
    "metformin": {"max": 2, "risk": "medium"},
    "fentanyl": {"max": 0, "risk": "critical"},
    "heroin": {"max": 0, "risk": "critical"},
    "cocaine": {"max": 0, "risk": "critical"},
    "ketamine": {"max": 0, "risk": "high"},
    "methamphetamine": {"max": 0, "risk": "critical"},
}

def extract_number(text):
    match = re.search(r"\d+", text)
    return int(match.group()) if match else None

def analyze_medicine(medicine, dosage_text):
    med = medicine.lower().strip().replace(".", "")
    number = extract_number(dosage_text)

    if med not in SAFETY_DATA:
        if number and number >= 3:
            return "HIGH", f"{medicine} unknown with concerning quantity"
        return "UNKNOWN", f"{medicine} not found in safety database"

    info = SAFETY_DATA[med]

    if info["risk"] == "critical":
        return "CRITICAL", f"{medicine.upper()} is dangerous/illegal and may be life-threatening"

    if info["risk"] == "high":
        return "HIGH", f"{medicine.upper()} is high-risk and needs professional supervision"

    if number and number > info["max"]:
        return "HIGH", f"Possible overdose risk for {medicine}. Quantity exceeds safer single-dose limit"

    return "SAFE", f"No immediate rule-based danger detected for {medicine}"

def check_interactions(medicine_list):
    try:
        df = pd.read_csv("data/medicine_interactions.csv")
    except:
        return []

    warnings = []
    meds = [m.lower().strip() for m in medicine_list]

    for i in range(len(meds)):
        for j in range(i + 1, len(meds)):
            med1, med2 = meds[i], meds[j]
            match = df[
                ((df["med1"].str.lower() == med1) & (df["med2"].str.lower() == med2)) |
                ((df["med1"].str.lower() == med2) & (df["med2"].str.lower() == med1))
            ]
            if not match.empty:
                row = match.iloc[0]
                warnings.append(f"{row['med1']} + {row['med2']} → {row['severity']} risk: {row['warning']}")

    return warnings