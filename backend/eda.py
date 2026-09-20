import pandas as pd

df = pd.read_csv("data/reliance_features.csv")

print("\n--- Dataset Shape ---")
print(df.shape)

print("\n--- Columns ---")
print(df.columns.tolist())

print("\n--- Missing Values ---")
print(df.isnull().sum())

print("\n--- Statistics ---")
print(df.describe())

print("\n--- Correlation ---")
print(df.corr(numeric_only=True)["close"].sort_values(ascending=False))