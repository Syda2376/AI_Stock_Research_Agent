from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    INSERT INTO companies
    (symbol, company_name, sector, current_price)
    VALUES ('RELIANCE', 'Reliance Industries Limited', 'Oil & Gas', NULL)
    ON CONFLICT (symbol) DO NOTHING
""")

connection.commit()

cursor.close()
connection.close()

print("RELIANCE added successfully!")