import pandas as pd
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

split_index = int(len(df) * 0.8)

test = df.iloc[split_index:].copy()

model = joblib.load("models/model.pkl")

test["prediction"] = model.predict(test[features])

test["strategy_return"] = (
    test["future_return_20d"] * test["prediction"]
)

strategy_return = test["strategy_return"].sum()
buy_hold_return = test["future_return_20d"].sum()

print("Backtest")
print("--------")
print(f"ML Strategy Return: {strategy_return:.2%}")
print(f"Buy & Hold Return:  {buy_hold_return:.2%}")