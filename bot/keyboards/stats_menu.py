from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

stats_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="↩ Назад в меню")],
        [KeyboardButton(text="📊 Общая статистика")],
        [KeyboardButton(text="📉 Статистика трат")],
        [KeyboardButton(text="📈 Статистика доходов")],
        [KeyboardButton(text="🧾 Отчёты")]
    ],
    resize_keyboard=True
)