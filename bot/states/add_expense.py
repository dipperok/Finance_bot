from aiogram.fsm.state import StatesGroup, State

class AddExpense(StatesGroup):
    amount = State()
    category = State()