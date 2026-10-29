import pandas as pd
from datetime import datetime


def calculate_statistics(df):
    """
    Calculate all dashboard statistics.

    Returns:
        dict: Dictionary containing all calculated values.
    """

    current_price = df["net_price"].iloc[-1]

    lowest_price = df["net_price"].min()
    highest_price = df["net_price"].max()

    latest_date = df["datetime"].max()

    # ----------------------------------
    # Period datasets
    # ----------------------------------

    last_7_days = df[
        df["datetime"]
        >= latest_date - pd.Timedelta(days=7)
    ]

    last_30_days = df[
        df["datetime"]
        >= latest_date - pd.Timedelta(days=30)
    ]

    last_365_days = df[
        df["datetime"]
        >= latest_date - pd.Timedelta(days=365)
    ]

    # ----------------------------------
    # Period averages
    # ----------------------------------

    average_7d = (
        last_7_days["net_price"]
        .mean()
    )

    average_30d = (
        last_30_days["net_price"]
        .mean()
    )

    average_365d = (
        last_365_days["net_price"]
        .mean()
    )

    historical_average = (
        df["net_price"]
        .mean()
    )

    # ----------------------------------
    # Period minimums
    # ----------------------------------

    lowest_price_7d = (
        last_7_days["net_price"]
        .min()
    )

    lowest_price_30d = (
        last_30_days["net_price"]
        .min()
    )

    lowest_price_365d = (
        last_365_days["net_price"]
        .min()
    )

    # ----------------------------------
    # Savings
    # ----------------------------------

    savings_per_liter = (
        average_30d - current_price
    )

    savings_per_30l = (
        savings_per_liter * 30
    )

    # ----------------------------------
    # Relative position
    # ----------------------------------

    cheaper_than_percent = round(
        (
            (
                df["net_price"]
                >= current_price
            ).sum()
            / len(df)
        ) * 100
    )

    # ----------------------------------
    # Last price change
    # ----------------------------------

    price_change = (
        df["net_price"]
        != df["net_price"].shift()
    )

    last_price_change = (
        df.loc[
            price_change,
            "datetime"
        ].iloc[-1]
    )

    time_since_change = (
        datetime.now()
        - last_price_change.to_pydatetime()
    )

    days_since_change = (
        time_since_change.days
    )

    hours_since_change = (
        time_since_change.seconds // 3600
    )

    return {
        "current_price": current_price,

        "lowest_price": lowest_price,
        "highest_price": highest_price,

        "lowest_price_7d": lowest_price_7d,
        "lowest_price_30d": lowest_price_30d,
        "lowest_price_365d": lowest_price_365d,

        "average_7d": average_7d,
        "average_30d": average_30d,
        "average_365d": average_365d,

        "historical_average": historical_average,

        "savings_per_liter": savings_per_liter,
        "savings_per_30l": savings_per_30l,

        "cheaper_than_percent": cheaper_than_percent,

        "days_since_change": days_since_change,
        "hours_since_change": hours_since_change,

        "latest_date": latest_date
    }