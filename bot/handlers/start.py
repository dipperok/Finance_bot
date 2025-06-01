from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from db.database import BotDB
from bot.keyboards.menu import main_menu

router = Router()
db = BotDB('db/db.sqlite')

@router.message(CommandStart())
async def cmd_start(message: Message):
    if db.user_exists(message.from_user.username):
        await message.answer("Привет! Ты есть в базе пользовтелей. Использую /info или меню", reply_markup=main_menu)
    else:
        await message.answer("Привет! Тебя нет в базе пользователей. При желании можешь обратиться к создателю - @dipperok")