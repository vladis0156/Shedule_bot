import pandas
import sqlite3

from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from loader import bot
from data import config
from keyboards.default import show_example
import utils


class FSMSupervisor(StatesGroup):
    floor_schedule = State()


# @dp.message_handler(Text(equals="Добавить график дежурств"), state=None)
async def supervisor_start(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await FSMSupervisor.floor_schedule.set()
    supervisors = utils.db_api.sqlite_db.get_supervisors_id()
    if str(chat_id) in supervisors or str(chat_id) in config.ADMINS:
        await message.answer('Загрузите список дежурств в формате .xlsx. Обратите внимание, что список дежурств должен '
                             'быть оформлен согласно примеру',
                             reply_markup=show_example)
    else:
        await message.answer('Вы не являетесь старостой. Для добавления вас в список старост, обратитесь к '
                             'разработчику.',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


# @dp.message_handler(content_types=['document'], state=FSMSupervisor.floor_schedule)
async def get_schedule(message: Message, state: FSMContext):
    chat_id = message.chat.id
    supervisors_list = utils.db_api.sqlite_db.get_supervisors_id()
    if str(chat_id) in supervisors_list or str(chat_id) in config.ADMINS:
        src = r'C:\Users\Vladislav Shamraev\Desktop\Programming\schedule_bot\tables\floor_' + message.document.file_name
        file_name = message.document.file_name

        if utils.validation.validation_excel(file_name):
            await message.answer('Неправильное название файла')
        else:
            try:
                async with state.proxy() as data:
                    data['floor_schedule'] = await bot.get_file(message.document.file_id)
                    file_info = data['floor_schedule']
                downloaded_file = await bot.download_file(file_info.file_path)
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file.getvalue())

                panda_db = pandas.read_excel(downloaded_file, sheet_name=None)
                con = sqlite3.connect('sixth_floor.db')

                for sheet in panda_db:
                    panda_db[sheet].to_sql(sheet, con, if_exists='replace', index=False)
                con.commit()
                con.close()

                await message.answer('Пожалуй, я сохраню это', reply_markup=ReplyKeyboardRemove())
            except Exception as e:
                await message.answer(e)
    else:
        await message.answer('Недасточтоно прав доступа для загрузки файла',
                             reply_markup=ReplyKeyboardRemove())
    await state.finish()


# @dp.message_handler(Text(equals="Посмотреть пример оформления списка дежурств"), state="*")
async def list_design(message: Message):
    photo = open(r'C:\Users\Vladislav Shamraev\Desktop\Programming\schedule_bot\Example.png', 'rb')
    await bot.send_document(message.chat.id, document=photo)
    await bot.send_message(message.chat.id,
                           ('\n1) Книга должна быть названа лишь одним числом - номером вашего этажа\n \n'
                            '2) Книга должна состоять из одного листа и его название должно выглядеть так: "floor" + '
                            'номер вашего этажа (без пробела!!)\n \n '
                            '3) Первые два столбца должны называться в соотвествии с примером на скриншоте\n\n'
                            '4) Эти требования необходимы для корректной работы бота.\n '
                            '                                            '),
                           reply_markup=ReplyKeyboardRemove())


# Выход из состяний
# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Ок', reply_markup=ReplyKeyboardRemove())


def register_handler_supervisors(dp: Dispatcher):
    dp.register_message_handler(supervisor_start, Text(equals="Добавить график дежурств"), state=None)
    dp.register_message_handler(get_schedule, content_types=['document'], state=FSMSupervisor.floor_schedule)
    dp.register_message_handler(list_design, Text(equals="Посмотреть пример оформления списка дежурств"), state="*")
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
