def save_dashboard(html, graph_path):
    """
    Save dashboard HTML to disk.
    """

    with open(
        graph_path,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(html)