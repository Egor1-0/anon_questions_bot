from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.database.queries import get_question

class IsAnswer(BaseFilter):
    async def __call__(self, message: Message):
        if message.reply_to_message:
            if await get_question(message.reply_to_message.message_id):
                return True
            
        return False