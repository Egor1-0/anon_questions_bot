from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.states.states import Ask
from app.database.queries import get_user, push_user, push_question
from app.keyboards.inline import *
from config import BOT_URL

ask_router = Router()

@ask_router.message(CommandStart())
async def bot_start(message: Message, state: FSMContext):
    if not await get_user(message.from_user.id):
        await push_user(message.from_user.id)
    user = await get_user(message.from_user.id)
    if not len(message.text) > 7:
        await message.answer("🚀 Начни получать анонимные сообщения прямо сейчас!"
                            "\n\nТвоя ссылка:"
                            f"\n{BOT_URL}?start={user.self_reffer_id}"
                            "\n\nРазмести эту ссылку ☝️ в описании профиля Telegram/TikTok/Instagram, чтобы начать получать анонимные сообщения 💬")
    else:
        ref = int(message.text[7:], 16)
        await state.set_state(Ask.ask)
        await state.update_data(ask=ref)
        await message.answer("🚀 Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку"
                             "\n✍️ Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение, но не будет знать от кого"
                             "\nОтправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры", reply_markup=cancel_kb)
        

@ask_router.callback_query(F.data == "cancel")
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.clear()
    await call.message.answer("Отменено!")


@ask_router.message(Ask.ask)
async def bot_ask(message: Message, state: FSMContext):
    ref = (await state.get_data())['ask']
    orig_mes = await message.reply(f"Сообщение отправлено, ожидайте ответ!", reply_markup=send_kb(ref))
    if (await get_user(message.from_user.id)).admin:
        await message.bot.send_message(chat_id=ref, text=f"Вопрос от: {message.from_user.id}, {"@" + message.from_user.username if message.from_user.username else ''}")
    msg = await message.bot.send_message(chat_id=ref, text=f"У тебя новое анонимное сообщение!\n\n{message.text}\n\n↩️ Свайпни для ответа.")
    await push_question(msg.message_id, message.from_user.id, orig_mes.message_id)
    await state.clear()


@ask_router.callback_query(F.data.startswith("send:again_"))
async def cancel(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(Ask.ask)
    await state.update_data(ask=int(call.data.split("_")[1]))
    await call.message.answer("🚀 Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку"
                            "\n✍️ Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше сообщение, но не будет знать от кого"
                            "\nОтправить можно фото, видео, 💬 текст, 🔊 голосовые, 📷 видеосообщения (кружки), а также ✨ стикеры", reply_markup=cancel_kb)