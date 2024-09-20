from datetime import timedelta, timezone, datetime
from sqlalchemy import select, func

from app.database.models import User, Question
from app.database.session import async_session

async def get_user(tg_id: int) -> User:
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))
    

async def get_question(message_id: int) -> Question:
    async with async_session() as session:
        return await session.scalar(select(Question).where(Question.message_id == message_id))
    

async def get_count_users(time: str = 'day') -> list[int]:
    async with async_session() as session:
        # if time == 'day':
        #     return (await session.execute(select(func.count(User)).filter(User.when_reg >= (datetime.now(timezone.utc) - timedelta(days=1))))).scalar()
        counts = []
        counts.append((await session.execute(select(func.count(User.id)).filter(User.when_reg >= (datetime.now(timezone.utc) - timedelta(days=1))))).scalar())
        counts.append((await session.execute(select(func.count(User.id)).filter(User.when_reg >= (datetime.now(timezone.utc) - timedelta(days=30))))).scalar())
        counts.append((await session.execute(select(func.count(User.id)))).scalar())
        return counts
    

async def get_count_questions() -> list[int]:
    async with async_session() as session:
        counts = []
        counts.append((await session.execute(select(func.count(Question.id)).filter(Question.when_reg >= (datetime.now(timezone.utc) - timedelta(days=1))))).scalar())
        counts.append((await session.execute(select(func.count(Question.id)).filter(Question.when_reg >= (datetime.now(timezone.utc) - timedelta(days=30))))).scalar())
        counts.append((await session.execute(select(func.count(Question.id)))).scalar())
        return counts