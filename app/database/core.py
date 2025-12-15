from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.database.config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


engine = create_async_engine(
    DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://"
    ),
    pool_pre_ping=True,
    connect_args={
        "ssl": "require"
    },
)

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