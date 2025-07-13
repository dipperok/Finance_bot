from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from db.database import BotDB, db_path
from bot.keyboards import main_menu

router = Router()
db = BotDB(db_path)

@router.message(CommandStart())
async def cmd_start(message: Message):
    if db.user_exists(message.from_user.username):
        if db.get_first_message_status(message.from_user.username):
            await message.answer("Ты есть в базе пользовтелей", reply_markup=main_menu)
        else:
            await message.answer("Ты есть в базе пользовтелей. Перед первым использованием посмотри - https://telegra.ph/Finance-by-d-bot-v10-06-03", reply_markup=main_menu)
    else:
        await message.answer("Тебя нет в базе пользователей. При желании можешь обратиться к создателю бота")