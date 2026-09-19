import pandas as pd
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator

from database import get_connection


connection = get_connection()

query = """
    SELECT date, open, high, low, close, volume
    FROM prices
    WHERE company_id = (
        SELECT id FROM companies WHERE symbol = 'RELIANCE'
    )
    ORDER BY date
"""

df = pd.read_sql(query, connection)

connection.close()


# Calculate technical indicators
df["sma_20"] = SMAIndicator(
    close=df["close"], window=20
).sma_indicator()

df["sma_50"] = SMAIndicator(
    close=df["close"], window=50
).sma_indicator()

df["ema_20"] = EMAIndicator(
    close=df["close"], window=20
).ema_indicator()

df["rsi_14"] = RSIIndicator(
    close=df["close"], window=14
).rsi()

macd = MACD(close=df["close"])

df["macd"] = macd.macd()


# Store indicators in PostgreSQL
connection = get_connection()
cursor = connection.cursor()

company_id = None

cursor.execute("""
    SELECT id
    FROM companies
    WHERE symbol = 'RELIANCE'
""")

company_id = cursor.fetchone()[0]


for _, row in df.iterrows():

    if pd.isna(row["sma_50"]) or pd.isna(row["rsi_14"]):
        continue

    cursor.execute("""
        INSERT INTO technical_indicators
        (company_id, date, sma_20, sma_50, ema_20, rsi_14, macd)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (company_id, date)
        DO UPDATE SET
            sma_20 = EXCLUDED.sma_20,
            sma_50 = EXCLUDED.sma_50,
            ema_20 = EXCLUDED.ema_20,
            rsi_14 = EXCLUDED.rsi_14,
            macd = EXCLUDED.macd
    """, (
        company_id,
        row["date"],
        row["sma_20"],
        row["sma_50"],
        row["ema_20"],
        row["rsi_14"],
        row["macd"]
    ))


connection.commit()

cursor.close()
connection.close()

print(f"Technical indicators calculated for {len(df)} price records.")