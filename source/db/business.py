import os
from datetime import datetime

import dotenv
from db.models import Payment, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from structures.structures import Answer

dotenv.load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DB_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


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
    except Exception as e:
        print(f"Error saving payments: {e}")
        return False


async def delete_last_payment(tg_id: int) -> bool:
    try:
        async with async_session() as session:
            stmt = (
                select(Payment)
                .where(Payment.tg_id == tg_id)
                .order_by(Payment.date.desc())
            )
            result = await session.execute(stmt)
            last_payment = result.scalars().first()

            if last_payment:
                print("FOUND")
                await session.delete(last_payment)
                await session.commit()
                return True
            else:
                print("NOT FOUND")
                return False
    except Exception as e:
        print(f"EXCEPTION: {e}")
        return False


async def delete_all_payments(tg_id: int) -> bool:
    try:
        async with async_session() as session:
            stmt = select(Payment).where(Payment.tg_id == tg_id)
            result = await session.execute(stmt)
            payments_to_delete = result.scalars().all()

            if payments_to_delete:
                for payment in payments_to_delete:
                    await session.delete(payment)
                await session.commit()
                return True
            else:
                return False
    except Exception:
        return False
