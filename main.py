from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from BOT_TOKEN import TOKEN
from bot.handlers import start, add_expense, add_profit, user_settings, menu

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        add_expense.router,
        add_profit.router,
        user_settings.router,
        menu.router,
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())