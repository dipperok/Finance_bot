from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_profit_states import AddProfit
from db.database import BotDB, db_path
from bot.keyboards import main_menu


db = BotDB(db_path)
router = Router()

@router.message(lambda msg: msg.text == "➕ Добавить доход")
async def handle_add_income(message: Message, state: FSMContext):
    await message.answer("Введите сумму:")
    await state.set_state(AddProfit.amount)

@router.message(StateFilter(AddProfit.amount), F.text.regexp(r"^\d+(\.\d+)?$"))
async def handle_income_amount(message: Message, state: FSMContext):
    amount = float(message.text)
    db.add_record(message.from_user.username, '+', amount, 'Доход')
    await message.answer(f"Доход {amount}₽ добавлен.", reply_markup=main_menu)
    await state.clear()