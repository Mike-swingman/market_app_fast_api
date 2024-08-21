from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import select, insert, delete


engine = create_async_engine(settings.DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


class Base(DeclarativeBase):
    model = None

    @classmethod
    async def get_or_none(cls, session, **filter_by):
        query = select(cls.__table__.columns).filter_by(**filter_by)
        result = await session.execute(query)
        return result.mappings().one_or_none()

    @classmethod
    async def add(cls, session, **data):
        try:
            query = insert(cls).values(**data).returning(cls.__table__.columns)
            result = await session.execute(query)
            await session.commit()
            return result.mappings().first()
        except SQLAlchemyError:
            await session.rollback()
            raise Exception("Database Exc: Cannot insert data into table")
        except Exception:
            await session.rollback()
            raise Exception("Unknown Exc: Cannot insert data into table")
