from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from bot.handlers import start, add_expense

async def main():
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        add_expense.router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())