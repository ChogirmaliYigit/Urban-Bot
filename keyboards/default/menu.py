from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton



contact_ru = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить номер!', request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

contact_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Raqam yuborish!', request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отменить')]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='🎉 День рождения!'), KeyboardButton(text='📊 Статистика')],
        [KeyboardButton(text='✉ Реклама'), KeyboardButton(text='📨 Пересылка сообщения')],
        [KeyboardButton(text='📇 Excel'), KeyboardButton(text='🔂 Рестарт')],
        [KeyboardButton(text='⬇️Загрузить'),KeyboardButton(text='SQLite')],
        [KeyboardButton(text='Каналы')],
        [KeyboardButton(text='Добавить канал'), KeyboardButton(text="Удалить канал")],
    ],
    resize_keyboard=True,
)
