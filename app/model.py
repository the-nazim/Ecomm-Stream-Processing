from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, DECIMAL, func
from sqlalchemy.orm import sessionmaker
import os

DATABASE = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE)
Base = declarative_base()
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(256), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    price = Column(DECIMAL(10, 2))
    category = Column(String(100))
    stock = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

