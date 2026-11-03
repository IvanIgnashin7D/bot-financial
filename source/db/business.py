import os
from datetime import datetime

import dotenv
from db.models import Payment, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

dotenv.load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def create_new_user(
    telegram_id: int,
    username: str | None = None,
) -> User | None:

    async with async_session() as session:
        existing_user = await get_user(telegram_id=telegram_id, session=session)
        if existing_user:
            return None  # User already exists, return None or handle as needed

        new_user = User(
            telegram_id=telegram_id,
            username=username,
            created_at=datetime.now(),
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user


async def get_user(telegram_id: int) -> User | None:
    async with async_session() as session:
        stmt = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def save_payments(payments: list[Payment]) -> bool:
    try:
        async with async_session() as session:
            for payment in payments:
                session.add(payment)
        await session.commit()
        return True
    except Exception:
        return False
