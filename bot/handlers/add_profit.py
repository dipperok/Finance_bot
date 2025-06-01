from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_profit import AddProfit
from db.database import BotDB

db = BotDB('db/db.sqlite')
router = Router()

@router.message(lambda msg: msg.text == "➕ Добавить доход")
async def handle_add_income(message: Message, state: FSMContext):
    await message.answer("Введите сумму:")
    await state.set_state(AddProfit.amount)

@router.message(StateFilter(AddProfit.amount), F.text.regexp(r"^\d+(\.\d+)?$"))
async def handle_income_amount(message: Message, state: FSMContext):
    amount = float(message.text)
    db.add_record(message.from_user.username, '+', amount, 'Доход')
    await message.answer(f"Доход {amount}₽ добавлен.")
    await state.clear()


'''
@router.message(AddProfit.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        return await message.answer("Введите число.")
    
    await state.update_data(amount=amount)
    
    
    
    
@router.callback_query()
async def add_profit(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    db.add_record(callback.from_user.username, '+', amount, 'profit')
    await callback.message.edit_text(f"Доход {amount}{db.get_currency(callback.from_user.username)[0]} добавлен!")
    await callback.answer()
    await state.clear()
'''