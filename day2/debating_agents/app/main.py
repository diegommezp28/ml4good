from fastapi import FastAPI

app = FastAPI(title="Debating Agents API")


@app.get("/")
async def root():
    return {"message": "Welcome to the Debating Agents API"}
