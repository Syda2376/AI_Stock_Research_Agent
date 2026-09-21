import pandas as pd

df = pd.read_csv("data/reliance_features.csv")

# 20-trading-day future return
df["future_return_20d"] = (
    df["close"].shift(-20) / df["close"] - 1
)

# Target: 1 = positive return, 0 = non-positive return
df["target"] = (df["future_return_20d"] > 0).astype(int)

# Remove the final 20 rows because they don't have future prices
df = df.dropna(subset=["future_return_20d"])

df.to_csv("data/reliance_ml_dataset.csv", index=False)

print("ML dataset created!")
print(f"Rows: {len(df)}")
print(f"Positive targets: {df['target'].sum()}")
print(f"Negative/non-positive targets: {(df['target'] == 0).sum()}")
print("\nTarget distribution:")
print(df["target"].value_counts())