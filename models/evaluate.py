import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv("data/reliance_ml_dataset.csv")

features = [
    "close",
    "volume",
    "sma_20",
    "sma_50",
    "ema_20",
    "rsi_14",
    "macd"
]

X = df[features]
y = df["target"]

split_index = int(len(df) * 0.8)

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]

model = joblib.load("models/model.pkl")

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("Model Evaluation")
print("----------------")
print(f"Test Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(classification_report(y_test, predictions, zero_division=0))