from copy import deepcopy

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.dispatcher.storage import FSMContext

from loader import dp
from storage import Session
from utils import render_message as _
from api_requests import user_get_or_create


class StartMessage:
    start_button = types.ReplyKeyboardMarkup([[types.KeyboardButton('Start')]], resize_keyboard=True)

    email_type_list = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Mail', callback_data='mail')],
        [types.InlineKeyboardButton(text='Gmail', callback_data='gmail')],
    ])

    def __init__(self, msg: types.Message):
        self.msg = msg

    async def get_start_text(self):
        bot_data = await self.msg.bot.get_me()
        bot_name = bot_data["first_name"]
        return _()

    async def start_render(self):
        text = await self.get_start_text()
        await self.msg.answer(text, reply_markup=self.email_type_list)

@dp.message_handler(CommandStart(), state='*')
async def start(msg: types.Message, state: FSMContext = None):
    data = deepcopy(msg.from_user.__dict__['_values'])
    user_id = msg.chat.id
    data.pop('id')
    await user_get_or_create(user_id, **data)
    try:
        await state.reset_data()
        await state.update_data(user_id=msg.from_user.id)
    except AttributeError:
        pass
    await Session.email_type.set()
    await StartMessage(msg).start_render()

@dp.message_handler(text='Start', state='*')
async def start_word(msg: types, state: FSMContext = None):
    await start(msg, state)


@dp.callback_query_handler(state=Session.email_type)
async def email_type_list(call: types.CallbackQuery, state: FSMContext):
    from views.users.emails_list import EmailAccountList
    await Session.email_name.set()

    await state.update_data({
        'user_id': call.from_user.id,
        'email_type': call.data,
        'last_msg_text': call.message.text,
        'last_msg_kb': call.message.reply_markup,
        'callback_query_msg_id': call.message.message_id
    })
    await EmailAccountList(call, state).render()
