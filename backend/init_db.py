from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS companies (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(20) UNIQUE NOT NULL,
        company_name VARCHAR(200) NOT NULL,
        sector VARCHAR(100),
        current_price DECIMAL(12,2)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("Companies table created successfully!")