from sqlmodel import create_engine, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

async_engine = AsyncEngine(
    create_engine(
    url=Config.DATABASE_URL,
    echo=True
)
)

async def init_db() :
    async with async_engine.begin() as conn :

        await conn.run_sync(SQLModel.metadata.create_all)

Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

async def get_session() -> AsyncGenerator[AsyncSession, None] :
    async with Session() as session :
        yield session