import datetime
import re
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import get_start_link
from data.config import CHANNELS
from keyboards.default.menu import contact_uz, contact_ru
from keyboards.inline.menu import chek, chek_uz
from loader import db
from loader import dp, bot
from states.state import Lang, UserInfo, Chek


@dp.callback_query_handler(state=Lang.select)
async def select_lang(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    text = call.data
    channel_name = await bot.get_chat(CHANNELS[0])
    channelname = (channel_name.active_usernames)
    bot_info = await db.bot_info()
    await db.update_lang(lang=text, telegram_id=call.from_user.id)
    user_channel_status = await bot.get_chat_member(chat_id=f'@{channelname[0]}', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        lang = await db.show_lang(id=call.from_user.id)
        if lang['lang'] == 'uz':
            bot_msg = await db.select_bot_message(code='select_lang')
            await call.answer(bot_msg['content'])
            if bot_info[0]['contest'] == True:
                bot_msg = await db.select_bot_message(code='select_lang_1')
                await call.message.answer(bot_msg['content'])

                bot_msg = await db.select_bot_message(code='select_lang_2')
                await call.message.answer(bot_msg['content'],
                    reply_markup=contact_uz)
                await UserInfo.phone.set()
            else:
                bot_msg = await db.select_bot_message(code='select_lang_3')
                await call.message.answer(bot_msg['content'])
                await state.finish()

        else:
            bot_msg = await db.select_bot_message(code='select_lang_4')
            await call.answer(bot_msg['content'])
            if bot_info[0]['contest'] == True:
                bot_msg = await db.select_bot_message(code='select_lang_5')
                await call.message.answer(bot_msg['content'])

                bot_msg = await db.select_bot_message(code='select_lang_6')
                await call.message.answer(bot_msg['content'],
                                          reply_markup=contact_ru)
                await UserInfo.phone.set()

            else:
                bot_msg = await db.select_bot_message(code='select_lang_7')
                await call.message.answer(bot_msg['content'])
                await state.finish()

    else:
        lang = await db.show_lang(id=call.from_user.id)
        channel = await bot.get_chat(CHANNELS[0])
        invite_link = await channel.export_invite_link()
        if lang['lang'] == 'uz':
            bot_msg = await db.select_bot_message(code='select_lang_8')
            await call.message.answer(bot_msg['content'])
            bot_msg = await db.select_bot_message(code='select_lang_9')
            await call.message.answer(bot_msg['content'].format(channel_username=channel.username, channel_title=channel.title, invite_link=invite_link), disable_web_page_preview=True,
                reply_markup=chek_uz)
        else:
            bot_msg = await db.select_bot_message(code='select_lang_10')
            await call.message.answer(bot_msg['content'])
            bot_msg = await db.select_bot_message(code='select_lang_11')
            await call.message.answer(bot_msg['content'].format(channel_username=channel.username, channel_title=channel.title, invite_link=invite_link), disable_web_page_preview=True,
                reply_markup=chek)
        await Chek.chek.set()


@dp.message_handler(content_types=['contact'], state=UserInfo.phone)
async def get_contact(message: types.Message, state: FSMContext):
    phone = message.contact['phone_number']
    num = "^[\+\]{1,2}?[(]?[998]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    lang = await db.show_lang(id=message.from_user.id)
    if lang['lang'] == 'uz':
        if re.match(num, phone):
            await state.update_data(
                {'phone': phone}
            )
            bot_msg = await db.select_bot_message(code='get_contact')
            await message.answer(bot_msg['content'], reply_markup=ReplyKeyboardRemove())
            await UserInfo.name.set()
        else:
            await db.get_bat(id=message.from_user.id, ban=False)
            bot_msg = await db.select_bot_message(code='get_contact_1')
            await message.answer(bot_msg['content'])
            await state.finish()
    else:
        if re.match(num, phone):
            await state.update_data(
                {'phone': phone}
            )
            bot_msg = await db.select_bot_message(code='get_contact_2')
            await message.answer(bot_msg['content'], reply_markup=ReplyKeyboardRemove())
            await UserInfo.name.set()
        else:
            await db.get_bat(id=message.from_user.id, ban=False)
            bot_msg = await db.select_bot_message(code='get_contact_3')
            await message.answer(bot_msg['content'])
            await state.finish()


@dp.message_handler(state=UserInfo.name)
async def name_add(message: types.Message, state: FSMContext):
    name = message.text
    lang = await db.show_lang(id=message.from_user.id)

    if name.isalpha():
        if lang['lang'] == 'uz':
            bot_msg = await db.select_bot_message(code='name_add')
            await message.answer(bot_msg['content'], reply_markup=ReplyKeyboardRemove())

        else:
            bot_msg = await db.select_bot_message(code='name_add_1')
            await message.answer(bot_msg['content'], reply_markup=ReplyKeyboardRemove())
        await state.update_data(
            {'name': name}
        )
        await UserInfo.birthday.set()
    else:
        if lang['lang'] == 'ru':
            bot_msg = await db.select_bot_message(code='name_add_2')
            await message.answer(bot_msg['content'])
        else:
            bot_msg = await db.select_bot_message(code='name_add_3')
            await message.answer()
        await UserInfo.name.set()


@dp.message_handler(state=UserInfo.birthday)
async def finaly(message: types.Message, state: FSMContext):
    date_reg = "(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\\4(?:(?:1[6-9]|[2-9]\d)?\d{2})"
    date_text = message.text
    link = await get_start_link(str(message.from_user.id), encode=True)
    lang = await db.show_lang(id=message.from_user.id)

    if re.match(date_reg, date_text):
        data = await state.get_data()
        name = data.get('name')
        phone = data.get('phone')
        date_text = date_text.replace('.', '-')
        date_text = date_text.replace('/', '-')
        date_text = date_text.split('-')
        payload = data.get('payload')
        if int(date_text[2]) <= datetime.datetime.now().year and int(date_text[2]) >= 1900:
            try:
                try:
                    if int(payload) != message.from_user.id:
                        await db.add_count(tg_id=int(payload))
                        count = await db.select_user(id=int(payload))
                        if lang['lang'] == 'uz':
                            bot_msg = await db.select_bot_message(code='finaly')
                            await message.bot.send_message(chat_id=count['id'],
                                                           text=bot_msg['content'].format(count=count))
                            if count['ref_count'] >= 2:
                                bot_msg = await db.select_bot_message(code='finaly_1')
                                await message.bot.send_message(chat_id=count['id'],
                                                               text=bot_msg['content'])
                        else:
                            bot_msg = await db.select_bot_message(code='finaly_2')
                            await message.bot.send_message(chat_id=count['id'],
                                                           text=bot_msg['content'].format(count=count))
                            if count['ref_count'] >= 2:
                                bot_msg = await db.select_bot_message(code='finaly_3')
                                await message.bot.send_message(chat_id=count['id'],
                                                               text=bot_msg['content'])
                    else:
                        bot_msg = await db.select_bot_message(code='finaly_4')
                        await message.answer(bot_msg['content'])

                except TypeError:
                    pass
            except ValueError:
                pass
            date_text = datetime.date(day=int(date_text[0]), month=int(date_text[1]), year=int(date_text[2]))
            await db.user_info(name=str(name), phone=str(phone), birth_day=date_text, tg_id=message.from_user.id)
            if lang['lang'] == 'uz':
                link = await get_start_link(str(message.from_user.id), encode=True)
                bot_msg = await db.select_bot_message(code='finaly_5')
                ref = bot_msg['content'].format(link=link)
                menu_uz = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='Referallar', callback_data='Referallar')],
                        [InlineKeyboardButton(text="🫂 Do'stlaringizni taklif qiling",
                                              url=f"https://telegram.me/share/url?url={ref}")]
                    ]
                )
                bot_msg = await db.select_bot_message(code='finaly_6')
                await message.answer(bot_msg['content'].format(competition_id=lang["competition_id"], link=link), reply_markup=menu_uz)
            else:
                link = await get_start_link(str(message.from_user.id), encode=True)
                bot_msg = await db.select_bot_message(code='finaly_7')
                ref = bot_msg['content'].format(link=link)
                menu_ru = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='Рефералы', callback_data='Рефералы')],
                        [InlineKeyboardButton(text="🫂 Пригласить друзей",
                                              url=f"https://telegram.me/share/url?url={ref}")
                         ]

                    ],
                    resize_keyboard=True,
                    one_time_keyboard=True
                )
                bot_msg = await db.select_bot_message(code='finaly_8')
                await message.answer(bot_msg['content'].format(competition_id=lang["competition_id"], link=link), reply_markup=menu_ru)

            await state.finish()

        else:
            if lang['lang'] == 'uz':
                bot_msg = await db.select_bot_message(code='finaly_9')
                await message.answer(bot_msg['content'].format(datetime=datetime.datetime.now().strftime("%Y-%m-%d")))
            else:
                bot_msg = await db.select_bot_message(code='finaly_10')
                await message.answer(bot_msg['content'].format(datetime=datetime.datetime.now().strftime("%Y-%m-%d")))
            await UserInfo.birthday.set()

    else:
        if lang['lang'] == 'uz':
            bot_msg = await db.select_bot_message(code='finaly_11')
            await message.answer(bot_msg['content'])
        else:
            bot_msg = await db.select_bot_message(code='finaly_12')
            await message.answer(bot_msg['content'])
        await UserInfo.birthday.set()


@dp.callback_query_handler(text='Рефералы')
async def get_ref(call: types.CallbackQuery):
    link = await get_start_link(str(call.from_user.id), encode=True)

    user = await db.select_user(id=call.from_user.id)
    bot_msg = await db.select_bot_message(code='get_ref')
    await call.message.answer(bot_msg['content'].format(ref_count=user["ref_count"], link=link))


@dp.callback_query_handler(text='Referallar')
async def get_ref_uz(call: types.CallbackQuery):
    link = await get_start_link(str(call.from_user.id), encode=True)
    user = await db.select_user(id=call.from_user.id)
    bot_msg = await db.select_bot_message(code='get_ref_uz')
    await call.message.answer(bot_msg['content'].format(ref_count=user["ref_count"], link=link))
