import re
import requests


def get_current_price():
    """
    Fetch the current Euro95 price from the
    Tango Hardenberg website.

    Returns:
        tuple:
        (
            pump_price,
            discount,
            net_price
        )
    """

    html = requests.get(
        "https://www.tango.nl/stations/tango-hardenberg",
        timeout=10
    ).text

    match = re.search(
        r'PETROL_EURO_95\\",\\"price\\":([0-9.]+),\\"discountPrice\\":([0-9.]+)',
        html
    )

    if not match:
        raise ValueError(
            "Euro95 price could not be found on the website."
        )

    pump_price = float(match.group(1))
    discount = float(match.group(2))

    net_price = (
        pump_price
        - (discount / 10)
    )

    return (
        pump_price,
        discount,
        net_price
    )