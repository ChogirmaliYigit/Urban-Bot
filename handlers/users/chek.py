from handlers.users.start import bot_start
from keyboards.inline.menu_in import get_channels_markup_user
from keyboards.inline.menu import lang
from loader import dp, db
from data.config import CHANNELS
from states.state import Lang
from utils.misc import subscription
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery, state: FSMContext):
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
            reply_markup=await get_channels_markup_user(subscribe_channels, lang1['lang'] if lang1 else 'ru')
        )
        return

    await call.message.delete()
    if not lang1:
        bot_msg = await db.select_bot_message(code='checker_6')
        await call.message.answer(bot_msg['content'].format(call=call), reply_markup=lang)
        await Lang.select.set()
    else:
        await bot_start(message=call.message, state=state)
