# shiny/app.py

from shiny import App, ui, render, reactive
import plotly.express as px
import requests, os

API_URL = os.getenv("API_URL", "http://localhost:8080/predict")

genres = [
    "Action", "Adventure", "RPG", "Strategy", "Indie",
    "Simulation", "Sports", "Racing", "Casual", "Massively Multiplayer"
]

# Define rating levels and corresponding numeric values
rating_levels = {
    "Overwhelmingly Negative (0–20%)": 0.10,
    "Mostly Negative (20–40%)": 0.30,
    "Mixed (40–70%)": 0.55,
    "Mostly Positive (70–80%)": 0.75,
    "Very Positive (80–95%)": 0.875,
    "Overwhelmingly Positive (95–100%)": 0.975,
}

# Define review count tiers and corresponding numeric values
review_tiers = {
    "Low (< 5,000)": 2000,
    "Medium (5,000 – 50,000)": 20000,
    "High (> 50,000)": 100000,
}

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_numeric("yr", "Release Year", 2024, min=2000, max=2025),
        ui.input_select("rating_level", "Rating Tier",
                        choices=list(rating_levels.keys()),
                        selected="Overwhelmingly Positive (95–100%)"),
        ui.input_select("review_tier", "Review Count Tier",
                        choices=list(review_tiers.keys()),
                        selected="Medium (5,000 – 50,000)"),
        ui.input_checkbox("mp", "Multiplayer?", True),
        ui.input_checkbox_group("gen", "Genres",
                                choices=genres, selected=["Action"]),
        ui.input_action_button("go", "Predict", class_="btn-primary"),
    ),
    ui.h4("Predicted Price (USD):"),
    ui.output_text("price"),
    ui.hr(),
    ui.h5("Price vs. Release Year"),
    ui.output_ui("year_curve_ui"),
    ui.hr(),
    ui.h5("Price vs. Rating Tier"),
    ui.output_ui("rating_scatter_ui"),
)

def make_payload(year, rating_key, review_key, multiplayer, genre_list):
    return {
        "release_year": year,
        "positive_ratio": rating_levels[rating_key],
        "total_reviews": review_tiers[review_key],
        "is_multiplayer": multiplayer,
        "genres": genre_list,
    }

def pred_price(payload):
    return requests.post(API_URL, json=payload, timeout=5).json()["predicted_price"]

def server(input, output, session):
    @output
    @render.text
    def price():
        if input.go() == 0:
            return "—"
        payload = make_payload(
            input.yr(), input.rating_level(), input.review_tier(),
            int(input.mp()), list(input.gen())
        )
        p = pred_price(payload)
        return f"${p:.2f}"

    @output
    @render.ui
    def year_curve_ui():
        years = list(range(2010, 2026))
        prices = []
        for y in years:
            payload = make_payload(
                y, input.rating_level(), input.review_tier(),
                int(input.mp()), list(input.gen())
            )
            prices.append(pred_price(payload))

        fig = px.line(
            x=years, y=prices,
            labels={"x": "Release Year", "y": "Price ($)"}
        )
        html = fig.to_html(full_html=False)
        return ui.HTML(html)

    @output
    @render.ui
    def rating_scatter_ui():
        # Use the numeric values of each rating tier as x-axis
        xs = list(rating_levels.values())
        xs_labels = list(rating_levels.keys())
        prices = []
        for key in rating_levels:
            payload = make_payload(
                input.yr(), key, input.review_tier(),
                int(input.mp()), list(input.gen())
            )
            prices.append(pred_price(payload))

        fig = px.scatter(
            x=xs, y=prices,
            labels={"x": "Rating Tier Value", "y": "Price ($)"},
            hover_name=xs_labels
        )
        html = fig.to_html(full_html=False)
        return ui.HTML(html)

app = App(app_ui, server)
