from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ml_predictions (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id),
        prediction_date DATE NOT NULL,
        predicted_return DECIMAL(8,4),
        predicted_direction VARCHAR(20),
        model_name VARCHAR(100),
        confidence DECIMAL(5,2)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("ML predictions table created successfully!")