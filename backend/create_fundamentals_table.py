from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS fundamentals (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id),
        report_date DATE NOT NULL,
        revenue DECIMAL(18,2),
        net_profit DECIMAL(18,2),
        eps DECIMAL(12,2),
        pe_ratio DECIMAL(12,2),
        debt_to_equity DECIMAL(12,2),
        roe DECIMAL(12,2),
        UNIQUE(company_id, report_date)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("Fundamentals table created successfully!")