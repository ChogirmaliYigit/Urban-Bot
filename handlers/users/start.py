import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link, decode_payload
from data.config import ADMINS, CHANNELS
from keyboards.default.menu import admin_key, contact_uz, contact_ru
from keyboards.inline.menu import lang, chek, chek_uz
from loader import db, bot
from loader import dp
from states.state import Lang, Chek, UserInfo


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message, state: FSMContext):
    bot_msg = await db.select_bot_message(code='bot_start')
    try:
        await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            ref_count=0,
            parent=None,
            birth_day=None,
            lang='ru',
            phone=None,
            name2='ADMIN',
            ban=True
        )
        await message.answer(bot_msg['content'], reply_markup=admin_key)
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer(bot_msg['content'], reply_markup=admin_key)
    await state.finish()


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    bot_info = await db.bot_info()
    lang_db = await db.show_lang(id=message.from_user.id)

    if bot_info[0]['contest'] == True:

        channel_name = await bot.get_chat(CHANNELS[0])
        channelname = (channel_name.active_usernames)
        user_channel_status = await bot.get_chat_member(chat_id=f'@{channelname[0]}',
                                                        user_id=message.from_user.id)

        user_where = await db.select_user(id=message.from_user.id)
        args = message.get_args()
        try:
            payload = decode_payload(args)
        except:
            payload = None
        await state.update_data(
            {'payload': payload}
        )
        try:
            try:
                payload = int(payload)
            except TypeError:
                payload = None
        except ValueError:
            payload = None
        bot_msg = await db.select_bot_message(code='bot_start_1')
        try:
            await db.add_user(
                telegram_id=message.from_user.id,
                full_name=message.from_user.full_name,
                username=message.from_user.username,
                ref_count=0,
                parent=payload,
                birth_day=None,
                lang=None,
                phone=None,
                name2='',
                ban=True
            )
            await message.answer(bot_msg['content'], reply_markup=lang)
            await Lang.select.set()
        except asyncpg.exceptions.UniqueViolationError:
            if user_where['ban'] != False:
                if user_where['birth_day'] == None:
                    await db.delete_user(id=message.from_user.id)
                    await db.add_user(
                        telegram_id=message.from_user.id,
                        full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        ref_count=0,
                        parent=payload,
                        birth_day=None,
                        lang=None,
                        phone=None,
                        name2='',
                        ban=True
                    )
                    await message.answer(bot_msg['content'], reply_markup=lang)
                    await Lang.select.set()
                else:
                    if user_channel_status["status"] != 'left':
                        if lang_db['lang'] == 'uz' and lang_db['ban'] != False:
                            link = await get_start_link(str(message.from_user.id), encode=True)
                            bot_msg = await db.select_bot_message(code='bot_start_2')
                            ref = bot_msg['content'].format(link=link)
                            menu_uz = InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [InlineKeyboardButton(text='Referallar', callback_data='Referallar')],
                                    [InlineKeyboardButton(text="🫂 Do'stlaringizni taklif qiling",
                                                          url=f"https://telegram.me/share/url?url={ref}")]
                                ]
                            )
                            bot_msg = await db.select_bot_message(code='bot_start_3')
                            await message.answer(bot_msg['content'].format(full_name=message.from_user.full_name, competition_id=lang_db["competition_id"]), reply_markup=menu_uz)
                        elif lang_db['lang'] == 'ru' and lang_db['ban'] != False:
                            link = await get_start_link(str(message.from_user.id), encode=True)
                            bot_msg = await db.select_bot_message(code='bot_start_4')
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
                            bot_msg = await db.select_bot_message(code='bot_start_5')
                            await message.answer(bot_msg['content'].format(full_name=message.from_user.full_name, competition_id=lang_db["competition_id"]), reply_markup=menu_ru)
                    else:
                        channel = await bot.get_chat(CHANNELS[0])
                        invite_link = await channel.export_invite_link()
                        if lang_db['lang'] == 'uz':
                            bot_msg = await db.select_bot_message(code='bot_start_6')
                            await message.answer(bot_msg['content'].format(invite_link=invite_link, channel_username=channel.username, channel_title=channel.title), reply_markup=chek_uz,
                                disable_web_page_preview=True)
                        else:
                            bot_msg = await db.select_bot_message(code='bot_start_7')
                            await message.answer(bot_msg['content'].format(invite_link=invite_link, channel_username=channel.username, channel_title=channel.title), reply_markup=chek,
                                disable_web_page_preview=True)
                        await Chek.chek.set()
            else:
                bot_msg = await db.select_bot_message(code='bot_start_8')
                await message.answer(bot_msg['content'])
                await state.finish()
    else:
        try:
            if lang_db['lang'] == 'ru':
                bot_msg = await db.select_bot_message(code='bot_start_9')
                await message.answer(bot_msg['content'])
            elif lang_db['lang'] == 'uz':
                bot_msg = await db.select_bot_message(code='bot_start_10')
                await message.answer(bot_msg['content'])
        except TypeError:
            bot_msg = await db.select_bot_message(code='bot_start_11')
            await message.answer(bot_msg['content'])


