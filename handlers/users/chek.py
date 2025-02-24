from keyboards.inline.menu_in import get_channels_markup_user
from loader import dp, db
from data.config import CHANNELS
from states.state import Lang
from utils.misc import subscription
from aiogram import types


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    lang1 = await db.show_lang(id=call.from_user.id)
    await call.answer()
    channels = await db.select_all_channels()
    channel_ids = {int(CHANNELS[0])}
    for channel in channels:
        channel_ids.add(int(channel["chat_id"]))

    subscribe_channels = await subscription.get_user_subscribe_channels(channel_ids, call.from_user.id)
    if subscribe_channels:
        bot_msg = await db.select_bot_message(code=f"subscribe_these_channels_{lang1['lang'] if lang1 else 'ru'}")
        await call.message.answer(
            text=bot_msg["content"] if bot_msg else "Пожалуйста, подпишитесь на эти каналы",
            reply_markup=get_channels_markup_user(subscribe_channels)
        )
        return

    await call.message.delete()
    bot_msg = await db.select_bot_message(code='checker_6')
    await call.message.answer(bot_msg['content'].format(call=call), reply_markup=lang1)
    await Lang.select.set()
