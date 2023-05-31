from keyboards.inline.menu_in import check_button_ru
from loader import dp, bot, db
from data.config import CHANNELS
from states.state import Lang
from utils.misc import subscription
from aiogram import types
from keyboards.inline.menu import lang, chek_uz, chek


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    lang1 = await db.show_lang(id=call.from_user.id)
    await call.answer()
    final_status = True
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            final_status *= status
            bot_msg = await db.select_bot_message(code='checker_1')
            result += bot_msg['content'].format(channel=channel)

        else:
            final_status *= False
            invite_link = await channel.export_invite_link()
            if lang1['lang'] == 'uz':
                bot_msg = await db.select_bot_message(code='checker_2')
                await call.message.answer(bot_msg['content'])
                bot_msg = await db.select_bot_message(code='checker_3')
                await call.message.answer(bot_msg['content'].format(invite_link=invite_link, channel=channel) ,disable_web_page_preview=True,
                    reply_markup=chek_uz)
            else:
                bot_msg = await db.select_bot_message(code='checker_4')
                await call.message.answer(bot_msg['content'])

                bot_msg = await db.select_bot_message(code='checker_5')
                await call.message.answer(bot_msg['content'].format(invite_link=invite_link, channel=channel), disable_web_page_preview=True,
                    reply_markup=chek)
    if final_status:
        await call.message.delete()
        bot_msg = await db.select_bot_message(code='checker_6')
        await call.message.answer(bot_msg['content'].format(call=call), reply_markup=lang)
        await Lang.select.set()
    else:
        await call.message.delete()
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=check_button_ru)
