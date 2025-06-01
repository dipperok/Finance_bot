from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_category_keyboard(categories):
    buttons = [
        [InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}")]
        for cat in categories
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)