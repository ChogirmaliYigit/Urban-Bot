from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

yesno = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Да', callback_data='yes')],
        [InlineKeyboardButton(text='Нет', callback_data='no')]
    ]
)

check_button_uz = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="✔️ Obunani tekshirish", callback_data="check_subs")
    ]]
)

check_button_ru = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="✔️ Проверить подписку", callback_data="check_subs")
    ]]
)


def get_channels_markup_admin(channels: list):
    inline_keyboard = []
    for channel in channels:
        inline_keyboard.append([
            InlineKeyboardButton(text=f"❌ {channel['name']}", callback_data=f"delete_{channel['id']}")
        ])
    inline_keyboard.append([
        InlineKeyboardButton(text="Kanal qo'shish", callback_data="add_channel"),
    ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)


def get_channels_markup_user(channels: list):
    inline_keyboard = []
    for channel in channels:
        inline_keyboard.append([
            InlineKeyboardButton(text=channel['name'], url=channel["link"])
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)
