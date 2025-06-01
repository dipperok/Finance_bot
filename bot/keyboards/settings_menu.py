from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="↩ Назад в меню")],
        [KeyboardButton(text="🛒 Категории")],
        [KeyboardButton(text="💵 Влюта")],
        [KeyboardButton(text="🔓 Премиум")],
        [KeyboardButton(text="🗑 Удалить мои данные")]
    ],
    resize_keyboard=True
)