from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.database.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession,
    expire_on_commit=False
    )

Base = declarative_base()


async def get_db():
    session = AsyncSessionLocal()
    async with session.begin():
        try:
            yield session
        finally:
            await session.close()