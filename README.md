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

<details> <summary>📁 Repository Structure</summary>

├── README.md                  # Main project description
├── api/                       
│   ├── README.md              # Describes Flask API
│   └── app.py                 # Flask API: expose /predict endpoint
├── scraper/                   
│   ├── README.md              # Web scraping logic
│   └── fetch_games.py         # Fetch Steam top games data
├── model/                     
│   ├── README.md              # Model training explanation
│   └── train.py               # Train Ridge regression model
├── shiny/                     
│   ├── README.md              # py-Shiny frontend description
│   └── app.py                 # Interactive frontend
├── docker/                    
│   ├── README.md              # Docker instructions
│   ├── Dockerfile             # API container
│   └── Dockerfile.shiny       # Shiny UI container
├── data/                      
│   └── steam_games.csv        # Final scraped dataset
├── requirements-api.txt       # Dependencies for Flask API
└── requirements-shiny.txt     # Dependencies for frontend
</details>

