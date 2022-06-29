from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

notify_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Я продежурил')
        ],
    ],
    resize_keyboard=True
)