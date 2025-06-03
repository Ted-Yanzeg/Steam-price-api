# Steam Price Prediction Project

This repository contains a pipeline to:
1. Scrape the top N Steam games’ metadata and reviews.
2. Train a Ridge regression model to predict paid-game prices.
3. Expose a Flask REST API that serves price predictions.
4. Provide a py-Shiny front-end for interactive user input and chart visualization.
5. Dockerize both back-end and front-end, and deploy them to Google Cloud Run.

## Repository Structure

├── README.md              # this file
├── api/                   
│ └── README.md
│ └── app.py               # Flask API: load a saved model, expose /predict endpoint
├── scraper/ 
│ └── README.md
│ └── fetch_games.py       # Fetch top N games’ metadata and reviews
├── model/ 
│ └── README.md
│ └── train.py             # Train a Ridge regression model
├── shiny/                 
│ └── README.md
│ └── app.py               # py-Shiny front-end
├── docker/                
│ └── README.md
│ └── Dockerfile           # Dockerfiles for API 
│ └── Dockerfile.shiny     # Dockerfiles for Shiny
├── data/                  
│ └── steam_games.csv      # Output CSV (steam_games.csv)
└── requirements-api.txt   # Dependencies for the Flask API
requirements-shiny.txt     # Dependencies for the Shiny front-end


## Quick Start

1. **Scrape data**  
   ```bash
   cd scraper
   python fetch_games.py -n 1000 --sleep 0.5 --out ../data/steam_games.csv
2. **Train model**
   ```bash
   cd model
   python train.py
