import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from model import create_db_and_tables
from settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await create_db_and_tables()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan, title=settings.APP_NAME)

@app.get("/")
async def root():
    return {"message": "E-Commerce API Running"}