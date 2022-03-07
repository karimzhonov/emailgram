from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from loader import dp
from storage import Session
from utils import render_message as _


class NewEmailMessage:
    keyboard_back_to_util_name = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Back', callback_data='back_to_email_util_name')]
    ])

    keyboard_result = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Send', callback_data='new_email_message_send')],
        [types.InlineKeyboardButton('Back', callback_data='back_to_email_util_name')]
    ])

    def __init__(self, state: FSMContext):
        self.data: dict = {}
        self.state = state

    async def get_data(self):
        return await self.state.get_data()

    def get_to_email_text(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        return _(etype, ename, eutil,
                 body='Enter to email')

    def get_subject_text(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        new_email_message_to_email = self.data['new_email_message_to_email']
        return _(etype, ename, eutil,
                 to=new_email_message_to_email,
                 body='Enter Subject:')

    def get_message_text(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        new_email_message_to_email = self.data['new_email_message_to_email']
        new_email_message_subject = self.data['new_email_message_subject']
        return _(etype, ename, eutil,
                 to=new_email_message_to_email,
                 subject=new_email_message_subject,
                 body='Enter Message')

    def get_resualt_text(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        new_email_message_to_email = self.data['new_email_message_to_email']
        new_email_message_subject = self.data['new_email_message_subject']
        new_email_message_message = self.data['new_email_message_message']
        return _(etype, ename, eutil,
                 to=new_email_message_to_email,
                 subject=new_email_message_subject,
                 body=new_email_message_message,
                 footer='Do you want to send?')

    def get_msg_sent_ok(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        new_email_message_to_email = self.data['new_email_message_to_email']
        new_email_message_subject = self.data['new_email_message_subject']
        new_email_message_message = self.data['new_email_message_message']
        return _(etype, ename, eutil,
                 to=new_email_message_to_email,
                 subject=new_email_message_subject,
                 body=new_email_message_message,
                 footer='Message sent succes')

    def get_msg_sent_no(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        eutil = self.data["email_util_name"]
        new_email_message_to_email = self.data['new_email_message_to_email']
        new_email_message_subject = self.data['new_email_message_subject']
        new_email_message_message = self.data['new_email_message_message']
        return _(etype, ename, eutil,
                 to=new_email_message_to_email,
                 subject=new_email_message_subject,
                 body=new_email_message_message,
                 footer='Message sent no')

    async def render_get_to_email(self, call: types.CallbackQuery):
        self.data = await self.get_data()
        text = self.get_to_email_text()
        keyboard = self.keyboard_back_to_util_name

        await call.message.edit_text(text, reply_markup=keyboard)

    async def render_get_subject(self):
        self.data = await self.get_data()

        text = self.get_subject_text()
        keyboard = self.keyboard_back_to_util_name
        callback_query_msg_id = self.data['callback_query_msg_id']
        chat_id = self.data['user_id']

        await dp.bot.edit_message_text(text, chat_id, callback_query_msg_id,
                                       callback_query_msg_id, reply_markup=keyboard)

    async def render_get_message(self):
        self.data = await self.get_data()
        text = self.get_message_text()
        keyboard = self.keyboard_back_to_util_name

        callback_query_msg_id = self.data['callback_query_msg_id']
        chat_id = self.data['user_id']

        await dp.bot.edit_message_text(text, chat_id, callback_query_msg_id,
                                       callback_query_msg_id, reply_markup=keyboard)

    async def render_get_result(self):
        self.data = await self.get_data()
        text = self.get_resualt_text()
        keyboard = self.keyboard_result

        callback_query_msg_id = self.data['callback_query_msg_id']
        chat_id = self.data['user_id']

        await dp.bot.edit_message_text(text, chat_id, callback_query_msg_id,
                                       callback_query_msg_id, reply_markup=keyboard)

    async def render_message_sent(self, call: types.CallbackQuery, status: bool):
        self.data = await self.get_data()

        if status:
            text = self.get_msg_sent_ok()
        else:
            text = self.get_msg_sent_no()
        keyboard = self.keyboard_back_to_util_name

        await call.message.edit_text(text, reply_markup=keyboard)


@dp.message_handler(state=Session.new_email_message_to_email)
async def new_email_message_to_email_func(msg: types.Message, state: FSMContext):
    await state.update_data(new_email_message_to_email=msg.text)
    await msg.delete()

    await Session.new_email_message_subject.set()
    await NewEmailMessage(state).render_get_subject()


@dp.message_handler(state=Session.new_email_message_subject)
async def new_email_message_subject_func(msg: types.Message, state: FSMContext):
    await state.update_data(new_email_message_subject=msg.text)
    await msg.delete()

    await Session.new_email_message_message.set()
    await NewEmailMessage(state).render_get_message()


@dp.message_handler(state=Session.new_email_message_message)
async def new_email_message_message_func(msg: types.Message, state: FSMContext):
    await state.update_data(new_email_message_message=msg.text)
    await msg.delete()

    await Session.new_email_message_result.set()
    await NewEmailMessage(state).render_get_result()


@dp.callback_query_handler(lambda c: c.data == 'new_email_message_send', state='*')
async def new_email_message_result_func(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()

    client = data['email_client']
    msg_to_email = data['new_email_message_to_email']
    msg_subject = data['new_email_message_subject']
    msg_message = data['new_email_message_message']

    status = client.send(msg_subject, msg_message, msg_to_email)
    await NewEmailMessage(state).render_message_sent(call, status)


@dp.callback_query_handler(lambda c: c.data == 'back_to_email_util_name', state='*')
async def back_to_email_util_name_func(call: types.CallbackQuery, state: FSMContext):
    from views.users.email_utils_list import EmailUtilsList

    await Session.email_util_name.set()
    await EmailUtilsList(call, state).render()
