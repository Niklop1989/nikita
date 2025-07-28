from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,DeclarativeBase

DATABSE_URL = "sqlite+aiosqlite:///./NNNNN.py.db"

engine = create_async_engine(DATABSE_URL, echo=True)

async_session = async_sessionmaker(
    engine, expire_on_commit=False
)
# session = async_session()
# Base = declarative_base()

class Base(DeclarativeBase):
    pass

async def get_session():
    async with async_session() as session:
        yield session

