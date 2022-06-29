from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message

from loader import dp
from data import config
from utils.db_api import sqlite_db


class FSMAdmins(StatesGroup):
    supervisor_floor = State()
    supervisor_id = State()
    supervisor_del = State()


# Добавить старосту этажа через бота
# @dp.message_handler(Text(equals='Добавить старосту этажа'), state=None)
async def add_supervisor(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if str(chat_id) in config.ADMINS:
        await FSMAdmins.supervisor_floor.set()
        await message.reply('Укажите номер этажа старосты')
    else:
        await message.reply('Вы не являетесь админом бота')
        await state.finish()


# Указываем этаж старосты
# @dp.message_handler(state=FSMAdmins.supervisor_floor)
async def add_supervisor_floor(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['supervisor_floor'] = message.text
    await FSMAdmins.next()
    await message.reply('Теперь укажите id старосты')


# Указываем айди старосты
# @dp.message_handler(state=FSMAdmins.supervisor_id)
async def add_supervisor_id(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['supervisor_id'] = message.text

    async with state.proxy() as data:
        await sqlite_db.add_supervisor(data['supervisor_floor'], data['supervisor_id'])
    await message.reply('Готово')
    await state.finish()


# Получить этаж старосты для удаления его айди из бд
# @dp.message_handler(Text(equals='Удалить старосту этажа'), state=None)
async def delete_handler(message: Message, state: FSMContext):
    chat_id = message.chat.id
    if str(chat_id) in config.ADMINS:
        await FSMAdmins.supervisor_del.set()
        await message.reply('Укажите номер этажа старосты')
    else:
        await message.reply('Вы не являетесь админом бота')
        await state.finish()


# Удалить старосту из бд
# @dp.message_handler(state=FSMAdmins.supervisor_del)
async def delete_supervisor(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['supervisor_del'] = message.text

    async with state.proxy() as data:
        await sqlite_db.del_supervisor(data['supervisor_del'])

    await message.reply('Готово')
    await state.finish()


# Выход из состяний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок')


def register_handler_admins(dp: Dispatcher):
    dp.register_message_handler(add_supervisor, Text(equals='Добавить старосту этажа'), state=None)
    dp.register_message_handler(add_supervisor_floor, state=FSMAdmins.supervisor_floor)
    dp.register_message_handler(add_supervisor_id, state=FSMAdmins.supervisor_id)
    dp.register_message_handler(delete_handler, Text(equals='Удалить старосту этажа'), state=None)
    dp.register_message_handler(delete_supervisor, state=FSMAdmins.supervisor_del)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
