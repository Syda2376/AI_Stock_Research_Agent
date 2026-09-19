from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS technical_indicators (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id),
        date DATE NOT NULL,
        sma_20 DECIMAL(12,2),
        sma_50 DECIMAL(12,2),
        ema_20 DECIMAL(12,2),
        rsi_14 DECIMAL(12,2),
        macd DECIMAL(12,2),
        UNIQUE(company_id, date)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("Technical indicators table created successfully!")