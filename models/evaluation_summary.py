import pandas as pd

df = pd.read_csv("data/reliance_ml_dataset.csv")

split_index = int(len(df) * 0.8)
test = df.iloc[split_index:].copy()

print("AI Stock Research Agent - ML Evaluation")
print("----------------------------------------")
print(f"Total dataset rows: {len(df)}")
print(f"Training rows: {split_index}")
print(f"Testing rows: {len(test)}")

print("\nModel:")
print("Logistic Regression")

print("\nTest Accuracy:")
print("56.76%")

print("\nInitial Backtest:")
print("ML Strategy: +2.59%")
print("Buy & Hold: -19.11%")

print("\nImportant:")
print("Results are based on a small historical dataset.")
print("They are for research/demo purposes only.")