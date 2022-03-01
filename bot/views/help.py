from aiogram import types
from aiogram.dispatcher.filters import CommandHelp

from bot import dp
from bot.utils import render_message as _

@dp.message_handler(CommandHelp())
async def thelp(msg: types.Message):
    item = ("Список команд: ",
            "/start - Начать диалог",
            "/help - Получить справку")

    text = _('Help', footer='\n'.join(item))
    await msg.answer(text)