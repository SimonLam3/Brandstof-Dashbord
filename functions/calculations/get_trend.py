def get_trend(df):
    """
    Determine whether the fuel price is rising,
    falling or unchanged.

    Returns:
        tuple:
        (
            trend,
            current_price_color
        )
    """

    if len(df) >= 2:

        current_price = df["net_price"].iloc[-1]
        previous_price = df["net_price"].iloc[-2]

        if current_price > previous_price:
            trend = "▲"
            current_price_color = "red"

        elif current_price < previous_price:
            trend = "▼"
            current_price_color = "limegreen"

        else:
            trend = "►"
            current_price_color = "dodgerblue"

    else:

        trend = "►"
        current_price_color = "dodgerblue"

    return trend, current_price_color
