from pathlib import Path
import subprocess

from functions.data.get_current_price import get_current_price
from functions.data.save_price_to_csv import save_price_to_csv
from functions.data.load_history import load_history
from functions.germany.get_page import get_page
from functions.germany.get_vorrink_price import get_vorrink_price
from functions.germany.is_it_worth_it import is_worth_it
from functions.calculations.calculate_statistics import (
    calculate_statistics
)
from functions.calculations.calculate_score import (
    calculate_score
)
from functions.calculations.get_trend import (
    get_trend
)
from functions.dashboard.get_dashboard_colors import (
    get_dashboard_colors
)

from functions.dashboard.create_dashboard import (
    create_dashboard
)
from functions.dashboard.save_dashboard import (
    save_dashboard
)

def main():

    csv_file = (
        Path(__file__).parent
        / "fuel_prices.csv"
    )

    graph_path = (
        Path(__file__).parent
        / "index.html"
    )

    # Get current fuel price
    pump_price, discount, net_price = (
        get_current_price()
    )

    # Germany Comparison

    html = get_page()

    vorrink_price = get_vorrink_price(html)

    if vorrink_price is None:
        vorrink_result = {
            "profit": 0,
            "worth_it": False
        }
    else:
        vorrink_result = is_worth_it(
            nl_price=net_price,
            de_price=vorrink_price,
            distance_km=18
        )

    # Save price if needed
    save_price_to_csv(
        csv_file,
        pump_price,
        discount,
        net_price
    )

    # Load historical data
    df = load_history(csv_file)

    # Calculate statistics
    stats = calculate_statistics(df)

    # Calculate trend
    trend, current_price_color = (
        get_trend(df)
    )

    # 7 Days
    (
        score_7d,
        score_label_7d,
        fuel_recommendation_7d
    ) = calculate_score(
        stats["current_price"],
        stats["lowest_price_7d"],
        stats["average_7d"]
    )

    # 30 Days
    (
        score_30d,
        score_label_30d,
        fuel_recommendation_30d
    ) = calculate_score(
        stats["current_price"],
        stats["lowest_price_30d"],
        stats["average_30d"]
    )

    # 365 Days
    (
        score_365d,
        score_label_365d,
        fuel_recommendation_365d
    ) = calculate_score(
        stats["current_price"],
        stats["lowest_price_365d"],
        stats["average_365d"]
    )

    # All Time
    (
        score_all,
        score_label_all,
        fuel_recommendation_all
    ) = calculate_score(
        stats["current_price"],
        stats["lowest_price"],
        stats["historical_average"]
    )

    # Default dashboard period (30D when page loads)

    background_color, border_color = (
        get_dashboard_colors(score_30d)
    )

    dashboard = create_dashboard(
        df=df,
        stats=stats,
        trend=trend,

        current_price_color=current_price_color,

        score_7d=score_7d,
        score_30d=score_30d,
        score_365d=score_365d,
        score_all=score_all,

        fuel_recommendation_7d=fuel_recommendation_7d,
        fuel_recommendation_30d=fuel_recommendation_30d,
        fuel_recommendation_365d=fuel_recommendation_365d,
        fuel_recommendation_all=fuel_recommendation_all,

        border_color=border_color,
        background_color=background_color,

        vorrink_result=vorrink_result,
        vorrink_price=vorrink_price
    )


    # Save dashboard image
    save_dashboard(
        dashboard,
        graph_path
    )

    git_path = r"C:\Program Files\Git\cmd\git.exe"

    subprocess.run(
        [git_path, "add", "."]
    )

    commit_result = subprocess.run(
        [
            git_path,
            "commit",
            "-m",
            "Automatic update"
        ],
        capture_output=True,
        text=True
    )

    print(commit_result.stdout)
    print(commit_result.stderr)

    if "nothing to commit" not in commit_result.stdout:
        subprocess.run(
            [git_path, "push"]
        )

if __name__ == "__main__":
    main()