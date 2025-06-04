from aiogram.fsm.state import StatesGroup, State


class AddProfit(StatesGroup):
    amount = State()