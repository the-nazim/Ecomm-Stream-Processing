import asyncio
from fastapi import FastAPI
from . model import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
async def startup():
    await create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "E-Commerce API Running"}