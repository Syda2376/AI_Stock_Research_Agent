from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    INSERT INTO companies
    (symbol, company_name, sector, current_price)
    VALUES ('TCS', 'Tata Consultancy Services', 'Information Technology', 3500)
""")

connection.commit()

cursor.close()
connection.close()

print("Company added successfully!")