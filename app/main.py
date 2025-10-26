
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from BOT_TOKEN import TOKEN_PSI
from bot.handlers import start, add_expense, add_profit, user_settings, menu, stats, reports, del_last_record

async def main():
    bot = Bot(TOKEN_PSI)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        add_expense.router,
        add_profit.router,
        user_settings.router,
        menu.router,
        stats.router,
        reports.router,
        del_last_record.router
    )
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())