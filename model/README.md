# Model Training

This folder contains the code and artifacts for training a Ridge regression model that predicts the (log-transformed) price of paid Steam games.

## File Structure
```text
model/
├── train_paid_only.py    # Script to train the regression model 
├── paid_price_model.pkl  # Saved model artifact (after training)
└── README.md             # This file
```
## Dependencies

Install the required Python packages before running the training script:

```bash
pip install pandas numpy scikit-learn joblib
```

## Training the Model

To train the model, run the following command:

```bash
python train.py
```

This script will load the data from the `data` folder, preprocess it, and train a Ridge regression model. The trained model will be saved as `paid_price_model.pkl` in the `model` folder.

## Expected console output:

R² on paid-only test: 
paid_price_model.pkl saved
