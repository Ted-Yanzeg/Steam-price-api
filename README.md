# Live Demo
- Github repo: [https://github.com/Ted-Yanzeg/Steam-price-api]
- 🎮 Shiny App (frontend): [https://steam-price-ui-255067357715.us-central1.run.app]
- 🔌 Prediction API: [https://steam-price-api-255067357715.us-central1.run.app]


# Steam Price Prediction Project

This repository contains a pipeline to:
1. Scrape the top N Steam games’ metadata and reviews.
2. Train a Ridge regression model to predict paid-game prices.
3. Expose a Flask API that serves price predictions.
4. Provide a py-Shiny front-end for interactive user input and chart visualization.
5. Dockerize both back-end and front-end, and deploy them to Google Cloud Run.

<details>
<summary>📁 Repository Structure</summary>

```text
├── README.md                  # Main project description
├── api/
│   ├── README.md              # Describes Flask API
│   └── app.py                 # /predict endpoint
├── scraper/
│   ├── README.md              # Web-scraping logic
│   └── fetch_games.py         # Fetch Steam data
├── model/
│   ├── README.md              # Training notes
│   └── train.py               # Ridge regression
├── shiny/
│   ├── README.md              # py-Shiny frontend
│   └── app.py                 # Interactive UI
├── docker/
│   ├── README.md              # Docker docs
│   ├── Dockerfile             # API container
│   └── Dockerfile.shiny       # Shiny container
├── data/
│   └── steam_games.csv        # Scraped dataset
├── requirements-api.txt       # Flask API deps
└── requirements-shiny.txt     # Frontend deps
</details> ```


