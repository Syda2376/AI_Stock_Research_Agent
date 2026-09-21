import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

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

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("logistic", LogisticRegression(max_iter=1000))
])

model.fit(X_train, y_train)

latest_data = X_test.iloc[[-1]]

probabilities = model.predict_proba(latest_data)[0]

print("Latest ML Prediction")
print("--------------------")
print(f"Probability of negative return: {probabilities[0]:.2%}")
print(f"Probability of positive return: {probabilities[1]:.2%}")

if probabilities[1] >= 0.5:
    print("ML Signal: POSITIVE")
else:
    print("ML Signal: NEGATIVE")