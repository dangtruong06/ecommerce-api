from fastapi import FastAPI
from api.db import core

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello world!"}