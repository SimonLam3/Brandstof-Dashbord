import csv
from datetime import datetime
from zoneinfo import ZoneInfo


def save_price_to_csv(
    csv_file,
    pump_price,
    discount,
    net_price
):
    """
    Save a fuel price to the CSV file.

    The price is only saved when the same
    net price has not already been stored today.

    Returns:
        bool: True if a new price was saved.
    """

    file_exists = csv_file.exists()
    save_price = True

    if file_exists:

        with open(
            csv_file,
            "r",
            encoding="utf-8"
        ) as f:

            reader = csv.reader(f)

            next(reader, None)

            last_row = None

            for row in reader:
                if row:
                    last_row = row

        if last_row:

            last_date = (
                last_row[0]
                .split(" ")[0]
            )

            last_price = float(
                last_row[3]
            )

            today = (
                datetime.now(
                    ZoneInfo("Europe/Amsterdam")
                )
                .date()
                .isoformat()
            )

            if (
                last_date == today
                and abs(
                    last_price - net_price
                ) < 0.0001
            ):
                save_price = False

    if save_price:

        with open(
            csv_file,
            "a",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "datetime",
                    "pump_price",
                    "discount",
                    "net_price"
                ])

            writer.writerow([
            datetime.now(
                ZoneInfo("Europe/Amsterdam")
            ).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
                pump_price,
                discount,
                net_price
            ])

    return save_price