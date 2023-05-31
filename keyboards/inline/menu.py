from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

lang = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Русский 🇷🇺', callback_data='ru'),
         InlineKeyboardButton(text="O'zbekcha 🇺🇿", callback_data='uz')]
    ]
)


chek = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Проверить',callback_data='chekker')]
    ]
)

chek_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Tasdiqlash',callback_data='chekker')]
    ]
)