# main.py
from get_data import all_data

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"data": all_data}

