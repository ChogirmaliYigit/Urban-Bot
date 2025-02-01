from typing import Union
from loader import bot, db


async def check(user_id, channel: Union[int, str]):
    member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return member.is_chat_member()


async def get_user_subscribe_channels(chat_ids, user_id):
    subcribe_channels = []
    for chat_id in chat_ids:
        is_member = await check(user_id, chat_id)
        if not is_member:
            channel = await db.select_channel(chat_id=chat_id)
            if channel:
                subcribe_channels.append(channel)
    return subcribe_channels
