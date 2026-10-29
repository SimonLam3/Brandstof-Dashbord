def get_dashboard_colors(score):
    """
    Return dashboard colors based on score.
    """

    if score >= 75:
        return "#f2fff2", "green"

    elif score >= 50:
        return "#fffde8", "gold"

    return "#fff2f2", "red"