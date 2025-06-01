from aiogram import Router
from aiogram.types import Message
from db.database import BotDB
from bot.keyboards.settings_menu import settings_menu

router = Router()
db = BotDB('db/db.sqlite')

@router.message(lambda msg: msg.text == "⚙ Настроки")
async def open_settings(message: Message):
    if db.user_exists(message.from_user.username):
        await message.answer("Настройки:", reply_markup=settings_menu)
    else:
        await message.answer("Тебя нет в базе пользователей. При желании можешь обратиться к создателю - @dipperok")