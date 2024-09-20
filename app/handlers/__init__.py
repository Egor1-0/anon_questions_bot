from aiogram import Router

from app.handlers.command_handlers import commands_router
from app.handlers.answer import answer_router

main_router = Router()

main_router.include_routers(commands_router, answer_router)