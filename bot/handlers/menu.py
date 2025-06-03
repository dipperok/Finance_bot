from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from db.database import BotDB, db_path
from bot.keyboards import main_menu, stats_menu, settings_menu

router = Router()

@router.message(lambda msg: msg.text == "↩ Назад в меню")
async def cmd_start(message: Message):
    await message.answer("Меню:", reply_markup=main_menu)
    
@router.message(lambda msg: msg.text == "📊 Статистика")
async def cmd_start(message: Message):
    await message.answer("Статистика:", reply_markup=stats_menu)
    
@router.message(lambda msg: msg.text == "⚙ Настроки")
async def open_settings(message: Message):
    await message.answer("Настройки:", reply_markup=settings_menu)
