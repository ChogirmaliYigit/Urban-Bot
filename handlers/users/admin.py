import asyncio

import os
import sqlite3
import datetime
import aiogram
import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from keyboards.default.menu import cancel, admin_key
from keyboards.inline.menu_in import yesno
from loader import dp, db, bot
from states.state import Reklama, Forward, Upload
from xlsxwriter.workbook import Workbook

import logging


@dp.message_handler(text="📊 Статистика", user_id=ADMINS)
async def get_all_users(message: types.Message):
    bot_msg = await db.select_bot_message(code='get_all_users')
    users = await db.count_users()
    await message.answer(bot_msg['content'].format(users=users))


@dp.message_handler(text="📨 Пересылка сообщения", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    bot_msg = await db.select_bot_message(code='send_ad_to_all')
    await message.answer(bot_msg['content'], reply_markup=cancel)
    await Forward.one.set()


@dp.message_handler(content_types=types.ContentType.ANY, state=Forward.one)
async def answer_fullname(message: types.Message, state: FSMContext):
    if message.text != "Отменить":
        try:
            cnt = 0
            users = await db.select_all_users()
            for user in users:
                try:
                    try:
                            await bot.forward_message(chat_id=user['id'],
                                                      from_chat_id=message.forward_from_chat.id,
                                                      message_id=message.forward_from_message_id)
                            cnt += 1
                            await asyncio.sleep(0.07)
                    except aiogram.utils.exceptions.MessageToForwardNotFound:
                        bot_msg = await db.select_bot_message(code='answer_fullname_1')
                        await message.answer(bot_msg['content'], reply_markup=admin_key)
                        await state.finish()
                        break
                except:
                    pass
            bot_msg = await db.select_bot_message(code='answer_fullname_2')
            await message.answer(bot_msg['content'].format(cnt=cnt), reply_markup=admin_key)
            await state.finish()
        except AttributeError:
            bot_msg = await db.select_bot_message(code='answer_fullname_3')
            await message.answer(bot_msg['content'])

    else:
        bot_msg = await db.select_bot_message(code='answer_fullname_3')
        await message.answer(bot_msg['content'], reply_markup=admin_key)
        await state.finish()


@dp.message_handler(text='✉ Реклама', user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    bot_msg = await db.select_bot_message(code='send_ad_to_all_1')
    await message.answer(bot_msg['content'], reply_markup=cancel)
    await Reklama.reklama.set()


@dp.message_handler(state=Reklama.reklama)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    reklama_text = message.text
    if reklama_text != 'Отменить':
        users = await db.select_all_users()
        cnt = 0
        for user in users:

            user_id = user[0]
            try:
                cnt += 1
                await bot.send_message(chat_id=user_id, text=reklama_text)
                await asyncio.sleep(0.05)
            except:
                pass
        bot_msg = await db.select_bot_message(code='send_ad_to_all_2')
        await message.answer(bot_msg['content'].format(cnt=cnt), reply_markup=admin_key)
        await state.finish()
    else:
        bot_msg = await db.select_bot_message(code='send_ad_to_all_3')
        await message.answer(bot_msg['content'], reply_markup=admin_key)
        await state.finish()


@dp.message_handler(text='🔂 Рестарт', user_id=ADMINS)
async def restart(message: types.Message):
    bot_msg = await db.select_bot_message(code='restart')
    await message.answer(bot_msg['content'], reply_markup=yesno)


@dp.callback_query_handler(text='yes')
async def yes(call: types.CallbackQuery):
    await call.message.delete()
    user = await db.select_all_users()
    for i in user:
        await db.user_restart(tg_id=i['id'], count=0)
    bot_msg = await db.select_bot_message(code='yes')
    await call.message.answer(bot_msg['content'], reply_markup=admin_key)


@dp.callback_query_handler(text='no')
async def no(call: types.CallbackQuery):
    await call.message.delete()
    bot_msg = await db.select_bot_message(code='no')
    await call.message.answer(bot_msg['content'], reply_markup=admin_key)


@dp.message_handler(text='📇 Excel')
async def excel(message: types.Message):
    user = await db.select_all_users()
    workbook = Workbook(
        f'backend/conf/{datetime.datetime.now().strftime("%Y_%m_%d")}.xlsx')  # Файл который надо передать админу
    worksheet = workbook.add_worksheet(name="Users")
    bold = workbook.add_format({'bold': True})
    worksheet.write('A1', 'ID', bold)
    worksheet.write('B1', 'USERNAME', bold)
    worksheet.write('C1', 'TG_NAME', bold)
    worksheet.write('D1', 'COMPETITION_ID', bold)
    worksheet.write('E1', 'NAME', bold)
    worksheet.write('F1', 'PHONE', bold)
    worksheet.write('G1', 'DATE', bold)
    worksheet.write('H1', 'REF_COUNT', bold)
    worksheet.write('I1', 'PARENT_ID', bold)
    worksheet.write('J1', 'LANG', bold)
    worksheet.write('K1', 'BAN', bold)
    for i, row in enumerate(user):
        for j, value in enumerate(row):
            worksheet.write(i + 1, j, str(value))
    workbook.close()
    await message.answer_document(
        document=open(f'backend/conf/{datetime.datetime.now().strftime("%Y_%m_%d")}.xlsx', 'rb'))


@dp.message_handler(text='⬇️Загрузить')
async def upload(message: types.Message):
    bot_msg = await db.select_bot_message(code='upload')
    await message.answer(bot_msg['content'], reply_markup=cancel)
    await Upload.one.set()


@dp.message_handler(text='Отменить', state=Upload.one)
async def text(message: types.Message, state: FSMContext):
    bot_msg = await db.select_bot_message(code='text')
    await message.answer(bot_msg['content'], reply_markup=admin_key)
    await state.finish()


@dp.message_handler(content_types=['document'], state=Upload.one)
async def file_upl(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    await bot.download_file(file.file_path, 'data/upload.db')
    conn = sqlite3.connect("data/upload.db")
    cursor = conn.execute("SELECT * FROM Users").fetchall()
    for i in cursor:
        try:
            try:
                try:
                    alld = i[5].split('.')
                    date = datetime.date(day=int(alld[0]), month=int(alld[1]), year=int(alld[2]))
                    lang = ''
                    if i[8] == 'rus':
                        lang = 'ru'
                    elif i[8] == 'uzb':
                        lang = 'uz'
                    await db.add_new(telegram_id=i[0],
                                     full_name=i[1],
                                     username=None,
                                     ref_count=i[6],
                                     parent=i[7],
                                     birth_day=date,
                                     lang=lang,
                                     phone=i[4],
                                     name2=i[3],
                                     ban=True,
                                     conkurs=int(i[2]))
                except AttributeError:
                    pass
            except ValueError:
                pass
        except asyncpg.exceptions.UniqueViolationError:
            pass
    bot_msg = await db.select_bot_message(code='file_upl')
    await message.answer(bot_msg['content'], reply_markup=admin_key)
    conn.close()
    os.remove(f'data/upload.db')
    await state.finish()


@dp.message_handler(text='SQLite')
async def sqlite(message: types.Message):

    user = await db.select_all_users()
    conn = sqlite3.connect(
        f"data/SQLite.db")
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE "main_user" ("id" bigint NOT NULL UNIQUE, "username" varchar(150) NULL, "name" varchar(150) NULL, "competition_id" bigint NOT NULL PRIMARY KEY, "fullname" varchar(250) NULL, "phone" varchar(250) NULL, "birth_day" date NULL, "ref_count" bigint NULL, "parent" bigint NULL, "lang" varchar(250) NULL, "ban" boolean NOT NULL);')
    conn.commit()
    for i in user:
        cursor.execute(
            '''INSERT INTO main_user("id", "username", "name" , "competition_id" , "fullname", "phone" , "birth_day", "ref_count", "parent", "lang" ,"ban") VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
            (i['id'], i['username'], i['name'], i['competition_id'], i['fullname'], i['phone'], i['birth_day'],
             i['ref_count'], i['parent'], i['lang'], i['ban'])
        )
        conn.commit()
    await message.answer_document(document=open(f'data/SQLite.db', 'rb'), reply_markup=admin_key)
    conn.close()
    os.remove('data/SQLite.db')

