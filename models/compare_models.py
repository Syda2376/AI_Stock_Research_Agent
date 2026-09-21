import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

from xgboost import XGBClassifier

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
y_test = y.iloc[split_index:]

logistic = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000))
])

xgb = XGBClassifier(
    n_estimators=100,
    max_depth=3,
    learning_rate=0.05,
    random_state=42,
    eval_metric="logloss"
)

logistic.fit(X_train, y_train)
xgb.fit(X_train, y_train)

logistic_pred = logistic.predict(X_test)
xgb_pred = xgb.predict(X_test)

print("Model Comparison")
print("----------------")
print(f"Logistic Regression: {accuracy_score(y_test, logistic_pred):.2%}")
print(f"XGBoost:             {accuracy_score(y_test, xgb_pred):.2%}")