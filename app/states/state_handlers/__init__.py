from aiogram import Router

from app.states.state_handlers.ask import ask_router


main_state = Router()

main_state.include_routers(ask_router)