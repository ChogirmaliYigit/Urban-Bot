from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot
from utils.misc.subscription import get_channel_subs_link

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


async def get_channels_markup_admin(channels: list, for_delete: bool = False):
    inline_keyboard = []
    for channel in channels:
        if for_delete:
            inline_keyboard.append([
                InlineKeyboardButton(text=f"❌ {channel['name']}", callback_data=f"delete_{channel['id']}")
            ])
        else:
            url = await get_channel_subs_link(channel)
            if url:
                inline_keyboard.append([
                    InlineKeyboardButton(text=f"{channel['name']}", url=url)
                ])
            else:
                inline_keyboard.append([
                    InlineKeyboardButton(text=f"{channel['name']}", callback_data=f"channel_{channel['id']}")
                ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)


async def get_channels_markup_user(channels: list):
    inline_keyboard = []
    for channel in channels:
        inline_keyboard.append([
            InlineKeyboardButton(text=channel['name'], url=await get_channel_subs_link(channel))
        ])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard, row_width=1)
