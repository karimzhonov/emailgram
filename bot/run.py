import logging
from aiogram import executor

from bot import dp, views
from bot.utils import set_default_commands, on_startup_notify

async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


def run_bot():
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)

if __name__ == '__main__':
    run_bot()