import pandas as pd

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

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

print("\nTraining period:")
print(df["date"].iloc[0], "to", df["date"].iloc[split_index - 1])

print("\nTesting period:")
print(df["date"].iloc[split_index], "to", df["date"].iloc[-1])