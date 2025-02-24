import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from data.config import CHANNELS
from keyboards.inline.menu_in import get_channels_markup_user
from loader import db
from utils.misc.subscription import get_user_subscribe_channels


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            if update.message.text in ['/start', ]:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data in ['check_subs', ]:
                return
        else:
            return

        logging.info(user)
        lang = await db.show_lang(id=user)

        channels = await db.select_all_channels()
        channel_ids = {int(CHANNELS[0])}
        for channel in channels:
            channel_ids.add(int(channel["chat_id"]))

        subscribe_channels = await get_user_subscribe_channels(channel_ids, user)
        if subscribe_channels:
            bot_msg = await db.select_bot_message(code=f"subscribe_these_channels_{lang['lang'] if lang else 'ru'}")
            await update.message.answer(
                text=bot_msg["content"] if bot_msg else "Пожалуйста, подпишитесь на эти каналы",
                reply_markup=await get_channels_markup_user(subscribe_channels, lang['lang'] if lang else 'ru')
            )
            raise CancelHandler()
