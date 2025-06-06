from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_expense_states import AddExpense
from db.database import BotDB, db_path
from bot.keyboards import get_category_keyboard
from bot.keyboards import main_menu


db = BotDB(db_path)
router = Router()

@router.message(lambda msg: msg.text == "➖ Добавить расход")
async def handle_add_button(message: Message, state: FSMContext):
    await message.answer("Введите сумму:")
    await state.set_state(AddExpense.amount)
    
@router.message(AddExpense.amount)
async def get_amount(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
    except ValueError:
        return await message.answer("Введите число.")
    
    await state.update_data(amount=amount)
    await message.answer("Выберите категорию:", reply_markup=get_category_keyboard(db.get_categories(message.from_user.username)))
    await state.set_state(AddExpense.category)

@router.callback_query(StateFilter(AddExpense.category))
async def category_chosen(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data.get("amount")
    category = callback.data.replace("cat_", "")
    
    db.add_record(callback.from_user.username, '-', amount, category)
    
    await callback.message.edit_text(f"Расход {amount}{db.get_currency(callback.from_user.username)[0]} на '{category}' добавлен!", reply_markup=main_menu)
    await callback.answer()
    await state.clear()
