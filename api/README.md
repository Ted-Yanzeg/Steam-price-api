# Steam-Price Prediction API

This Flask service wraps the **paid-only Ridge-regression model** and exposes a
simple `/predict` endpoint that returns a Steam game’s estimated USD price.

## File Structure
```text
api/
├── app.py # This file – runs the server
└── README.md # Quick-start & endpoint docs
```
## Dependencies

Flask
pandas
numpy
scikit-learn
joblib
