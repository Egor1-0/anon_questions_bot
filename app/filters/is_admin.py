from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.database.queries import get_user

class IsAdmin(BaseFilter):
    async def __call__(self, message: Message):
        return (await get_user(message.from_user.id)).admin