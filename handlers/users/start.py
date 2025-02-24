import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.deep_linking import get_start_link, decode_payload
from data.config import ADMINS, CHANNELS
from keyboards.default.menu import admin_key, contact_uz, contact_ru
from keyboards.inline.menu import lang, chek, chek_uz
from keyboards.inline.menu_in import get_channels_markup_user
from loader import db, bot
from loader import dp
from states.state import Lang, Chek, UserInfo
from utils.misc.subscription import get_user_subscribe_channels


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
    except asyncpg.exceptions.UniqueViolationError:
        pass
    await message.answer(bot_msg['content'], reply_markup=admin_key)
    await state.finish()


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    bot_info = await db.bot_info()
    lang_db = await db.show_lang(id=message.from_user.id)

    if bot_info[0]['contest'] == True:
        channels = await db.select_all_channels()
        channel_ids = {int(CHANNELS[0])}
        for channel in channels:
            channel_ids.add(int(channel["chat_id"]))

        subscribe_channels = await get_user_subscribe_channels(channel_ids, message.from_user.id)
        if subscribe_channels:
            bot_msg = await db.select_bot_message(code=f"subscribe_these_channels_{lang_db['lang'] if lang_db else 'ru'}")
            await message.answer(
                text=bot_msg["content"] if bot_msg else "Пожалуйста, подпишитесь на эти каналы",
                reply_markup=await get_channels_markup_user(subscribe_channels)
            )
            return

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
    lang1 = await db.show_lang(id=call.from_user.id)
    channels = await db.select_all_channels()
    channel_ids = {int(CHANNELS[0])}
    for channel in channels:
        channel_ids.add(int(channel["chat_id"]))

    subscribe_channels = await get_user_subscribe_channels(channel_ids, call.from_user.id)
    if subscribe_channels:
        bot_msg = await db.select_bot_message(code=f"subscribe_these_channels_{lang1['lang'] if lang1 else 'ru'}")
        await call.message.answer(
            text=bot_msg["content"] if bot_msg else "Пожалуйста, подпишитесь на эти каналы",
            reply_markup=await get_channels_markup_user(subscribe_channels)
        )
        return

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
