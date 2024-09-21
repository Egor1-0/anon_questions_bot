from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.database.queries import get_user, get_count_questions, get_count_users, push_user, update_user
from app.filters import IsAdmin
from config import BOT_URL

commands_router = Router()


@commands_router.message(Command("help"))
async def bot_help(message: Message):
    await message.answer("👉 /start - команда запуска бота\n"
                         "👉 /url - узнать мою ссылку")
    

@commands_router.message(Command("url"))
async def bot_url(message: Message):
    user = await get_user(message.from_user.id)
    await message.answer(f"Ваша ссылка👉 {BOT_URL}?start={user.self_reffer_id}")


@commands_router.message(Command("stats"), IsAdmin())
async def bot_stats(message: Message):
    questions = await get_count_questions()
    users = await get_count_users()
    await message.answer(f"Колво юзеров за день: {users[0]}"
                         f"\nКолво юзеров за месяц: {users[1]}"
                         f"\nКолво юзеров всего: {users[2]}"
                         f"\n\nКолво вопросов за день: {questions[0]}"
                         f"\nКолво вопросов за месяц: {questions[1]}"
                         f"\nКолво вопросов всего: {questions[2]}")
    

@commands_router.message(Command("add"), IsAdmin())
async def bot_add_admin(message: Message):
    if not message.text[5:].isdigit():
        await message.answer("Нужно ввести ID")
        return
    user = await get_user(int(message.text[5:]))
    if user:
        await update_user(user.tg_id, admin=True)
    else: 
        await push_user(int(message.text[5:]), admin=True)
    await message.answer("Админ добавлен")
