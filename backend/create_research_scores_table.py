from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS research_scores (
        id SERIAL PRIMARY KEY,
        company_id INTEGER REFERENCES companies(id),
        score_date DATE NOT NULL,
        fundamental_score DECIMAL(5,2),
        technical_score DECIMAL(5,2),
        overall_score DECIMAL(5,2),
        recommendation VARCHAR(50),
        UNIQUE(company_id, score_date)
    )
""")

connection.commit()

cursor.close()
connection.close()

print("Research scores table created successfully!")