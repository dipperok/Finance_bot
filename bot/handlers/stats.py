from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_expense_states import AddExpense
from db.database import BotDB, db_path
from bot.keyboards import stats_menu
from datetime import datetime
from dateutil.relativedelta import relativedelta

router = Router()
db = BotDB(db_path)


@router.message(lambda msg: msg.text == "📊 Статистика за прошлый месяц")
async def cmd_start(message: Message):
    last_month = (datetime.now() - relativedelta(months=1)).strftime('%m.%Y')
    stats_this_mounth = db.get_all_user_stat(message.from_user.username, last_month, last_month)
    categories = '\n'.join([f"{key}: {value}" for key, value in stats_this_mounth[2].items()])
    
    await message.answer(f'Статистика за этот месяц:\nДоходы: {stats_this_mounth[0]}\nРасходы: {stats_this_mounth[1]}\n\nРасходы по категориями:\n{categories}')

@router.message(lambda msg: msg.text == "📈 Статистика за этот месяц")
async def cmd_start(message: Message):
    this_mounth = datetime.now().strftime('%m.%Y')
    stats_this_mounth = db.get_all_user_stat(message.from_user.username, this_mounth, this_mounth)
    categories = '\n'.join([f"{key}: {value}" for key, value in stats_this_mounth[2].items()])
    
    await message.answer(f'Статистика за этот месяц:\nДоходы: {stats_this_mounth[0]}\nРасходы: {stats_this_mounth[1]}\n\nРасходы по категориями:\n{categories}')
    
@router.message(lambda msg: msg.text == "📋 Статистика за всё время")
async def cmd_start(message: Message):
    all_period = db.get_all_period(message.from_user.username)
    stats_this_mounth = db.get_all_user_stat(message.from_user.username, all_period[0], all_period[1])
    categories = '\n'.join([f"{key}: {value}" for key, value in stats_this_mounth[2].items()])
    
    await message.answer(f'Статистика за этот месяц:\nДоходы: {stats_this_mounth[0]}\nРасходы: {stats_this_mounth[1]}\n\nРасходы по категориями:\n{categories}')


@router.message(lambda msg: msg.text == "📅 Статистика за период")
async def cmd_start(message: Message):
    pass



'''
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
    
    await callback.message.edit_text(f"Расход {amount}{db.get_currency(callback.from_user.username)[0]} на '{category}' добавлен!")
    await callback.answer()
    await state.clear()
'''