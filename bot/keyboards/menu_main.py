from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➖ Добавить расход")],
        [KeyboardButton(text="➕ Добавить доход")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⚙ Настроки")]
    ],
    resize_keyboard=True
)