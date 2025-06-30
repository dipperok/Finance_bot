from aiogram.fsm.state import StatesGroup, State

class AddExpense(StatesGroup):
    date1 = State()
    date2 = State()