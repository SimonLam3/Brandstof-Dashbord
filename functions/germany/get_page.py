import requests

def get_page():
    url = "https://www.clever-tanken.de/tankstelle_details/48339"

    r = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    print("Status:", r.status_code)

    if r.status_code != 200:
        return None

    return r.text