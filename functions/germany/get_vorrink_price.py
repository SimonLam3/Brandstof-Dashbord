import re

def get_vorrink_price(html):
    match = re.search(
        r'Super E5.*?id="current-price-3">([\d.]+)</span>\s*<sup[^>]*>(\d)</sup>',
        html,
        re.DOTALL
    )

    if match:
        return float(match.group(1) + match.group(2))

    return None