import aioschedule
import asyncio

from aiogram import executor

from handlers.users import students, supervisors, admins
from loader import dp
from utils.db_api.sqlite_db import sql_start
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def scheduler():
    aioschedule.every().day.at('22:00').do(students.send_notification)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Импорт хендлеров студентов
    students.register_handler_student(dp)

    # Импорт хендлеров старост
    supervisors.register_handler_supervisors(dp)

    # Импорт хендлеров админов
    admins.register_handler_admins(dp)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)

    # Уведомляет о подключении базы данных
    sql_start()

    # Рассылка уведомлений о дежурстве
    asyncio.create_task(scheduler())


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
