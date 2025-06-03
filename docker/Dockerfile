FROM python:3.10-slim
WORKDIR /app

COPY api/app.py               ./api/app.py
COPY model/paid_price_model.pkl ./model/paid_price_model.pkl
COPY requirements-api.txt     .

RUN pip install --no-cache-dir -r requirements-api.txt

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "flask --app api.app run --host=0.0.0.0 --port=$PORT"]
