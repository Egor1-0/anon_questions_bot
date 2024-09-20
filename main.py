import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeDefault

from app.database.session import create_table
from app.handlers import main_router
from app.states.state_handlers import main_state
from app.commands import bot_commands
from config import TOKEN


async def main():
    await create_table()
    bot = Bot(token=TOKEN)     
    await bot.set_my_commands(bot_commands)
    dp = Dispatcher()

    dp.include_routers(main_state, main_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass