from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator 

from app.core.config import settings

# Асинхронный клиент из databases — для простых асинхронных запросов
database = Database(settings.DATABASE_URL)

# Синхронный движок для Alembic и метаданных 
engine = create_engine(settings.DATABASE_URL.replace('asyncpg', 'psycopg2'))

metadata = MetaData()

# Асинхронный движок SQLAlchemy ORM
async_engine = create_async_engine(settings.DATABASE_URL, echo=True)

# Асинхронный сессионный мейкер
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс моделей для ORM
Base = declarative_base()

# Депенденси для FastAPI — генератор сессии
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:

    async with async_session_maker() as session:
        yield session
