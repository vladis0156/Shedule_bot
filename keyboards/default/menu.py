from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить график дежурств')
        ],
        [
            KeyboardButton(text='Подписаться на рассылку уведомлений о дежурствах')
        ],
        [
            KeyboardButton(text='Отписаться от рассылки')
        ],
    ],
    resize_keyboard=True
)

show_example = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Посмотреть пример оформления списка дежурств')],
        [KeyboardButton(text='Отмена')],
    ],
    resize_keyboard=True
)
