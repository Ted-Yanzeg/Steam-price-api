# docker/ – Container Recipes

This folder holds **two Dockerfiles**—one for the *model API* and one for the
*Shiny-for-Python UI*.  Each image is completely standalone so you can deploy
them to Cloud Run (or any OCI-compatible runtime) without sharing volumes.

## file structure
```text
docker/
├── Dockerfile # Flask / FastAPI prediction API image
└── Dockerfile.shiny # Shiny-for-Python front-end image
```
## Dockerfile Build & test locally

```bash
docker build -f docker/Dockerfile -t steam-price-api .
docker run -p 8080:8080 steam-price-api
curl -X POST localhost:8080/predict \
     -H "Content-Type: application/json" \
     -d '{"release_year":2024,"positive_ratio":0.9,"total_reviews":10000,"is_multiplayer":1,"genres":["Action"]}'

```

## Dockerfile.shiny Build & test locally

```bash
docker build -f docker/Dockerfile.shiny -t steam-shiny:latest .
docker run -p 8081:8080 \                                      
  --env API_URL=http://host.docker.internal:8080/predict \
  steam-shiny:latest
```
