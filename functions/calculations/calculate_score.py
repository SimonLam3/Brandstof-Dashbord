def calculate_score(
    current_price,
    lowest_price,
    average_price
):
    """
    Calculate a fuel price score and recommendation.

    Args:
        current_price (float):
            Current fuel price.

        lowest_price (float):
            Lowest price within the selected period.

        average_price (float):
            Average price within the selected period.

    Returns:
        tuple:
        (
            score,
            score_label,
            fuel_recommendation
        )
    """

    # Prevent division by zero
    if abs(average_price - lowest_price) < 0.0001:
        score = 100

    else:
        score = 100 - (
            (current_price - lowest_price)
            / (average_price - lowest_price)
        ) * 100

    # Clamp score between 0 and 100
    score = max(0, min(100, score))

    # -----------------------------
    # Score label
    # -----------------------------

    if score >= 75:
        score_label = "GOOD"

    elif score >= 50:
        score_label = "FAIR"

    elif score >= 25:
        score_label = "EXPENSIVE"

    else:
        score_label = "VERY EXPENSIVE"

    # -----------------------------
    # Recommendation
    # -----------------------------

    if score >= 85:
        fuel_recommendation = "Fill Up Now"

    elif score >= 70:
        fuel_recommendation = "Good Time To Fuel"

    elif score >= 50:
        fuel_recommendation = "Acceptable Price"

    elif score >= 30:
        fuel_recommendation = "Consider Waiting"

    else:
        fuel_recommendation = "Wait If Possible"

    return (
        round(score, 1),
        score_label,
        fuel_recommendation
    )