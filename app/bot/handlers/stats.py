from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_expense_states import AddExpense
from db.database import BotDB, db_path
from bot.keyboards import stats_menu
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO

router = Router()
db = BotDB(db_path)

mouth_dict = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 
    7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

def num_to_mouth(num):
    if num == 0:
        num = 12
    return mouth_dict[num]

@router.message(lambda msg: msg.text == "📊 Статистика за прошлый месяц")
async def cmd_start(message: Message):
    currency = db.get_currency(message.from_user.username)[0]
    last_month = (datetime.now() - relativedelta(months=1)).strftime('%m.%Y')
    stats_this_month = db.get_all_user_stat(message.from_user.username, last_month, last_month)

    if not stats_this_month:
        await message.answer("Статистика не найдена.")
        return

    incomes, expenses, categories_data = stats_this_month

    def format_number(n: int) -> str:
        return "{:,}".format(n).replace(",", " ")

    categories_text = '\n'.join(
        f"*{key}*: `{format_number(value)}{currency}`" for key, value in categories_data.items()
    )

    await message.answer(
        f'*Статистика за {num_to_mouth(int(datetime.now().strftime('%m'))-1)}*\n'
        f'*Доходы*: `{format_number(incomes)}{currency}`\n'
        f'*Расходы*: `{format_number(expenses)}{currency}`\n\n'
        f'*Расходы по категориям:*\n{categories_text}',
        parse_mode="Markdown")


@router.message(lambda msg: msg.text == "📈 Статистика за этот месяц")
async def cmd_start(message: Message):
    currency = db.get_currency(message.from_user.username)[0]
    this_month = datetime.now().strftime('%m.%Y')
    stats_this_month = db.get_all_user_stat(message.from_user.username, this_month, this_month)

    if not stats_this_month:
        await message.answer("Статистика не найдена.")
        return

    incomes, expenses, categories_data = stats_this_month

    def format_number(n: int) -> str:
        return "{:,}".format(n).replace(",", " ")

    categories_text = '\n'.join(
        f"*{key}*: `{format_number(value)}{currency}`" for key, value in categories_data.items()
    )

    await message.answer(
        f'*Статистика за {num_to_mouth(int(datetime.now().strftime('%m')))}:*\n'
        f'*Доходы*: `{format_number(incomes)}{currency}`\n'
        f'*Расходы*: `{format_number(expenses)}{currency}`\n\n'
        f'*Расходы по категориям:*\n{categories_text}',
        parse_mode="Markdown")


@router.message(lambda msg: msg.text == "📋 Статистика за всё время")
async def cmd_start(message: Message):
    currency = db.get_currency(message.from_user.username)[0]
    all_period = db.get_all_period(message.from_user.username)
    stats_this_month = db.get_all_user_stat(message.from_user.username, all_period[0], all_period[1])

    if not stats_this_month:
        await message.answer("Статистика не найдена.")
        return

    incomes, expenses, categories_data = stats_this_month

    def format_number(n: int) -> str:
        return "{:,}".format(n).replace(",", " ")

    categories_text = '\n'.join(
        f"*{key}*: `{format_number(value)}{currency}`" for key, value in categories_data.items()
    )

    await message.answer(
        f'*Статистика за всё время:*\n'
        f'*Доходы*: `{format_number(incomes)}{currency}`\n'
        f'*Расходы*: `{format_number(expenses)}{currency}`\n\n'
        f'*Расходы по категориям:*\n{categories_text}',
        parse_mode="Markdown")


@router.message(lambda msg: msg.text == "📅 Статистика за период")
async def cmd_start(message: Message):
    pass