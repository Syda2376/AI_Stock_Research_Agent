from fastapi import FastAPI

app = FastAPI(title="AI Stock Research Agent")


@app.get("/")
def home():
    return {"message": "AI Stock Research Agent API is running!"}