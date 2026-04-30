import pandas as pd

def generate_diet_plan(age, weight, goal, preference, region, budget, condition):
    df = pd.read_csv("data/indian_foods.csv")

    if preference == "Veg":
        df = df[df["preference"] == "Veg"]

    if region != "All":
        df = df[(df["region"] == region) | (df["region"] == "All")]

    if budget != "Any":
        df = df[df["budget"] == budget]

    if condition != "Any":
        df = df[(df["condition"] == condition) | (df["condition"] == "General")]

    breakfast = df[df["category"] == "Breakfast"].head(1)
    lunch = df[df["category"] == "Lunch"].head(2)
    snacks = df[df["category"] == "Snacks"].head(1)
    dinner = df[df["category"] == "Dinner"].head(1)

    return {
        "breakfast": ", ".join(breakfast["food_name"].tolist()),
        "lunch": ", ".join(lunch["food_name"].tolist()),
        "snacks": ", ".join(snacks["food_name"].tolist()),
        "dinner": ", ".join(dinner["food_name"].tolist()),
        "water_goal": "2.5 to 3 liters"
    }