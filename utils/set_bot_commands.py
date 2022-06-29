from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("menu", "Загрузить список дежурств или указать блок для получения уведомлений"),
            types.BotCommand("admin", "Связь с разработчиком")
        ]
    )
