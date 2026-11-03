import logging
import os
from datetime import datetime

import dotenv
from db.models import Payment, User
from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from structures.structures import Answer

dotenv.load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=True)

logger = logging.getLogger(__name__)


async def create_new_user(
    telegram_id: int,
    username: str | None = None,
) -> User | None:

    async with async_session() as session:
        existing_user = await get_user(telegram_id=telegram_id)
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


async def save_payments(answer: Answer, tg_id: int) -> bool:
    try:
        async with async_session() as session:
            for trata in answer.content:
                session.add(
                    Payment(
                        tg_id=tg_id,
                        name=trata.name,
                        amount=trata.amount,
                        category=trata.category,
                        date=trata.date,
                        shop=trata.shop,
                    )
                )
            await session.commit()
        return True
    except SQLAlchemyError as e:
        logger.exception(f"Error saving payments: {e}")
        return False


async def delete_last_payment(tg_id: int) -> bool:
    try:
        async with async_session() as session:
            stmt = (
                select(Payment)
                .where(Payment.tg_id == tg_id)
                .order_by(Payment.date.desc(), Payment.id.desc())
                .limit(1)
            )
            result = await session.execute(stmt)
            last_payment = result.scalars().first()

            if last_payment:
                await session.delete(last_payment)
                await session.commit()
                return True
            else:
                return False
    except SQLAlchemyError as e:
        logger.exception(f"Error deleting last payment: {e}")
        return False


async def delete_all_payments(tg_id: int) -> bool:
    try:
        async with async_session() as session:
            stmt = delete(Payment).where(Payment.tg_id == tg_id)
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount > 0

    except SQLAlchemyError as e:
        logger.exception(f"Error deleting all payments: {e}")
        return False
