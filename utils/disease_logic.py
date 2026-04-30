def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    return round(weight / (height_m * height_m), 2)

def calculate_disease_risk(age, bmi, exercise, sleep, smoking, alcohol, sugar, family_history, bp):
    score = 0
    factors = []

    if age >= 45:
        score += 2
        factors.append("Higher age")

    if bmi >= 25:
        score += 2
        factors.append("High BMI")

    if exercise == "Low":
        score += 2
        factors.append("Low exercise")

    if sleep < 6:
        score += 1
        factors.append("Poor sleep")

    if smoking == "Yes":
        score += 2
        factors.append("Smoking")

    if alcohol == "Yes":
        score += 1
        factors.append("Alcohol use")

    if sugar == "High":
        score += 2
        factors.append("High sugar intake")

    if family_history == "Yes":
        score += 2
        factors.append("Family history")

    if bp == "High":
        score += 2
        factors.append("High blood pressure")

    if score <= 3:
        level = "Low"
    elif score <= 7:
        level = "Moderate"
    else:
        level = "High"

    return score, level, factors