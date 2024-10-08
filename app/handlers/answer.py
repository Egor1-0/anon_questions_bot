from aiogram import F, Router
from aiogram.types import Message

from app.database.queries import get_question
from app.keyboards.inline import send_kb
from app.filters import IsAnswer

answer_router = Router()


@answer_router.message(IsAnswer())
async def bot_answer(message: Message):
    message_reply = message.reply_to_message
    question_obj = (await get_question(message_reply.message_id))
    await message.answer("Ответ отправлен!", reply_markup=send_kb(question_obj.from_user_id))
    await message.bot.send_message(chat_id=question_obj.from_user_id, text=message.text, reply_to_message_id=question_obj.original_message)