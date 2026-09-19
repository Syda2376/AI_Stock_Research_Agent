import yfinance as yf
from database import get_connection


symbol = "RELIANCE.NS"

stock = yf.Ticker(symbol)

data = stock.history(period="1y")

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id
    FROM companies
    WHERE symbol = 'RELIANCE'
""")

company_id = cursor.fetchone()[0]

for date, row in data.iterrows():
    cursor.execute("""
        INSERT INTO prices
        (company_id, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (company_id, date) DO NOTHING
    """, (
        company_id,
        date.date(),
        float(row["Open"]),
        float(row["High"]),
        float(row["Low"]),
        float(row["Close"]),
        int(row["Volume"])
    ))

connection.commit()

cursor.close()
connection.close()

print(f"Inserted {len(data)} price records for RELIANCE")