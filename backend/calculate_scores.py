from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        c.id,
        c.symbol,
        t.date,
        t.rsi_14,
        t.macd,
        t.sma_20,
        t.sma_50,
        p.close
    FROM companies c
    JOIN technical_indicators t ON c.id = t.company_id
    JOIN prices p
        ON c.id = p.company_id
        AND t.date = p.date
    WHERE c.symbol = 'RELIANCE'
    ORDER BY t.date DESC
    LIMIT 1
""")

row = cursor.fetchone()

if not row:
    print("No technical data found.")
    exit()

company_id, symbol, date, rsi, macd, sma20, sma50, close = row

technical_score = 0

if close > sma20:
    technical_score += 1
if close > sma50:
    technical_score += 1
if rsi < 30:
    technical_score += 1
elif rsi > 70:
    technical_score -= 1
if macd > 0:
    technical_score += 1
else:
    technical_score -= 1

if technical_score >= 2:
    recommendation = "Bullish"
elif technical_score <= -2:
    recommendation = "Bearish"
else:
    recommendation = "Neutral"

cursor.execute("""
    INSERT INTO research_scores
    (company_id, score_date, technical_score, recommendation)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (company_id, score_date)
    DO UPDATE SET
        technical_score = EXCLUDED.technical_score,
        recommendation = EXCLUDED.recommendation
""", (
    company_id,
    date,
    technical_score,
    recommendation
))

connection.commit()

print(f"Stock: {symbol}")
print(f"Technical Score: {technical_score}")
print(f"Signal: {recommendation}")

cursor.close()
connection.close()