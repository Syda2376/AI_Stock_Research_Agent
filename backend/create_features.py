import pandas as pd
from database import get_connection

connection = get_connection()

query = """
SELECT
    p.date,
    p.close,
    p.volume,
    t.sma_20,
    t.sma_50,
    t.ema_20,
    t.rsi_14,
    t.macd,
    f.revenue,
    f.net_profit,
    f.eps,
    f.pe_ratio,
    f.debt_to_equity
FROM prices p
JOIN technical_indicators t
    ON p.company_id = t.company_id
    AND p.date = t.date
LEFT JOIN fundamentals f
    ON p.company_id = f.company_id
WHERE p.company_id = 2
ORDER BY p.date
"""

df = pd.read_sql(query, connection)
connection.close()

df = df.dropna()

df.to_csv("data/reliance_features.csv", index=False)

print("Feature dataset created!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(df.head())