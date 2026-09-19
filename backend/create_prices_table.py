from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id),
        date DATE NOT NULL,
        open DECIMAL(12,2),
        high DECIMAL(12,2),
        low DECIMAL(12,2),
        close DECIMAL(12,2),
        volume BIGINT,
        UNIQUE(company_id, date)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("Prices table created successfully!")