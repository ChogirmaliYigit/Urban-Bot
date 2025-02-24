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


async def get_channel_subs_link(channel: dict):
    link = str(channel["link"])
    url = None
    if link.startswith("@"):
        url = "https://t.me/" + link[1:]
    elif link[1:].isdigit():
        chat = await bot.get_chat(link)
        if chat.active_usernames:
            url = "https://t.me/" + chat.active_usernames[0]
        else:
            invite_link = await chat.create_invite_link()
            url = invite_link.invite_link
    else:
        url = link
    return url
