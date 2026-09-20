from fastapi import FastAPI
from database import get_connection

app = FastAPI(title="AI Stock Research Agent")


@app.get("/")
def home():
    return {"message": "AI Stock Research Agent API is running!"}


@app.get("/db-test")
def database_test():
    connection = get_connection()
    connection.close()
    return {"message": "PostgreSQL connection successful!"}


@app.get("/companies")
def get_companies():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM companies ORDER BY id")
    companies = cursor.fetchall()

    cursor.close()
    connection.close()

    return {"companies": companies}


@app.get("/stock/{symbol}")
def get_stock(symbol: str):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            c.symbol,
            c.company_name,
            c.sector,
            c.current_price,
            t.date,
            t.sma_20,
            t.sma_50,
            t.ema_20,
            t.rsi_14,
            t.macd,
            f.revenue,
            f.net_profit,
            f.eps,
            f.pe_ratio,
            f.debt_to_equity,
            rs.technical_score,
            rs.recommendation
        FROM companies c
        LEFT JOIN technical_indicators t
            ON c.id = t.company_id
        LEFT JOIN fundamentals f
            ON c.id = f.company_id
        LEFT JOIN research_scores rs
            ON c.id = rs.company_id
            AND rs.score_date = t.date
        WHERE c.symbol = %s
        ORDER BY t.date DESC
        LIMIT 1
    """, (symbol.upper(),))

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if not row:
        return {"error": "Company not found"}

    return {
        "symbol": row[0],
        "company_name": row[1],
        "sector": row[2],
        "current_price": float(row[3]) if row[3] else None,
        "date": str(row[4]),
        "technical": {
            "sma_20": float(row[5]),
            "sma_50": float(row[6]),
            "ema_20": float(row[7]),
            "rsi_14": float(row[8]),
            "macd": float(row[9])
        },
        "fundamentals": {
            "revenue": float(row[10]) if row[10] else None,
            "net_profit": float(row[11]) if row[11] else None,
            "eps": float(row[12]) if row[12] else None,
            "pe_ratio": float(row[13]) if row[13] else None,
            "debt_to_equity": float(row[14]) if row[14] else None
        },
        "research": {
            "technical_score": row[15],
            "recommendation": row[16]
        }
    }