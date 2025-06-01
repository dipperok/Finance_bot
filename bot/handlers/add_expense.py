from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.states.add_expense import AddExpense
from db.database import BotDB

db = BotDB('db.sqlite')
router = Router()

@router.message(Command("add"))
async def start_add(message: Message, state: FSMContext):
    await message.answer("Введи сумму:")
    await state.set_state(AddExpense.amount)

@router.message(AddExpense.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        return await message.answer("Введите число.")
    await state.update_data(amount=amount)
    await message.answer("Введите категорию:")
    await state.set_state(AddExpense.category)

@router.message(AddExpense.category)
async def get_category(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    category = message.text
    await db.add_record(message.from_user.id, amount, category)
    await message.answer(f"Расход {amount}₽ на '{category}' добавлен!")
    await state.clear()