import asyncio
import datetime
import logging

from aiogram import Dispatcher

from data.config import ADMINS

async def on_startup_notify(dp: Dispatcher, db):
    for admin in ADMINS:
        try:
            bot_msg = await db.select_bot_message(code='on_startup_notify')
            await dp.bot.send_message(admin, bot_msg['content'])
        except Exception as err:
            logging.exception(err)
    # while True:
    #     for admin in ADMINS:
    #         try:
    #             await dp.bot.send_message(admin, "Не забудьте поздравить своих подписчиков  нажав на команду /bday\n"
    #                                              "Я вам напомню это и завтра)")
    #         except Exception as err:
    #             logging.exception(err)
    #     await asyncio.sleep(86400)

