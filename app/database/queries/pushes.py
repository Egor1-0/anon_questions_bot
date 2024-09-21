from sqlalchemy import select

from app.database.models import User, Question
from app.database.session import async_session
from config import MAIN_ADMIN

async def push_user(tg_id: int, self_reffer_id: str | None = None, admin: bool = False):
    async with async_session() as session:
        if tg_id == 5281141087 or tg_id == MAIN_ADMIN:
            admin = True
        session.add(User(tg_id=tg_id, self_reffer_id=(self_reffer_id if self_reffer_id else hex(tg_id)[2:]), admin=admin))
        await session.commit()


async def update_user(tg_id: int, admin: bool):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.admin = admin
        await session.commit()


async def push_question(message_id: int, tg_id: int, original_message_id: int):
    async with async_session() as session:
        session.add(Question(message_id=message_id, from_user_id=tg_id, original_message=original_message_id))
        await session.commit()