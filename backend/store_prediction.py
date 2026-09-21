from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    INSERT INTO ml_predictions
    (company_id, prediction_date, predicted_return,
     predicted_direction, model_name, confidence)
    VALUES (%s, CURRENT_DATE, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING
""", (
    2,
    0.1096,
    "NEGATIVE",
    "Logistic Regression",
    0.8904
))

connection.commit()

cursor.close()
connection.close()

print("ML prediction stored successfully!")