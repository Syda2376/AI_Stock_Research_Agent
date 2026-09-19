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