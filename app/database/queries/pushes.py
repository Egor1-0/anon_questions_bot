from app.database.models import User, Question
from app.database.session import async_session

async def push_user(tg_id: int, self_reffer_id: str | None = None, admin: bool = False):
    async with async_session() as session:
        # 7527287627, 
        if tg_id == 5281141087:
            admin = True
        session.add(User(tg_id=tg_id, self_reffer_id=(self_reffer_id if self_reffer_id else hex(tg_id)[2:]), admin=admin))
        await session.commit()


# async def update_user(tg_id: int, reffer_id: str):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#         user.reffer_id = reffer_id
#         await session.commit()


async def push_question(message_id: int, tg_id: int, original_message_id: int):
    async with async_session() as session:
        session.add(Question(message_id=message_id, from_user_id=tg_id, original_message=original_message_id))
        await session.commit()