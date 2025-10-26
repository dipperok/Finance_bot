from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_profit_states import AddProfit
from bot.keyboards import main_menu

from db.db_postgress import BotDBpg, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
db = BotDBpg(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

router = Router()

@router.message(lambda msg: msg.text == "➕ Добавить доход")
async def handle_add_income(message: Message, state: FSMContext):
    await message.answer("Введите сумму:")
    await state.set_state(AddProfit.amount)

@router.message(StateFilter(AddProfit.amount), F.text.regexp(r"^\d+(\.\d+)?$"))
async def handle_income_amount(message: Message, state: FSMContext):
    amount = float(message.text)
    db.add_record(message.from_user.username, '+', amount, 'Доход')
    await message.answer(f"Доход {amount}{db.get_currency(message.from_user.username)[0]} добавлен.", reply_markup=main_menu)
    await state.clear()