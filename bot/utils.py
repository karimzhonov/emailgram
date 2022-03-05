import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext

from config import APPNAME, ROUTER_DICT
from api_requests import get_admins


async def on_startup_notify(dp: Dispatcher):
    admins = await get_admins()
    for admin in admins:
        try:
            await dp.bot.send_message(admin['user_id'], "Бот Запущен ----------")

        except Exception as err:
            logging.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
        ]
    )


class Message:
    def __init__(self, call: types.CallbackQuery, state: FSMContext):
        self.call = call
        self.state = state
        self.data = None

    async def get_data(self):
        return await self.state.get_data()

    async def update_data(self, data: dict = None, **kwargs):
        await self.state.update_data(data, **kwargs)

def _set_router(*args):
    _router = ['Home']
    for r in args:
        try:
            _router.append(ROUTER_DICT[r])
        except KeyError:
            _router.append(r)
    return '/'.join(_router)


def render_message(*router,
                   subject: str = '',
                   from_: str = '',
                   date: str = '',
                   body: str = '',
                   footer: str = ''):
    """
    Router, data - code
    Subject, From_ --- Bold
    Footer - Italic
    """

    app_name = f'{APPNAME}\n'
    router = f'<code>/{_set_router(*router)}/</code>\n\n' if router else ''
    subject = f'<b>Subject:</b> {subject}\n' if subject else ''
    from_ = f'<b>From:</b> {from_}\n' if from_ else ''
    date = f'<b>Date:</b> {date}\n\n' if date else ''
    body = f'{body}\n' if body else ''
    footer = f'<i>{footer}</i>\n' if footer else ''

    mark = ''.join([
        app_name,
        router,
        subject,
        from_,
        date,
        body,
        footer,
    ])
    return mark
