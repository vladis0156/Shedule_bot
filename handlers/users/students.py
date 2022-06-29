from datetime import date

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

import utils
from loader import bot, dp
from utils.db_api import sqlite_db


class FSMStudent(StatesGroup):
    block_number = State()


# @dp.message_handler(Text(equals='Подписаться на рассылку уведомлений о дежурствах'), state=None)
async def cm_start(message: Message):
    await FSMStudent.block_number.set()
    await message.reply('Укажите номер блока и комнаты через, например 617/2 или 601(если вы живете в аспирантской)',
                        reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(state=FSMStudent.block_number)
async def choose_room(message: Message, state: FSMContext):
    room_number = message.text
    async with state.proxy() as data:
        data['room_number'] = message.text

    user_id = message.chat.id
    if utils.validation.validation_room(room_number):
        await message.answer('Неправильно указана комната', reply_markup=ReplyKeyboardRemove())
    else:
        await sqlite_db.sql_add_command(room_number, user_id)
        await message.reply('Вы подписались на уведомления о дежурствах :)',
                            reply_markup=ReplyKeyboardRemove())
        await state.finish()


# @dp.message_handler(Text(equals='Отписаться от рассылки'))
async def delete_student(message: Message):
    sqlite_db.del_student_id(message.chat.id)
    await message.reply('Вы больше не будете получать уведомления о дежурствах.',
                        reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(Command('admin'))
async def admin_info(message: Message):
    await message.answer('\n Telegram: https://t.me/Vladis0156\n'
                         'Вконтакте: https://vk.com/whhat_is_love\n'
                         'GitHub: https://github.com/vladis0156\n',
                         reply_markup=ReplyKeyboardRemove()
                         )


async def send_notification():
    today = int(str(date.today())[-2:])
    id_list = sqlite_db.get_students_id(today)
    for student_id in id_list:
        await bot.send_message(
            student_id,
            'Вы сегодня дежурите. Пожалуйста, уберитесь на кухне и выбросьте мусор до 23:00.',
            reply_markup=ReplyKeyboardRemove()
        )


def register_handler_student(dp: Dispatcher):
    dp.register_message_handler(cm_start, Text(equals='Подписаться на рассылку уведомлений о дежурствах'), state=None)
    dp.register_message_handler(choose_room, state=FSMStudent.block_number)
    dp.register_message_handler(admin_info, Command('admin'))
    dp.register_message_handler(delete_student, Text(equals='Отписаться от рассылки'))
