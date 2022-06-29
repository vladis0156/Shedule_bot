from loader import dp
from aiogram.types import Message
from keyboards.default import start_menu
from aiogram.dispatcher.filters import Command


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите цель вашего обращения:",
                         reply_markup=start_menu)
