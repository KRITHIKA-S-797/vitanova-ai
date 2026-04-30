def calculate_mental_score(mood, stress, sleep, energy, appetite, social):
    score = 0

    score += mood
    score += (11 - stress)
    score += sleep
    score += energy
    score += appetite
    score += social

    if score >= 45:
        level = "Stable"
    elif score >= 30:
        level = "Stressed"
    else:
        level = "Needs Support"

    return score, level