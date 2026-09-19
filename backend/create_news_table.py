from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS news (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id),
        published_at TIMESTAMP,
        headline TEXT NOT NULL,
        source VARCHAR(200),
        url TEXT,
        sentiment DECIMAL(5,2)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("News table created successfully!")