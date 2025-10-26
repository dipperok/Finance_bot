from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from bot.keyboards import main_menu
from db.db_postgress import BotDBpg, DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

db = BotDBpg(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    if db.user_exists(message.from_user.username):
        if db.get_first_message_status(message.from_user.username):
            await message.answer("Ты есть в базе пользовтелей", reply_markup=main_menu)
        else:
            await message.answer("Ты есть в базе пользовтелей. Перед первым использованием посмотри - https://telegra.ph/Finance-by-d-bot-v10-06-03", reply_markup=main_menu)
    else:
        await message.answer("Тебя нет в базе пользователей. При желании можешь обратиться к создателю бота")