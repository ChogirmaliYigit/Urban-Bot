from aiogram.dispatcher.filters.state import StatesGroup, State


class Reklama(StatesGroup):
    reklama = State()


class Lang(StatesGroup):
    select = State()


class UserInfo(StatesGroup):
    name = State()
    phone = State()
    birthday = State()

class Forward(StatesGroup):
    one = State()


class Upload(StatesGroup):
    one = State()

class Chek(StatesGroup):
    chek = State()

class Start(StatesGroup):
    start = State()


class Channel(StatesGroup):
    add = State()
    delete = State()
    delete_confirm = State()
