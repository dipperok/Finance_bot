from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.BOT_TOKEN import TOKEN
from bot.handlers import start, add_expense, add_profit, user_settings, menu, stats, reports
from bot.bot_status import is_db_test_print
from db.database import db_path

is_db_test_print(db_path)

async def main():
    bot = Bot(TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        add_expense.router,
        add_profit.router,
        user_settings.router,
        menu.router,
        stats.router,
        reports.router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())