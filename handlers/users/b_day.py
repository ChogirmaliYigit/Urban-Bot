import asyncio
import aioschedule
import datetime
from loader import bot, db
from data.config import ADMINS


async def congratulation_birth_day():
    users = await db.select_all_users()
    print(users)
    user_all_brithday = 'Сегодня День рождение у:\n\n'
    today = datetime.datetime.now().strftime('%d-%m')
    cnt = 0
    for user in users:
        cnt += 1
        if user['birth_day']:
            if user['birth_day'].strftime('%d-%m') == today:
                user_all_brithday += f'Имя: <a href="tg://user?id={user["id"]}">{user["fullname"]}</a> | @{user["username"]}\n' \
                                        f'Номер телефона: +{user["phone"]}\n\n'
                lang_db = await db.show_lang(id=user['id'])

                if lang_db['lang'] == 'uz':
                    code = 'congratulation_birth_day_uz'
                else:
                    code = 'congratulation_birth_day_ru'
                bot_msg = await db.select_bot_message(code=code)
                try:
                    await bot.send_message(chat_id=user['id'], text=bot_msg['content'])
                except Exception as err:
                    print("1-", err)

    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=admin, text=user_all_brithday)
        except Exception as error:
            print('2-', error)


async def scheduler():
    aioschedule.every().day.at("12:00").do(congratulation_birth_day)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