@dp.callback_query_handler(text='chekker', state=Chek.chek)
async def chek_1(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    channel_name = await bot.get_chat(CHANNELS[0])
    channelname = (channel_name.active_usernames)
    lang1 = await db.show_lang(id=call.from_user.id)
    user_channel_status = await bot.get_chat_member(chat_id=f'@{channelname[0]}', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        if call.from_user.id == lang1['id'] and lang1['birth_day'] != None:
            if lang1['lang'] == 'uz' and lang1['ban'] != False:
                link = await get_start_link(str(call.from_user.id), encode=True)
                bot_msg = await db.select_bot_message(code='chek_1')
                ref = bot_msg['content'].format(link=link)
                menu_uz = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text='Referallar', callback_data='Referallar')],
                        [InlineKeyboardButton(text="🫂 Do'stlaringizni taklif qiling",
                                              url=f"https://telegram.me/share/url?url={ref}")]
                    ]
                )
                bot_msg = await db.select_bot_message(code='chek_1_1')
                await call.message.answer(bot_msg['content'].format(full_name=call.from_user.full_name, competition_id=lang1["competition_id"]), reply_markup=menu_uz)
            elif lang1['lang'] == 'ru' and lang1['ban'] != False:
                link = await get_start_link(str(call.from_user.id), encode=True)
                bot_msg = await db.select_bot_message(code='chek_1_2')
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
                bot_msg = await db.select_bot_message(code='chek_1_3')
                await call.message.answer(bot_msg['content'].format(full_name=call.from_user.full_name, competition_id=lang1["competition_id"]), reply_markup=menu_ru)
        else:

            if lang1['lang'] == 'uz':
                bot_msg = await db.select_bot_message(code='chek_1_4')
                await call.message.answer(bot_msg['content'],
                    reply_markup=contact_uz)

            else:
                bot_msg = await db.select_bot_message(code='chek_1_5')
                await call.message.answer(bot_msg['content'],
                                          reply_markup=contact_ru)

            await UserInfo.phone.set()
    else:
        channel = await bot.get_chat(CHANNELS[0])
        invite_link = await channel.export_invite_link()
        if lang1['lang'] == 'uz':
            bot_msg = await db.select_bot_message(code='chek_1_6')
            await call.message.answer(bot_msg['content'].format(invite_link=invite_link, channel_username=channel.username, channel_title=channel.title), reply_markup=chek_uz,
                disable_web_page_preview=True)
        else:
            bot_msg = await db.select_bot_message(code='chek_1_7')
            await call.message.answer(bot_msg['content'].format(invite_link=invite_link, channel_username=channel.username, channel_title=channel.title), reply_markup=chek,
                disable_web_page_preview=True)
        await Chek.chek.set()
