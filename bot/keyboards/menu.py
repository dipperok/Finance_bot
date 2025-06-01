from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➖ Добавить расход")],
        [KeyboardButton(text="➕ Добавить доход")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="📂 Категории")]
    ],
    resize_keyboard=True
)