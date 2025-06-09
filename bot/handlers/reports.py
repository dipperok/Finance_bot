from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from bot.states.add_expense_states import AddExpense
from db.database import BotDB, db_path


db = BotDB(db_path)
router = Router()
