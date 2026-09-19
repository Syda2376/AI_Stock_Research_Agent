from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT
        c.symbol,
        t.date,
        p.close,
        t.sma_20,
        t.sma_50,
        t.ema_20,
        t.rsi_14,
        t.macd
    FROM technical_indicators t
    JOIN companies c ON t.company_id = c.id
    JOIN prices p
        ON p.company_id = t.company_id
        AND p.date = t.date
    WHERE c.symbol = 'RELIANCE'
    ORDER BY t.date DESC
    LIMIT 1
""")

data = cursor.fetchone()

cursor.close()
connection.close()


if not data:
    print("No technical data found.")
    exit()


symbol, date, close, sma_20, sma_50, ema_20, rsi, macd = data

score = 0

# Price vs moving averages
if close > sma_20:
    score += 1
else:
    score -= 1

if close > sma_50:
    score += 1
else:
    score -= 1

# RSI
if rsi < 30:
    score += 1
elif rsi > 70:
    score -= 1

# MACD
if macd > 0:
    score += 1
else:
    score -= 1


if score >= 2:
    signal = "Bullish"
elif score <= -2:
    signal = "Bearish"
else:
    signal = "Neutral"


print(f"Stock: {symbol}")
print(f"Date: {date}")
print(f"Close: {close}")
print(f"SMA 20: {sma_20}")
print(f"SMA 50: {sma_50}")
print(f"EMA 20: {ema_20}")
print(f"RSI 14: {rsi}")
print(f"MACD: {macd}")
print(f"Technical Score: {score}")
print(f"Technical Signal: {signal}")