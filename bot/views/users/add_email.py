from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import asyncio

from loader import dp
from storage import Session
from client import Client
from views.users.email_utils_list import back_to_emails_list
from utils import render_message as _
from api_requests import email_create

class AddEmailForm:
    back_to_email_list_kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('Back', callback_data='back_to_emails_list_from_add')]
    ])

    @staticmethod
    def get_text_enter_email(data: dict):
        etype = data["email_type"]
        ename = data["email_name"]
        return _(etype, ename,
                 body='Enter Email ')

    @staticmethod
    def get_text_enter_password(data: dict):
        etype = data["email_type"]
        ename = data["email_name"]
        return _(etype, ename,
                 body=f'Email: {data["adding_email_name"]}\nEnter Password ')

    @staticmethod
    def get_text_checking_email(data: dict):
        etype = data["email_type"]
        ename = data["email_name"]
        return _(etype, ename,
                 body=f'Checking Email {ename}')

    @staticmethod
    def get_text_response_ok(data: dict):
        etype = data["email_type"]
        ename = data["email_name"]
        return _(etype, ename,
                 body=f'Account added succesfuly')

    @staticmethod
    def get_text_response_no(data: dict):
        etype = data["email_type"]
        ename = data["email_name"]
        return _(etype, ename,
                 body=f'Email or password invalid')

    async def event_btn_add_emial(self, call: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        text = self.get_text_enter_email(data)
        await state.update_data(callback_query_msg_id=call.message.message_id)
        await call.message.edit_text(text)
        await call.message.edit_reply_markup(self.back_to_email_list_kb)

    async def get_email_event_handler(self, msg: types.Message, state: FSMContext):
        await Session.adding_email_password.set()
        email_name = msg.text

        await dp.bot.delete_message(msg.chat.id, msg.message_id)
        await state.update_data(adding_email_name=email_name)
        data = await state.get_data()
        text = self.get_text_enter_password(data)
        await dp.bot.edit_message_text(text, msg.chat.id,
                                       data['callback_query_msg_id'],
                                       data['callback_query_msg_id'],
                                       reply_markup=self.back_to_email_list_kb)

    async def get_password_event_handler(self, msg: types.Message, state: FSMContext):
        password = msg.text
        await dp.bot.delete_message(msg.chat.id, msg.message_id)
        # Geting data
        data = await state.get_data()
        email_name = data['adding_email_name']
        call_back_msg_id = data['callback_query_msg_id']
        email_type = data['email_type']
        text = self.get_text_checking_email(data)
        await dp.bot.edit_message_text(text, msg.chat.id,
                                       call_back_msg_id, call_back_msg_id,
                                       reply_markup=None)
        # Checking Emial
        status = Client(email_name, password, email_type).check_email()
        if status == 'OK':
            await Session.email_name.set()

            await email_create(msg.from_user.id, password=password,
                                  email=email_name, email_type=email_type)

            text = self.get_text_response_ok(data)
        else:
            await Session.email_name.set()
            text = self.get_text_response_no(data)

        await asyncio.sleep(1)
        await dp.bot.edit_message_text(text, msg.chat.id, call_back_msg_id, call_back_msg_id,
                                       reply_markup=self.back_to_email_list_kb)


@dp.callback_query_handler(lambda c: c.data == 'add_email')
async def add_mail_account(callback_query: types.CallbackQuery, state: FSMContext):
    await Session.adding_email_name.set()
    await AddEmailForm().event_btn_add_emial(callback_query, state)


@dp.callback_query_handler(lambda c: c.data == 'back_to_emails_list_from_add', state='*')
async def back_to_emails_list_from_add(call: types.CallbackQuery, state: FSMContext):
    await back_to_emails_list(call, state)


@dp.message_handler(state=Session.adding_email_name)
async def get_email(msg: types.Message, state: FSMContext):
    await Session.adding_email_password.set()
    await AddEmailForm().get_email_event_handler(msg, state)


@dp.message_handler(state=Session.adding_email_password)
async def get_password(msg: types.Message, state: FSMContext):
    await Session.email_util_name.set()
    await AddEmailForm().get_password_event_handler(msg, state)
