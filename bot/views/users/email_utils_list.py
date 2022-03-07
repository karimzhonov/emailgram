from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from loader import dp
from storage import Session
from utils import Message, render_message as _
from api_requests import remove_email


class EmailUtilsList(Message):
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton('New Email', callback_data='new_email_message')],
        [types.InlineKeyboardButton('Inbox', callback_data='email_inbox')],
        [types.InlineKeyboardButton('Exit from account', callback_data='email_exit')],
        [types.InlineKeyboardButton('Back', callback_data=f'back_to_emails_list')],
    ])

    async def get_email_utils_list_text(self):
        etype = self.data["email_type"]
        ename = self.data["email_name"]
        return _(f'{etype}', f'{ename}')

    async def render(self):
        self.data = await self.get_data()
        text = await self.get_email_utils_list_text()
        await self.call.message.edit_text(text)
        await self.call.message.edit_reply_markup(self.keyboard)


@dp.callback_query_handler(lambda c: c.data == 'new_email_message', state=Session.email_util_name)
async def new_email_message(call: types.CallbackQuery, state: FSMContext):
    from views.users.new_emial_message import NewEmailMessage

    await state.update_data(email_util_name='new_email_message')
    await Session.new_email_message_to_email.set()
    await NewEmailMessage(state).render_get_to_email(call)


@dp.callback_query_handler(lambda c: c.data == 'email_exit', state=Session.email_util_name)
async def exit_account(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await remove_email(user_id=call.from_user.id, email=data['email_name'])

    await back_to_emails_list(call, state)


@dp.callback_query_handler(lambda c: c.data == 'back_to_emails_list', state=Session.email_util_name)
async def back_to_emails_list(call: types.CallbackQuery, state: FSMContext):
    from views.users.emails_list import EmailAccountList

    await Session.email_name.set()
    await EmailAccountList(call, state).render()


@dp.callback_query_handler(state=Session.email_util_name)
async def open_email_util(call: types.CallbackQuery, state: FSMContext):
    from views.users.inbox_message_list import InboxMessageList

    await Session.email_msg.set()
    await state.update_data({
        'email_util_name': call.data,
        'start_idx': 0,
        'end_idx': 10,
    })
    await InboxMessageList(call, state).render()
