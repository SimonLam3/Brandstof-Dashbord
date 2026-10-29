import pandas as pd


def load_history(csv_file):
    """
    Load historical fuel prices from CSV.
    """

    df = pd.read_csv(csv_file)

    df["datetime"] = pd.to_datetime(
        df["datetime"]
    )

    df = df.sort_values(
        by="datetime"
    )

    return df