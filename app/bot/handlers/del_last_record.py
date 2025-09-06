from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_profit_states import AddProfit
from db.database import BotDB, db_path


db = BotDB(db_path)
router = Router()

@router.message(lambda msg: msg.text == "🗑 Удалить последнюю запись")
async def handle_add_income(message: Message, state: FSMContext):
    if db.del_last_record(message.from_user.username):
        await message.answer("Последняя запись удалена")
    else:
        await message.answer("Последняя запись не найдена")
