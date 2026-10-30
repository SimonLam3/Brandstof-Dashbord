import plotly.graph_objects as go
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def create_dashboard(
    df,
    stats,
    trend,

    current_price_color,

    score_7d,
    score_30d,
    score_365d,
    score_all,

    fuel_recommendation_7d,
    fuel_recommendation_30d,
    fuel_recommendation_365d,
    fuel_recommendation_all,

    border_color,
    background_color,

    vorrink_result,
    vorrink_price
):
    
    """
    Create interactive fuel dashboard.
    """

    last_check = datetime.now(
        ZoneInfo("Europe/Amsterdam")
    ).strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    fig = go.Figure()

    # -------------------------------------------------
    # Main Fuel Price Line
    # -------------------------------------------------

    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=df["net_price"],
            mode="lines",
            name="Euro95",
            line=dict(
                width=4,
                color="#2563EB"
            ),
            hovertemplate=(
                "Date: %{x|%d-%m-%Y %H:%M}<br>"
                "Price: €%{y:.3f}"
                "<extra></extra>"
            )
        )
    )

    # -------------------------------------------------
    # Average Lines
    # (as traces, not hlines)
    # -------------------------------------------------

    # 7-Day Average
    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=[stats["average_7d"]] * len(df),
            mode="lines",
            name="7-Day Average",
            visible=False,
            line=dict(
                color="#8B5CF6",
                width=2
            )
        )
    )

    # 30-Day Average 
    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=[stats["average_30d"]] * len(df),
            mode="lines",
            name="30-Day Average",
            visible=False,
            line=dict(
                color="#F59E0B",
                width=2
            )
        )
    )

    # 365-Day Average
    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=[stats["average_365d"]] * len(df),
            mode="lines",
            name="365-Day Average",
            visible=False,
            line=dict(
                color="#10B981",
                width=2
            )
        )
    )

    # Historical Average (default visible)
    fig.add_trace(
        go.Scatter(
            x=df["datetime"],
            y=[stats["historical_average"]] * len(df),
            mode="lines",
            name="Historical Average",
            visible=True,
            line=dict(
                color="gray",
                width=2,
                dash="dash"
            )
        )
    )

    # -------------------------------------------------
    # Layout
    # -------------------------------------------------

    fig.update_layout(
        title="",

        height=400,

        autosize=True,

        template="plotly_white",

        paper_bgcolor="white",
        plot_bgcolor="white",

        hovermode="x unified",

        margin=dict(
            t=40,
            l=40,
            r=40,
            b=40
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),

        xaxis=dict(
            type="date"
        ),

        xaxis_title="Date",
        yaxis_title="Price (€ per litre)"
    )

    plot_html = fig.to_html(
        full_html=False,
        include_plotlyjs=True,
        config={
            "responsive": True
        }
    )

    latest_date = stats["latest_date"]

    date_7d = (
        latest_date - timedelta(days=7)
    ).strftime("%Y-%m-%d")

    date_30d = (
        latest_date - timedelta(days=30)
    ).strftime("%Y-%m-%d")

    date_365d = (
        latest_date - timedelta(days=365)
    ).strftime("%Y-%m-%d")

    latest_date_str = (
        latest_date.strftime("%Y-%m-%d")
    )

    html = f"""
    <!DOCTYPE html>
    <html lang="en">

    <head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Fuel Dashboard</title>

    <style>

    body {{
        font-family: Arial, sans-serif;
        background-color: #f5f7fa;
        margin: 0;
        padding: 20px;
    }}

    .container {{
        max-width: 1400px;
        margin: auto;
    }}

    .header {{
        text-align: center;
        margin-bottom: 25px;
    }}

    .cards {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 15px;
        margin-bottom: 20px;
    }}

    .card {{
        background: white;
        border-left: 5px solid {border_color};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        text-align: center;
    }}

    .card-title {{
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
    }}

    .card-value {{
        font-size: 24px;
        font-weight: bold;
    }}

    .graph-wrapper {{
        background: white;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        overflow-x: auto;
    }}

    .period-buttons {{

        display: flex;

        justify-content: center;

        gap: 10px;

        flex-wrap: wrap;

        margin-bottom: 15px;
    }}

    .period-btn {{

        border: none;

        background: #2563EB;

        color: white;

        padding: 10px 20px;

        border-radius: 10px;

        cursor: pointer;

        font-weight: bold;
    }}

    .period-btn:hover {{

        background: #1D4ED8;
    }}

    .period-btn.active {{

        background: #111827;
    }}

    .js-plotly-plot {{
        width: 100% !important;
    }}

    @media (max-width: 768px) {{

        body {{
            padding: 12px;
        }}

        .card {{
            padding: 25px;
        }}

        .card-value {{
            font-size: 28px;
        }}

        .graph-wrapper {{
            padding: 5px;
        }}
    }}

    </style>

    <head>

    <link rel="icon" type="image/png" href="favicon.png">

    <link rel="apple-touch-icon" href="favicon.png">

    <meta charset="UTF-8">


    <body>

    <div class="container">

    <div class="header">
    <h1>Tango Hardenberg Euro95</h1>

    <p>
    Last Updated:
    {last_check}
    </p>
    </div>

    <div class="cards">

        <div class="card">
            <div class="card-title">Recommendation</div>
            <div
                id="recommendation-card"
                class="card-value"
            >
                {fuel_recommendation_all}
            </div>
            <div>
                €{stats['savings_per_30l']:.2f} per 30L
            </div>
        </div>

        <div class="card">
            <div class="card-title">Current Price</div>
            <div
                class="card-value"
                style="color:{current_price_color};"
            >
                €{stats['current_price']:.3f}/L
            </div>
        </div>

        <div class="card">
            <div class="card-title">Score</div>
            <div
                id="score-card"
                class="card-value"
            >
                {score_all:.0f}/100
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                Last Price Change
            </div>
            <div class="card-value">
                {stats['days_since_change']}d
                {stats['hours_since_change']}h
            </div>
        </div>

        <div class="card">
            <div class="card-title">
                Germany
            </div>

            <div>
                {
                    "€" + format(vorrink_price, ".3f") + "/L"
                    if vorrink_price is not None
                    else "Unavailable"
                }
            </div>

            <div>
                €{vorrink_result['profit']:.2f}
            </div>

            <div class="card-value">
                {
                    "Worth It"
                    if vorrink_result["worth_it"]
                    else "Not Worth It"
                }
            </div>
        </div>

    </div>

    <div class="period-buttons">

        <button
            class="period-btn active"
            onclick="setPeriod('all', this)"
        >
            ALL
        </button> 

        <button
            class="period-btn"
            onclick="setPeriod('7d', this)"
        >
            7D
        </button>   

        <button
            class="period-btn"
            onclick="setPeriod('30d', this)"
        >
            30D
        </button>

        <button
            class="period-btn"
            onclick="setPeriod('365d', this)"
        >
            365D
        </button>

    </div>  

    <div class="graph-wrapper">
        {plot_html}
    </div>

    </div>

    <script>

    const dashboardData = {{

        "7d": {{
            recommendation: "{fuel_recommendation_7d}",
            score: "{score_7d:.0f}/100"
        }},

        "30d": {{
            recommendation: "{fuel_recommendation_30d}",
            score: "{score_30d:.0f}/100"
        }},

        "365d": {{
            recommendation: "{fuel_recommendation_365d}",
            score: "{score_365d:.0f}/100"
        }},

        "all": {{
            recommendation: "{fuel_recommendation_all}",
            score: "{score_all:.0f}/100"
        }}

    }};

    const ranges = {{

        "7d": {{
            start: "{date_7d}",
            end: "{latest_date_str}",
            traces: [true, true, false, false, false]
        }},

        "30d": {{
            start: "{date_30d}",
            end: "{latest_date_str}",
            traces: [true, false, true, false, false]
        }},

        "365d": {{
            start: "{date_365d}",
            end: "{latest_date_str}",
            traces: [true, false, false, true, false]
        }},

        "all": {{
            start: null,
            end: null,
            traces: [true, false, false, false, true]
        }}

    }};

            function setPeriod(period, button)
        {{

            document.getElementById(
                "recommendation-card"
            ).innerHTML =
                dashboardData[period].recommendation;

            document.getElementById(
                "score-card"
            ).innerHTML =
                dashboardData[period].score;

            document
                .querySelectorAll(".period-btn")
                .forEach(btn =>
                    btn.classList.remove("active")
                );

            button.classList.add("active");

            const graph =
                document.querySelector(
                    ".plotly-graph-div"
                );

            if (!graph)
            {{
                return;
            }}

            if (typeof Plotly === "undefined")
            {{
                return;
            }}

            Plotly.restyle(
                graph,
                {{
                    visible:
                        ranges[period].traces
                }}
            );

            if (period === "all")
            {{

                Plotly.relayout(
                    graph,
                    {{
                        "xaxis.autorange": true
                    }}
                );

            }}
            else
            {{

                Plotly.relayout(
                    graph,
                    {{
                        "xaxis.range": [
                            ranges[period].start,
                            ranges[period].end
                        ]
                    }}
                );

            }}

        }}

    </script>    

    </body>
    </html>
    """

    return html