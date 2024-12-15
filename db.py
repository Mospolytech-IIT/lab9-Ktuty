from bestconfig import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import MetaData, create_engine
from fastapi import Depends
from typing import Annotated, AsyncGenerator
from sqlalchemy.orm import registry

mapper_registry = registry()
metadata_obj = MetaData()

config = Config(".env")
engine = create_async_engine(config.get("DB_URL"))

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        yield session