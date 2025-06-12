# Live Demo
- Github repo: [https://github.com/Ted-Yanzeg/Steam-price-api]
- Shiny App (frontend): [https://steam-price-ui-255067357715.us-central1.run.app]
- Prediction API: [https://steam-price-api-255067357715.us-central1.run.app]


# Steam Price Prediction Project

This repository contains a pipeline to:
1. Scrape the top 1000 Steam games’ metadata and reviews.
2. Train a Ridge regression model to predict paid-game prices.
3. Expose a Flask API that serves price predictions.
4. Provide a py-Shiny front-end for interactive user input and chart visualization.
5. Dockerize both back-end and front-end, and deploy them to Google Cloud Run.

## 1. Repository Structure

```text
├── README.md                  # This file
├── Presentation
│   ├── Final Presentation.pdf
│   ├── Final Presentation.pptx
│   └── eda.ipynb              # EDA file
├── api/
│   ├── README.md              # Flask API README
│   └── app.py                 # /predict endpoint
├── scraper/
│   ├── README.md              # Web-scraping README
│   └── fetch_games.py         # Fetch Steam data
├── model/
│   ├── README.md              # Model REANDME
│   ├── paid_price_model.pkl   # Saved model artifact (after training)
│   └── train.py               # Ridge regression
├── shiny/
│   ├── README.md              # py-Shiny frontend README
│   ├── requirements-shiny.txt # Frontend deps
│   └── app.py                 # Interactive UI
├── docker/
│   ├── README.md              # Docker README
│   ├── Dockerfile             # API container
│   └── Dockerfile.shiny       # Shiny container
├── data/
│   ├── README.md              
│   └── steam_games.csv        # Scraped dataset
└── requirements-api.txt       # Flask API deps

``` 

## 2. Quick Start

### Run locally with Docker
```
bash
# 1. build & start API
docker build -f docker/Dockerfile -t steam-api .
docker run -d -p 8080:8080 steam-api

# 2. build & start Shiny UI, pointing to local API
docker build -f docker/Dockerfile.shiny -t steam-ui .
docker run -d -p 8081:8080 \
  -e API_URL=http://host.docker.internal:8080/predict \
  steam-ui

# 3. open the app
open http://localhost:8081          # macOS
```
### Delopy to google cloud run

Replace <DOCKERHUB_USER> with your own Docker Hub username.

Because I’m on an Apple-Silicon Mac, I avoid the arm/amd64 mismatch by letting Google Cloud Build compile the image for the linux/amd64 platform, then deploy it directly to Cloud Run.

```
bash
# A) build & push amd64 images 
docker buildx build --platform linux/amd64 \
  -f docker/Dockerfile \
  -t <DOCKERHUB_USER>/steam-api:latest --push .

docker buildx build --platform linux/amd64 \
  -f docker/Dockerfile.shiny \
  -t <DOCKERHUB_USER>/steam-ui:latest --push .

# B) deploy API
gcloud run deploy steam-price-api \
  --image docker.io/<DOCKERHUB_USER>/steam-api:latest \
  --region us-central1 \
  --allow-unauthenticated
API_URL=$(gcloud run services describe steam-price-api \
         --region us-central1 --format='value(status.url)')/predict

# C) deploy Shiny UI
gcloud run deploy steam-price-ui \
  --image docker.io/<DOCKERHUB_USER>/steam-ui:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_URL=$API_URL
```
