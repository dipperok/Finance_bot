from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_category_keyboard(categories):
    buttons = [
        [InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}")]
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➖ Добавить расход")],
        [KeyboardButton(text="➕ Добавить доход")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⚙ Настроки")]
    ],
    resize_keyboard=True
)

settings_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="↩ Назад в меню")],
        [KeyboardButton(text="🛒 Категории")],
        [KeyboardButton(text="💵 Влюта")],
        [KeyboardButton(text="🗑 Удалить мои данные")]
    ],
    resize_keyboard=True
)

stats_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="↩ Назад в меню")],
        [KeyboardButton(text="🧾 Отчёты")],
        [KeyboardButton(text="📉 Статистика трат")],
        [KeyboardButton(text="📈 Статистика доходов")],
        [KeyboardButton(text="📊 Общая статистика")]
    ],
    resize_keyboard=True
)

reports = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="↩ Назад в меню")],
        [KeyboardButton(text="🧾 Отчёты")],
        [KeyboardButton(text="📉 Статистика трат")],
        [KeyboardButton(text="📊 Общая статистика")],
        [KeyboardButton(text="📈 Статистика доходов")]
    ],
    resize_keyboard=True
)