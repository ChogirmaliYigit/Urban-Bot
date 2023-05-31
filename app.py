from aiogram import executor
import asyncio
from loader import dp, db
import middlewares, filters, handlers
from handlers.users.b_day import scheduler
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()

    # Команды первой важности (/start и /help)
    await set_default_commands(dispatcher)

    # Уведомляет админов о запуске бота
    await on_startup_notify(dispatcher, db)

    asyncio.create_task(scheduler())

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
